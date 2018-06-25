from ursina import *
from PIL import Image, ImageChops



class Brush(Entity):
    def __init__(self):
        super().__init__()
        self.org_brush = Image.open('textures/' + 'round_pixelated.png').transpose(Image.FLIP_TOP_BOTTOM)
        self.brush = self.org_brush.copy()
        self.brush_color = color.lime
        self.prev_pos = None


    @property
    def brush_color(self):
        return self._brush_color

    @brush_color.setter
    def brush_color(self, value):
        self._brush_color = value
        # self.brush_color = value
        self.value = (
            int(value[0] * 255),
            int(value[1] * 255),
            int(value[2] * 255)
            )
        tint = Image.new("RGBA", (self.brush.width, self.brush.height), self.value)
        self.brush = ImageChops.multiply(self.org_brush, tint)


    def input(self, key):
        if key == 'left mouse up':
            self.prev_pos = None


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
                        (int(pos_x - (self.brush.size[0] / 2)),
                        int(pos_y - (self.brush.size[1] / 2))),
                        self.brush)
            else:
                base.canvas.img.paste(
                    self.brush,
                    (int(self.tex_x - (self.brush.size[0] / 2)),
                    int(self.tex_y - (self.brush.size[1] / 2))),
                    self.brush)

            self.prev_pos = Vec3(self.tex_x, self.tex_y, 0)
