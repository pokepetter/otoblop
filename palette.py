from ursina import *
from ursina.color import *

class Palette(Entity):
    def __init__(self):
        super().__init__()
        self.parent = camera.ui
        self.position = (.4, .4)
        self.colors = (
            red, orange, yellow, lime,
            green, turquoise, cyan, azure,
            blue, violet, magenta, pink

            )

        for c in self.colors:
            e = PaletteButton(
                parent = self,
                color = c,
                )

        self.add_script('grid_layout')
        self.grid_layout.update_grid()
        self.scale *= .05


class PaletteButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height_color = self.color

    def on_click(self):
        base.brush.brush_color = self.color
