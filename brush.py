from ursina import *
from PIL import Image, ImageChops, ImageEnhance



class Brush(Entity):
    def __init__(self):
        super().__init__()
        self.org_brush = Image.open('textures/' + 'brush.png').transpose(Image.FLIP_TOP_BOTTOM)
        # convert to brg color
        channels = self.org_brush.split()
        printvar(len(channels))
        if len(channels) == 3:
            self.org_brush = Image.merge("RGB", (channels[2], channels[1], channels[0]))
        else:
            self.org_brush = Image.merge("RGBA", (channels[2], channels[1], channels[0], channels[3]))
            self.org_mask = channels[3]
        self.brush = self.org_brush.copy()

        self.brush_color = color.white
        self.brush_opacity = 1  # must be set!
        self.prev_pos = None


    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, value):
        self._brush_color = value
        self.value = (
            int(value[2] * 255),
            int(value[1] * 255),
            int(value[0] * 255)
            )
        tint = Image.new("RGBA", (self.brush.width, self.brush.height), self.value)
        self.brush = ImageChops.multiply(self.org_brush, tint)

    @property
    def brush_opacity(self):
        return self._brush_opacity

    @brush_opacity.setter
    def brush_opacity(self, value):
        # alpha = 1
        try:
            # self.mask = self.org_brush.convert("L").point(lambda x: min(x, value * 256))
            # self.mask = channels[3]
            self.mask = ImageEnhance.Brightness(self.org_mask).enhance(value)
            print(self.mask)
            # self.brush.putalpha(mask)
        except:
            print('fail')


    def input(self, key):
        if key == 'left mouse up':
            self.prev_pos = None

        if key.isdigit():
            if key == '0':
                key = '10'
            self.brush_opacity = int(key) / 10


    def update(self, dt):
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
                    base.canvas.img.paste(
                        self.brush,
                        (int(pos_x - (self.brush.size[0] / 2)), int(pos_y - (self.brush.size[1] / 2))),
                        self.mask)
            else:
                # base.canvas.img = Image.alpha_composite(
                # base.canvas.img,
                # self.brush
                # )
                base.canvas.img.paste(
                    self.brush,
                    (int(self.tex_x - (self.brush.size[0] / 2)), int(self.tex_y - (self.brush.size[1] / 2))),
                    mask=self.mask)

            self.prev_pos = Vec3(self.tex_x, self.tex_y, 0)


# if __name__ == '__main__':
#     bg = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
#     brush = Image.open('textures/' + 'round_soft.png').transpose(Image.FLIP_TOP_BOTTOM)
#
#     value = color.green
#     value = (
#         int(value[2] * 255),
#         int(value[1] * 255),
#         int(value[0] * 255)
#         )
#     tint = Image.new("RGBA", (brush.width, brush.height), value)
#     brush = ImageChops.multiply(brush, tint)
#     # new = Image.alpha_composite(bg, brush)
#     # new.show()
#     bg.paste(
#         brush,
#         (int(0 - (brush.size[0] / 2)),
#         int(0 - (brush.size[1] / 2))),
#         brush)
#     bg.show()
