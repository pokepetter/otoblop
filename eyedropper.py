from ursina import *

class Eyedropper(Entity):

    def update(self):
        # if mouse.left and self. pressure < 2:
        #     self.pressure += .1
        if mouse.left:
            print('pick color')
            if mouse.hovered_entity == base.layer:
                self.tex_x = int((mouse.point[0] + .5) * base.layer.width)
                self.tex_y = int((mouse.point[1] + .5) * base.layer.height)
                base.brush.brush_color = base.layer.img.getpixel((self.tex_x, self.tex_y))
                base.cursor.color = base.brush.brush_color

            elif mouse.hovered_entity:
                base.brush.brush_color = mouse.hovered_entity.color

            else:
                base.brush.brush_color = window.color
            return
