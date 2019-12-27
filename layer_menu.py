from ursina import *
from layer import Layer


class LayerButton(Draggable):
    def __init__(self, **kwargs):
        super().__init__()
        self.text = 'layer'
        self.lock_x = True
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.z = -.1
        self.scale_y=.95
        self.text_entity.world_scale = 1
        self.text_entity.position = (-.5 + (.075*5), .5)

        self.eye = Button(parent=self, model='quad', position=(-.5+.075, .5, -1), color=color.olive)
        self.eye.world_scale = .5
        self.eye.on_click = 'self.color = self.color.invert()'

        self.selected = False
        self.prev_index = 0

        self.debug_square = Entity(parent=camera.ui, model='quad', scale=.2, x=-.2, color=color.azure)
        # self.thumbnail = Button(parent=self, model='quad', color=color.azure, position=(-.5 + (.075*3), .5, -1))
        # self.thumbnail.world_scale = self.world_scale_y * 1
        # self.parent = render
        # self.scale = ()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value == True:
            self.color = color.cyan.tint(-.3)
            if not self in self.parent.selection:
                self.parent.selection.append(self)
        else:
            self.color = Button.color
            if self in self.parent.selection:
                self.parent.selection.remove(self)


    def input(self, key):
        super().input(key)
        if key == 'left mouse down' and mouse.hovered_entity not in self.parent.layers:
            self.selected = False


    def on_click(self):
        if not self.selected and not held_keys['control'] and not held_keys['shift']:
            for layer in self.parent.selection:
                layer.selected = False


        # select range
        if held_keys['shift'] and self.parent.selection:
            start, end = int(self.parent.selection[-1].y), int(self.y)
            if end < start:
                start, end = end, start

            # print('select range:', start, end)
            for i in range(start, end):
                self.parent.layers[i].selected = True

        self.selected = True


    def drag(self):
        if not held_keys['control'] and not held_keys['shift']:
            for l in self.parent.selection:
                l.prev_index = int(l.y)
                l.dragging = True

        # print('move layer from:', self.original_index)

    def drop(self):

        if abs(mouse.delta_drag[1]) < .05:
            if not held_keys['control'] and not held_keys['shift']:
                for l in self.parent.selection:
                    if not l == self:
                        l.selected = False

            self.parent.render()
            return

        moved_layers = sorted(self.parent.selection, key=lambda x: x.prev_index)

        for i, l in enumerate(moved_layers):
            self.parent.layers.remove(l)

        layers_below = [l for l in self.parent.layers if l.y < self.parent.layer_move_indicator.y]
        layers_above = [l for l in self.parent.layers if not l in layers_below]
        self.parent.layers = layers_below + moved_layers + layers_above
        self.parent.render()

        for i, j in zip([int(l.y) for l in moved_layers], [l.prev_index for l in moved_layers]):
            print('move:', i, '->', j)


    def update(self):
        super().update()
        if self.dragging and abs(mouse.y-mouse.start_y) > .01:
            self.parent.layer_move_indicator.enabled = True

            for layer in self.parent.layers:
                if layer == self:
                    continue

                layers_beneath = [l for l in self.parent.layers if l.y < self.y]
                if layers_beneath:
                    self.parent.layer_move_indicator.y = layers_beneath[-1].y + self.scale_y

                if self.y < self.parent.layers[0].y:
                    self.parent.layer_move_indicator.y = self.parent.layers[0].y


class LayerMenu(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            scale = (.3, .05),
            position = (.5, -.4)
            )

        self.bg = Panel(parent=self, model='quad', scale_y=12, origin_y=-.5)
        self.layer_buttons = list()
        self.selection = list()
        self.layer_move_indicator = Entity(
            parent=self, model='quad', color=color.orange, world_scale_y=.1, enabled=False, scale_x=1.05, z=-.2)



    def render(self):
        for i, c in enumerate(self.layer_buttons):
            c.y = i

        self.layer_move_indicator.enabled = False


    def input(self, key):
        if held_keys['control'] and held_keys['shift'] and key == 'n':
            print('add layer')



if __name__ == '__main__':
    app = Ursina()
    # lm = LayerMenu()
    window.position += Vec2(100,0)
    def input(key):
        if key == '+':
            lm.add_layer_button()
        if key == '-':
            lm.remove_layer_button()
    app.run()
