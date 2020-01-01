from ursina import *


class Eyedropper(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled = False

    def update(self):
        if held_keys['alt'] and mouse.left:
            if mouse.hovered_entity == self.parent.combined_layer:
                self.tex_x = int((mouse.point[0] + .5) * self.parent.canvas_width)
                self.tex_y = int((mouse.point[1] + .5) * self.parent.canvas_height)
                col = self.parent.combined_layer.img.getpixel((self.tex_x, self.tex_y))
                self.parent.brush.brush_color = color.rgb(col[2], col[1], col[0]) # bgr to rgb
                self.parent.cursor.color = self.parent.brush.brush_color
