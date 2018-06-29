from ursina import *
from PIL import Image, ImageChops
# import opencv-python as ocv
import numpy
import time
from brush import Brush
from eyedropper import Eyedropper
from palette import Palette

def premultiply_alpha(img):
    # fake transparent image to blend with
    transparent = Image.new("RGBA", img.size, (0, 0, 0, 0))
    # blend with transparent image using own alpha
    return Image.composite(img, transparent, img)

class Otoblop(Ursina):
    def __init__(self):
        super().__init__()

        camera.orthographic = True
        camera.fov = 16
        window.color = color.gray
        self.cursor = Cursor()

        self.canvas = Canvas(2048, 1024)

        # instantiate tools
        self.brush = Brush()
        self.eyedropper = Eyedropper()
        self.tools = (
            self.brush,
            self.eyedropper,
            )
        self.active_tool = self.brush

        self.palette = Palette()


    def input(self, key):
        super().input(key)
        if key == 'b':
            self.active_tool = self.brush

        if key == 'alt':
            self.prev_tool = self.active_tool
            self.active_tool = self.eyedropper
            print('tyoo', self.active_tool)

        if key == 'alt up':
            self.active_tool = self.prev_tool


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



class Canvas(Entity):
    def __init__(self, width=1024, height=1024, color=color.white):
        super().__init__()
        self.scale *= 7
        self.model = 'quad'
        self.collider = 'box'

        self.i = 0
        # self.pressure = .1
        self.width = width
        self.height = height
        self.scale_x *= width/height

        self.img = Image.new('RGBA', (width, height), (255, 255, 255))

        self.texture_buffer = Texture()
        self.texture_buffer.setup2dTexture(width, height, Texture.TUnsignedByte, Texture.FRgba)
        self.texture_buffer.setRamImageAs(self.img.tobytes(), "RGBA")
        self.texture = self.texture_buffer
        self.texture.setRamImageAs(self.img.tobytes(), "RGBA")


    def input(self, key):
        if key == 'left mouse down':
            self.undo_img = self.img.copy()

        if key == 'scroll up':
            camera.fov -= 1
            camera.fov = max(camera.fov, 0)

        if key == 'scroll down':
            camera.fov += 1
            camera.fov = min(camera.fov, 200)

        if held_keys['control'] and key == 'z':
            # print('undo')
            if self.undo_img:
                self.img = self.undo_img
                b = self.img.tobytes()
                self.texture_buffer.setRamImage(b)
                self.texture = self.texture_buffer


    def update(self, dt):

        if held_keys['space']:
            camera.x -= mouse.velocity[0] * 10
            camera.y -= mouse.velocity[1] * 10



        self.i += 1
        if self.i > 2:  # update image less often to reduce lag.
            b = self.img.tobytes()
            self.texture_buffer.setRamImage(b)
            self.texture = self.texture_buffer
            self.i = 0

app = Otoblop()
app.run()
