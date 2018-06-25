from ursina import *

class Eyedropper(Entity):

    def update(self, dt):
        # if mouse.left and self. pressure < 2:
        #     self.pressure += .1
        if mouse.left:
            print('pick color')
            if mouse.hovered_entity == base.canvas:
                self.tex_x = int((mouse.point[0] + .5) * base.canvas.width)
                self.tex_y = int((mouse.point[1] + .5) * base.canvas.height)
                base.brush.brush_color = base.canvas.img.getpixel((self.tex_x, self.tex_y))
                base.cursor.color = base.brush.brush_color

            elif mouse.hovered_entity:
                base.brush.brush_color = mouse.hovered_entity.color

            else:
                base.brush.brush_color = window.color
            return
