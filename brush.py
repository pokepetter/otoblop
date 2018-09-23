from ursina import *
from PIL import Image, ImageChops, ImageEnhance



class Brush(Entity):
    def __init__(self):
        super().__init__()
        self.org_brush = Image.open('textures/' + 'round_soft.png').transpose(Image.FLIP_TOP_BOTTOM)
        # convert to brg color
        channels = self.org_brush.split()
        printvar(len(channels))
        if len(channels) == 3:
            self.org_brush = Image.merge("RGBA", (channels[2], channels[1], channels[0], 255))
        else:
            self.org_brush = Image.merge("RGBA", (channels[2], channels[1], channels[0], channels[3]))

        self.brush = self.org_brush.copy()
        self.brush_color = color.black33
        self.prev_pos = None

        self.empty = Image.new("RGBA", (base.canvas.img.width, base.canvas.img.height), (255,0,0,128))
        self.temp_layer_entity = Entity(parent = base.canvas, model='quad', z=-1, color=(1,1,1,.5))
        self.temp_layer_buffer = Texture()
        self.temp_layer_buffer.setup2dTexture(self.empty.width, self.empty.height, Texture.TUnsignedByte, Texture.FRgba)
        self.temp_layer_buffer.setRamImageAs(self.empty.tobytes(), "RGBA")
        self.temp_layer_entity.texture = self.temp_layer_buffer


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
        if key == 'left mouse down':
            self.empty = Image.new("RGBA", (base.canvas.img.width, base.canvas.img.height), (0,0,0,0))
            self.temp_layer_entity.visible=True

        if key == 'left mouse up':
            self.prev_pos = None
            # apply stroke
            self.empty = Image.eval(self.empty, lambda x: x/2)
            base.canvas.img = Image.alpha_composite(base.canvas.img, self.empty)
            self.temp_layer_entity.visible=False
            # self.empty = Image.new("RGBA", (base.canvas.img.width, base.canvas.img.height), (0,0,0,0))

        if key.isdigit():
            if key == '0':
                key = '10'
            self.brush_opacity = int(key) / 10


    def update(self):
        if mouse.hovered_entity == base.canvas and mouse.left and mouse.point:
            self.tex_x = int((mouse.point[0] + .5) * base.canvas.width)
            self.tex_y = int((mouse.point[1] + .5) * base.canvas.height)
            self.prev_point = (self.tex_x, self.tex_y)

            # draw line between points
            if self.prev_pos:
                dist = distance(Vec3(self.prev_pos[0], self.prev_pos[1], 0), Vec3(self.tex_x, self.tex_y, 0))
                # printvar(dist)
                steps = int(dist / 5)
                for i in range(steps):
                    pos_x = lerp(self.prev_pos[0], self.tex_x, i / steps)
                    pos_y = lerp(self.prev_pos[1], self.tex_y, i / steps)
                    self.empty.alpha_composite(
                        self.brush,
                        (int(self.tex_x - (self.brush.size[0] / 2)), int(self.tex_y - (self.brush.size[1] / 2)))
                    )
            # else:
            #     self.empty = Image.new("RGBA", (base.canvas.img.width, base.canvas.img.height), (0,0,0,0))
            #     self.empty.alpha_composite(
            #         self.brush,
            #         (int(self.tex_x - (self.brush.size[0] / 2)), int(self.tex_y - (self.brush.size[1] / 2)))
            #     )
                # base.canvas.img.alpha_composite(self.empty)

            self.prev_pos = Vec3(self.tex_x, self.tex_y, 0)

            # update temp layer
            # b = self.empty.tobytes()
            self.temp_layer_buffer.setRamImageAs(self.empty.tobytes(), "RGBA")
            # self.temp_layer_buffer.setRamImage(b)
            self.temp_layer_entity.texture = self.temp_layer_buffer
