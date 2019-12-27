from ursina import *
import PIL
from PIL import Image, ImageChops
import numpy as np
import time
from panda3d.core import Texture as PandaTexture
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.file_browser_save import FileBrowserSave

from brush import Brush
# from move_tool import MoveTool
# from eyedropper import Eyedropper
from palette import Palette
from layer import Layer
from layer_menu import LayerMenu
try:
    from PIL import ImageGrab   # windows only
except:
    pass

# window.vsync = False
window.show_ursina_splash = False
input_handler.bind('x', '-')
input_handler.bind('d', '+')
Button.color = color.color(0,0,0,.9)


class Otoblop(Entity):
    def __init__(self):
        super().__init__()

        camera.orthographic = True
        camera.fov = 100
        window.color = color.white
        self.cursor = Cursor(model=Circle(mode='line'))

        self.canvas_width = 1920
        self.canvas_height = 1080
        # self.layer = Layer(512, 512)
        # self.layer = Layer(self.canvas_width, self.canvas_height)
        # self.layer_2 = Layer(self.canvas_width, self.canvas_height, z=-1)
        # self.layers = [self.layer, self.layer_2]
        self.layers = list()
        self.layer_index = -1
        self.add_layer()
        self.add_layer()
        # self.layer_menu = LayerMenu()
        # self.layer_menu.otoblop = self
        # self.layer_menu.add_layer()
        print('---', self.layers, self.layer_index)

        self.cover = Entity(parent=self.current_layer, z=-1)
        Entity(parent=self.cover, model='quad', color=color.dark_gray, origin_y=-.5, y=.5, scale=10)
        Entity(parent=self.cover, model='quad', color=color.dark_gray, origin_y=.5, y=-.5, scale=10)
        Entity(parent=self.cover, model='quad', color=color.dark_gray, origin_x=-.5, x=.5, scale=10)
        Entity(parent=self.cover, model='quad', color=color.dark_gray, origin_x=.5, x=-.5, scale=10)
        self.cover.world_parent = self


        # instantiate tools
        self.brush = Brush(parent=self)
        # self.move_tool = MoveTool(parent=self)
        # self.eyedropper = Eyedropper(parent=self)

        # self.tools = (self.brush, self.move_tool)
        self.active_tool = self.brush

        self.palette = Palette(self.brush)

        self.info_text = Text(
            position=window.top_left,
            text=dedent('''
                x:   reduce brush size
                d:   increase brush size
                r:   round brush
                p:   paint brush
                1-9: brush opacity
                '''),
            color=color.black
            )
        def enable_brush():
            self.brush.enabled = True
        def disable_brush():
            self.brush.enabled = False

        self.move_cursor = Cursor(enabled=False)
        Text(parent=self.move_cursor, text='move', enabled=False)

        self.file_browser = FileBrowser(file_types=('.png', ), enabled=False)
        self.file_browser.on_submit = self.open
        self.file_browser.on_enable = disable_brush
        self.file_browser.on_disable = enable_brush

        self.file_browser_save = FileBrowserSave(file_types=('.png', ), file_type='.png', enabled=False)
        self.file_browser_save.save_button.on_click = self.save
        self.file_browser_save.on_enable = disable_brush
        self.file_browser_save.on_disable = enable_brush


    @property
    def current_layer(self):
        if not self.layers:
            print('error, no layers!')
        return self.layers[self.layer_index]


    @property
    def layer_index(self):
        return self._layer_index

    @layer_index.setter
    def layer_index(self, value):
        for l in self.layers:
            l.collision = False

        self._layer_index = value
        self.layers[value].collision = True
        print('---', self.layers[value].collision)

        self.brush.temp_layer.parent = self.layers[value]


    def add_layer(self):
        self.layers.append(Layer(self.canvas_width, self.canvas_height))
        self.layer_index += 1

        for i, l in enumerate(self.layers):
            l.z = -i


    def input(self, key):
        # print('key:', key)
        if key == 'b':
            self.active_tool = self.brush

        if key == 'v':
            # self.active_tool = self.move_tool
            self.layers[1].x += 10
            print('moved layer')

        if key == 'alt':
            self.prev_tool = self.active_tool
            self.active_tool = eyedropper
            print('tyoo', self.active_tool)

        if key == 'alt up':
            self.active_tool = self.prev_tool

        if held_keys['control'] and key == 'o':
            print('open')
            self.file_browser.enabled = True

        if held_keys['control'] and key == 's':
            print('save')
            self.file_browser_save.enabled = True

        if held_keys['control'] and key == 'v':
            # paste
            image = ImageGrab.grabclipboard()
            if isinstance(image, PIL.BmpImagePlugin.DibImageFile):
                t = Image.new('RGBA', image.size)
                t.putdata(image.getdata())

                # print(img.size)
                reference_image = Entity(
                    model='quad',
                    scale = (image.size[0]/1080*90, image.size[1]/1080*90),
                    texture=Texture(t),
                    z=-1
                    )
                # fit to canvas
                relative_scale_y = reference_image.scale_y / self.layer.scale_y
                relative_scale_x = reference_image.scale_x / self.layer.scale_x
                relative_scale = max(relative_scale_y, relative_scale_x)

                if relative_scale > 1:
                    reference_image.scale /= relative_scale

        if key == '1':
            self.layer_index = 0
        if key == '2':
            self.layer_index = 1


    def save(self):
        file_name = self.file_browser_save.file_name_field.text_field.text
        if not file_name.endswith(self.file_browser_save.file_type):
            file_name += self.file_browser_save.file_type

        p = self.file_browser_save.path / file_name
        print('save:', p)
        if p.exists():
            print('overwrite', p.name, '?')
            # self.close
            return

        else:
            img = self.layer.img
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            # bgra to rgba
            img = img.convert("RGBA")
            data = np.array(img)
            red, green, blue, alpha = data.T
            data = np.array([blue, green, red, alpha])
            data = data.transpose()
            img = Image.fromarray(data)


            img.save(p, 'PNG')
            self.file_browser_save.enabled = False
            print('saved:', p)

    def open(self, path):
        print('||||||||||||', type(path), isinstance(path, (tuple, list)))
        if not isinstance(path, (tuple, list)):
            print('open file:', path)
            self.layer.img = Image.open(path)
            self.layer.texture._texture.setRamImage(otoblop.layer.img.tobytes())
        else:
            print('open file 2:', path[0])
            self.layer.img = Image.open(path[0])
            self.layer.texture._texture.setRamImage(otoblop.layer.img.tobytes())
        # TODO: open multiple



    @property
    def active_tool(self):
        return self._active_tool

    @active_tool.setter
    def active_tool(self, value):
        print('set active tool to:', value)
        for t in self.tools:
            if t is not value:
                t.enabled = False

        value.enabled = True
        self._active_tool = value


app = Ursina()
otoblop = Otoblop()
app.otoblop = otoblop
print('.....', sys.argv)
if len(sys.argv) > 1 and sys.argv[1].endswith('.png'):
    otoblop.open(sys.argv[1])

sys.modules['OTOBLOP'] = otoblop
import eyedropper
from color_sliders import ColorMenu
color_menu = ColorMenu()

otoblop.tools = (otoblop.brush, eyedropper)
otoblop.active_tool = otoblop.brush
# sys.modules['eyedropper'] = Eyedropper(parent=self)]
# from ursina.prefabs.dropdown_menu import DropdownMenu
# from ursina.prefabs.dropdown_menu import DropdownMenuButton as MenuButton
#
# DropdownMenu(
#     text = 'File',
#     buttons = (
#         MenuButton('New'),
#         MenuButton('Open'),
#         MenuButton('Save'),
#         MenuButton('Save as...'),
#         MenuButton('Settings'),
#         MenuButton('Exit', on_click='application.quit'),
#         )
# )


app.run()
