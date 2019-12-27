from ursina import *
import OTOBLOP

class Eyedropper(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled = False

    def update(self):
        # if mouse.left and self. pressure < 2:
        #     self.pressure += .1
        if mouse.left:
            # print('pick color')
            if mouse.hovered_entity == OTOBLOP.current_layer:
                self.tex_x = int((mouse.point[0] + .5) * OTOBLOP.canvas_width)
                self.tex_y = int((mouse.point[1] + .5) * OTOBLOP.canvas_height)
                col = OTOBLOP.layer.img.getpixel((self.tex_x, self.tex_y))
                OTOBLOP.brush.brush_color = color.rgb(col[2], col[1], col[0]) # bgr to rgb
                OTOBLOP.cursor.color = OTOBLOP.brush.brush_color

            elif mouse.hovered_entity and not mouse.hovered_entity.color == color.clear:
                OTOBLOP.brush.brush_color = mouse.hovered_entity.color[:3]
                print('selected color:', OTOBLOP.brush.brush_color)

            else:
                OTOBLOP.brush.brush_color = window.color
            return


sys.modules['eyedropper'] = Eyedropper()
