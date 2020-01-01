from ursina import *
from PIL import Image, ImageChops, ImageEnhance
from panda3d.core import Texture as PandaTexture


class Brush(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.i = 0
        self._delta_times = (0,0,0,0)

        self.brush = 'round'
        self.brush_color = color.black
        self.opacity = 1
        self.spacing = 2
        # self.spacing = 6     # better default for round brush
        # self.spacing = 25     # better default for round brush
        self.size = 1
        # self.size = .05
        # self.smoothing = .1
        self.smoothing = 1
        mouse.visible = True


    @property
    def brush(self):
        return self._brush

    @brush.setter
    def brush(self, value):
        # self.org_brush = Image.open('textures/' + 'pokebrush_64.png').transpose(
        self.org_brush = Image.open(f'textures/{value}.png').transpose(Image.FLIP_TOP_BOTTOM)
        # convert to brg color
        channels = self.org_brush.split()
        if len(channels) == 3:
            self.org_brush = Image.merge('RGBA', (channels[2], channels[1], channels[0], 255))
        else:
            self.org_brush = Image.merge('RGBA', (channels[2], channels[1], channels[0], channels[3]))

        self._brush = self.org_brush.copy()
        self.brush_color = self.brush_color

    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, value):
        self._brush_color = value
        self.value = (int(value[2] * 255), int(value[1] * 255), int(value[0] * 255))
        tint = Image.new('RGBA', (self.brush.width, self.brush.height), self.value)
        self._brush = ImageChops.multiply(self.org_brush, tint)
        self.size = self.size


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        size = (int(self.org_brush.width * value), int(self.org_brush.height * value))
        self._brush = self.org_brush.resize(size, Image.ANTIALIAS)

        # reapply tint
        color = (int(self.color[2] * 255), int(self.color[1] * 255), int(self.color[0] * 255))
        tint = Image.new('RGBA', (self.brush.width, self.brush.height), self.value)
        self._brush = ImageChops.multiply(self.brush, tint)
        # print(value * self.brush.height, 'px')
        self.parent.cursor.scale = value / 20


    def input(self, key):
        if key == 'left mouse down':
            self.parent.temp_image = Image.new(
                'RGBA', (self.parent.canvas_width, self.parent.canvas_height), (0, 0, 0, 0)
            )
            self.parent.temp_layer.visible = True
            self.last_drawn_point = self.get_layer_position()
            self.stamp(self.get_layer_position())
            self.original_size = self.size

        if key == 'left mouse up':
            # apply stroke
            self.parent.temp_image = Image.alpha_composite(self.parent.current_layer.img, self.parent.temp_image)
            self.parent.current_layer.img = Image.blend(self.parent.current_layer.img, self.parent.temp_image, alpha=self.opacity)

            self.parent.temp_layer.visible = False
            self.parent.temp_image = Image.new('RGBA', (self.parent.canvas_width, self.parent.canvas_height), (0, 0, 0, 0))
            # render layer
            self.parent.current_layer.texture._texture.setRamImage(self.parent.current_layer.img.tobytes())
            self.size = self.original_size

        if key == 'f':
            print(mouse.hovered_entity)
            # self.line_start = (int((mouse.point[0] + .5) * self.parent.layer.width), int((mouse.point[1] + .5) * self.parent.layer.height), 0)
        if key == 'f up':
            print('draw line')
            # self.draw_line(self.line_start, (int((mouse.point[0] + .5) * self.parent.layer.width), int((mouse.point[1] + .5) * self.parent.layer.height), 0))

        if key.isdigit():
            if key == '0':
                key = '10'
            self.opacity = int(key) / 10
            self.parent.temp_layer.color = color.color(0,0,1,self.opacity)
            printvar(self.opacity)

        if key in ('+', '+ hold') or key == 'scroll up' and mouse.left:
            self.size *= 1.2
        if key in ('-', '- hold') or key == 'scroll down' and mouse.left:
            self.size /= 1.2

        if key == 'r':
            self.brush = 'round'
            # self.spacing = 6
        if key == 'p':
            self.brush = 'pokebrush_64'
            # self.spacing = 2
        if key == 'arrow right':
            self.spacing += 1
        if key == 'arrow left':
            self.spacing -= 1
            self.spacing = max(0, self.spacing)


    def get_layer_position(self, smoothing=1):
        # returns pixel position
        # print(1)
        # print(mouse.hovered_entity, self.parent.current_layer)
        if mouse.hovered_entity == self.parent.current_layer:
            pos = (mouse.point) + Vec3(.5, .5, 0)
            pos = (pos[0] * self.parent.canvas_width, pos[1] * self.parent.canvas_height)
            pos = (int(pos[0]), int(pos[1]), 0)
            # print(pos)
            if hasattr(self, 'prev_pos') and smoothing < 1:
                newpos = lerp(self.prev_pos, pos, smoothing)
                self.prev_pos = newpos
                return newpos

            self.prev_pos = pos
            return pos

        return None

    def stamp(self, position):
        if not position:
            return

        stamp_pos = (int(position[0] - (self.brush.size[0] / 2)), int(position[1] - (self.brush.size[1] / 2)))
        try:
            self.parent.temp_image.alpha_composite(self.brush, stamp_pos)
        except:
            cropped_brush = self._brush.crop((
                -stamp_pos[0], -stamp_pos[1],
                self.brush.width, self.brush.height)
            )
            stamp_pos = (
                max(int(position[0] - cropped_brush.width), 0) // 10,
                max(int(position[1] - cropped_brush.height), 0) // 10
                )
            self.parent.temp_image.alpha_composite(cropped_brush, stamp_pos)

        self.last_drawn_point = position


    def draw_line(self, start_pos, end_pos):
        amount = int(distance2d(start_pos, end_pos) / self.spacing / self.size)
        for i in range(1, amount):  # start at 1 to skip the first point
            position = lerp(start_pos, end_pos, i / amount)
            self.stamp(position)


    def update(self):

        self.i += time.dt
        if mouse.hovered_entity == self.parent.current_layer and mouse.left and mouse.point and self.last_drawn_point != None:
            self.draw_line(self.last_drawn_point, self.get_layer_position(self.smoothing))

            # render temp texture
            # if time.dt <= 1 / 240 / 1.95:
            self._delta_times = self._delta_times[:3] + (time.dt,)
            # print(self._delta_times)

            # if sum(self._delta_times) <= .03:
            # if sum(mouse.velocity) < .005:
            # if self.i > 32:
            self.parent.temp_texture._texture.setRamImage(self.parent.temp_image.tobytes())
            self.i = 0
