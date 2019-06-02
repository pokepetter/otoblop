from ursina import *
from PIL import Image, ImageChops, ImageEnhance
from panda3d.core import Texture as PandaTexture


class Brush(Entity):
    def __init__(self):
        super().__init__()
        self.i = 0
        # self.org_brush = Image.open("textures/" + "pokebrush_64.png").transpose(
        self.org_brush = Image.open("textures/" + "round.png").transpose(
            Image.FLIP_TOP_BOTTOM
        )
        # convert to brg color
        channels = self.org_brush.split()
        printvar(len(channels))
        if len(channels) == 3:
            self.org_brush = Image.merge(
                "RGBA", (channels[2], channels[1], channels[0], 255)
            )
        else:
            self.org_brush = Image.merge(
                "RGBA", (channels[2], channels[1], channels[0], channels[3])
            )

        self.brush = self.org_brush.copy()
        self.brush_color = color.black33
        self.opacity = 1
        # self.spacing = 64
        self.spacing = 3
        self.spacing = 10
        # self.spacing = 10     # bette default for round brush
        self.size = 1
        self.smoothing = .1
        mouse.visible=True

        self.temp_image = Image.new(
            "RGBA", (base.layer.width, base.layer.height), (0, 0, 0, 0)
        )
        self.temp_layer = Entity(
            # parent=base.layer, model="quad", z=-1, color=(1, 1, 1, .5)
            parent=base.layer, model="quad", z=-1, color=(1, 1, 1, self.opacity)
        )
        self.temp_texture = Texture(self.temp_image)
        self.temp_layer.texture = self.temp_texture

    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, value):
        self._brush_color = value
        self.value = (int(value[2] * 255), int(value[1] * 255), int(value[0] * 255))
        tint = Image.new("RGBA", (self.brush.width, self.brush.height), self.value)
        self.brush = ImageChops.multiply(self.org_brush, tint)
        self.size = self.size


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        size = (int(self.org_brush.width * value), int(self.org_brush.height * value))
        self.brush = self.org_brush.resize(size, Image.ANTIALIAS)

        # reapply tint
        color = (int(self.color[2] * 255), int(self.color[1] * 255), int(self.color[0] * 255))
        tint = Image.new("RGBA", (self.brush.width, self.brush.height), self.value)
        self.brush = ImageChops.multiply(self.brush, tint)
        print(value * self.brush.height, 'px')


    def input(self, key):
        if key == "left mouse down":
            self.temp_image = Image.new(
                "RGBA", (base.layer.width, base.layer.height), (0, 0, 0, 0)
            )
            self.temp_layer.visible = True
            self.last_drawn_point = self.get_layer_position()
            self.stamp(self.get_layer_position())

        if key == "left mouse up":
            # apply stroke
            self.temp_image = Image.alpha_composite(base.layer.img, self.temp_image)
            base.layer.img = Image.blend(base.layer.img, self.temp_image, alpha=self.opacity)

            self.temp_layer.visible = False
            self.temp_image = Image.new("RGBA", (base.layer.width, base.layer.height), (0, 0, 0, 0))
            # render layer
            base.layer.texture._texture.setRamImage(base.layer.img.tobytes())

        if key == "f":
            print(mouse.hovered_entity)
            # self.line_start = (int((mouse.point[0] + .5) * base.layer.width), int((mouse.point[1] + .5) * base.layer.height), 0)
        if key == "f up":
            print("draw line")
            # self.draw_line(self.line_start, (int((mouse.point[0] + .5) * base.layer.width), int((mouse.point[1] + .5) * base.layer.height), 0))

        if key.isdigit():
            if key == "0":
                key = "10"
            self.opacity = int(key) / 10
            self.temp_layer.color = color.color(0,0,1,self.opacity)
            printvar(self.opacity)

        if key == '+':
            self.size *= 1.2
        if key == '-':
            self.size /= 1.2

    def get_layer_position(self, smoothing=1):
        # returns pixel position
        # print(1)
        if mouse.hovered_entity == base.layer:
            pos = (mouse.point) + Vec3(.5, .5, 0)
            pos = (pos[0] * base.layer.width, pos[1] * base.layer.height)
            pos = (int(pos[0]), int(pos[1]), 0)
            if hasattr(self, 'prev_pos') and smoothing < 1:
                newpos = lerp(self.prev_pos, pos, smoothing)
                self.prev_pos = newpos
                return newpos

            self.prev_pos = pos
            return pos

    def stamp(self, position):
        if not position:
            return

        stamp_pos = (int(position[0] - (self.brush.size[0] / 2)), int(position[1] - (self.brush.size[1] / 2)))
        try:
            self.temp_image.alpha_composite(self.brush, stamp_pos)
        except:
            cropped_brush = self.brush.crop((
                -stamp_pos[0], -stamp_pos[1],
                self.brush.width, self.brush.height)
            )
            stamp_pos = (
                max(int(position[0] - cropped_brush.width), 0) // 10,
                max(int(position[1] - cropped_brush.height), 0) // 10
                )
            self.temp_image.alpha_composite(cropped_brush, stamp_pos)

        self.last_drawn_point = position


    def draw_line(self, start_pos, end_pos):
        amount = int(distance2d(start_pos, end_pos) / self.spacing / self.size)
        for i in range(1, amount):  # start at 1 to skip the first point
            position = lerp(start_pos, end_pos, i / amount)
            self.stamp(position)


    def update(self):
        self.i += time.dt
        if mouse.hovered_entity == base.layer and mouse.left and mouse.point:
            self.draw_line(self.last_drawn_point, self.get_layer_position(self.smoothing))

            # render temp texture
            if time.dt <= 1 / 240:
            # if self.i > 32:
                # self.temp_texture._texture.setRamImageAs(self.temp_image.tobytes(), "BGRA")
                self.temp_texture._texture.setRamImage(self.temp_image.tobytes())
                # self.temp_layer.texture = self.temp_texture
                self.i = 0
