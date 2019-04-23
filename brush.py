from ursina import *
from PIL import Image, ImageChops, ImageEnhance
from panda3d.core import Texture as PandaTexture


class Brush(Entity):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.org_brush = Image.open("textures/" + "pokebrush_64.png").transpose(
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
        # self.spacing = 64
        self.spacing = 2

        self.temp_image = Image.new(
            "RGBA", (base.canvas.width, base.canvas.height), (0, 0, 0, 0)
        )
        self.temp_layer = Entity(
            # parent=base.canvas, model="quad", z=-1, color=(1, 1, 1, .5)
            parent=base.canvas, model="quad", z=-1, color=(1, 1, 1, 1)
        )
        self.temp_texture = Texture(self.temp_image)
        self.temp_layer.texture = self.temp_texture

    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, value):
        self._brush_color = value
        self.value = (
            int(value[2] * 255),
            int(value[1] * 255),
            int(value[0] * 255),
            # int(value[3] * 255)
        )
        tint = Image.new("RGBA", (self.brush.width, self.brush.height), self.value)
        self.brush = ImageChops.multiply(self.org_brush, tint)

    def input(self, key):
        if key == "left mouse down":
            self.temp_image = Image.new(
                "RGBA", (base.canvas.width, base.canvas.height), (0, 0, 0, 0)
            )
            self.temp_layer.visible = True
            self.stamp(self.get_canvas_position())

        if key == "left mouse up":
            # apply stroke
            # self.temp_image = Image.eval(self.temp_image, lambda x: x / 2)
            self.temp_image = Image.eval(self.temp_image, lambda x: x / 1)
            base.canvas.current_layer._cached_image = Image.alpha_composite(base.canvas.current_layer._cached_image, self.temp_image)
            self.temp_layer.visible = False
            self.temp_image = Image.new(
                "RGBA", (base.canvas.width, base.canvas.height), (0, 0, 0, 0)
            )

        if key == "f":
            print(mouse.hovered_entity)
            # self.line_start = (int((mouse.point[0] + .5) * base.canvas.width), int((mouse.point[1] + .5) * base.canvas.height), 0)
        if key == "f up":
            print("draw line")
            # self.draw_line(self.line_start, (int((mouse.point[0] + .5) * base.canvas.width), int((mouse.point[1] + .5) * base.canvas.height), 0))

        if key.isdigit():
            if key == "0":
                key = "10"
            self.brush_color[3] = int(key) / 10

    def get_canvas_position(self):
        # returns pixel position
        if mouse.hovered_entity == base.canvas.bg:
            pos = (mouse.point * 10) + Vec3(.5, .5, 0)
            pos = (pos[0] * base.canvas.width, pos[1] * base.canvas.height)
            pos = (int(pos[0]), int(pos[1]), 0)
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
        amount = int(distance(start_pos, end_pos) / self.spacing)
        for i in range(1, amount):  # start at 1 to skip the first point
            position = lerp(start_pos, end_pos, i / amount)
            self.stamp(position)

        # self.temp_texture.setRamImageAs(self.temp_image.tobytes(), "RGBA")
        # self.temp_layer.texture = self.temp_texture

    def update(self):
        # self.i += 1
        if mouse.hovered_entity == base.canvas.bg and mouse.left and mouse.point:
            self.draw_line(
                self.last_drawn_point,
                self.get_canvas_position(),
            )

            if time.dt <= 1 / 60:
                self.temp_texture._texture.setRamImageAs(
                    self.temp_image.tobytes(), "BGRA"
                )
                self.temp_layer.texture = self.temp_texture
                self.i = 0
