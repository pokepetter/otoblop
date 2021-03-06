from ursina import *



class Palette(Entity):
    def __init__(self, brush):
        super().__init__()
        self.parent = camera.ui
        self.position = (.4, .4)

        self.brush = brush
        # self.colors = (
        #     black, dark_gray, gray, light_gray, white,
        #     red, orange, yellow, lime,
        #     green, turquoise, cyan, azure,
        #     blue, violet, magenta, pink
        #
        #     )

        for key, value in color.colors.items():
            e = PaletteButton(
                parent = self,
                color = value,
                highlight_color = value,
                tooltip = Tooltip(key),
                )

        grid_layout(self.children)
        self.scale *= .05


class PaletteButton(Button):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.highlight_color = self.color

    def on_click(self):
        print(self.parent.brush)
        self.parent.brush.brush_color = self.color
