from ursina import *
from layer import Layer
from copy import copy


class LayerButton(Draggable):
    def __init__(self, connected_layer, **kwargs):
        super().__init__()
        self.connected_layer = connected_layer
        self.text = 'layer'
        self.lock_x = True
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.origin_y = -.5
        self.z = -.1
        self.scale_y=.95
        self.text_entity.world_scale = 1
        self.text_entity.position = (-.5 + (.075*6), .5)

        self.eye = Button(parent=self, model='quad', position=(-.5+.075, .5, -1))
        self.eye.world_scale = .5
        self.eye.on_click = self.toggle_layer

        self.selected = False
        self.prev_index = 0

        self.thumbnail = Button(parent=self, model='quad', color=color.white, position=(-.5 + (.075*3), .5, -1))
        self.thumbnail.world_scale = self.world_scale_y
        self.thumbnail.world_scale_y /= self.parent.otoblop.canvas_width / self.parent.otoblop.canvas_height
        self.thumbnail.texture = self.connected_layer.texture
        self.thumbnail_outline = Entity(
            parent=self.thumbnail,
            model=copy(self.connected_layer.outline.model),
            color=color.light_gray
            )

    def toggle_layer(self):
        self.connected_layer.enabled = not self.connected_layer.enabled


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


    def on_click(self):
        for lb in self.parent.layer_buttons:
            lb.selected = False
        # select range
        if held_keys['shift'] and self.parent.selection:
            start, end = int(self.parent.selection[-1].y), int(self.y)
            if end < start:
                start, end = end, start

            # print('select range:', start, end)
            for i in range(start, end):
                self.parent.layer_buttons[i].selected = True

        self.selected = True
        self.parent.otoblop.layer_index = self.parent.layer_buttons.index(self)


    def drag(self):
        if not held_keys['control'] and not held_keys['shift']:
            for l in self.parent.selection:
                l.prev_index = int(l.y)
                l.dragging = True


    def drop(self):
        mouse.hold_duration = 0

        if abs(mouse.delta_drag[1]) < .05:
            if not held_keys['control'] and not held_keys['shift']:
                for l in self.parent.selection:
                    if not l == self:
                        l.selected = False
            return

        if len(self.parent.selection) == 1:
            lb = self.parent.selection[0]
            from_index = lb.prev_index
            to_index = round(self.parent.layer_move_indicator.y)
            if to_index > from_index:
                to_index -= 1

            self.parent.layer_buttons.pop(from_index)
            self.parent.layer_buttons.insert(to_index, lb)
            self.parent.otoblop.move_layer(from_index, to_index)
            self.parent.layer_move_indicator.enabled = False
            self.parent.otoblop.layer_index = to_index

        else:
            moved_layers = sorted(self.parent.selection, key=lambda x: x.prev_index)

            for i, l in enumerate(moved_layers):
                self.parent.layer_buttons.remove(l)

            layers_below = [l for l in self.parent.layer_buttons if l.y < self.parent.layer_move_indicator.y]
            layers_above = [l for l in self.parent.layer_buttons if not l in layers_below]
            self.parent.layer_buttons = layers_below + moved_layers + layers_above
            self.parent.sort_layer_buttons()

            for i, j in zip([l.prev_index for l in moved_layers], [int(l.y) for l in moved_layers]):
                print('move layer:', i, '->', j)
                self.parent.otoblop.move_layer(i, j)



    def update(self):
        if self.dragging:
            mouse.hold_duration += time.dt

        if mouse.hold_duration > .2:
            super().update()
            if self.dragging and abs(mouse.y-mouse.start_y) > .01:
                self.parent.layer_move_indicator.enabled = True

                for layer in self.parent.layer_buttons:
                    if layer == self:
                        continue

                    layers_beneath = [l for l in self.parent.layer_buttons if l.y < self.y]
                    if layers_beneath:
                        self.parent.layer_move_indicator.y = layers_beneath[-1].y + self.scale_y

                    if self.y < self.parent.layer_buttons[0].y:
                        self.parent.layer_move_indicator.y = self.parent.layer_buttons[0].y



class LayerMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent = camera.ui,
            scale = (.25, .05),
            position = (.5*camera.aspect_ratio - (.25/2) - .0025, -.45)
            )

        self.bg = Panel(parent=self, model='quad', scale_y=12, origin_y=-.5, color=color.dark_gray.tint(-.1))
        self.border = Entity(parent=self.bg, model=Quad(segments=0, mode='line'), origin_y=self.bg.origin_y, color=self.bg.color.tint(-.1))
        self.layer_buttons = list()
        self.selection = list()
        mouse.hold_duration = 0
        self.layer_move_indicator = Entity(
            parent=self, model='quad', color=color.orange, world_scale_y=.1, enabled=False, scale_x=1.05, z=-.2)

        for key, value in kwargs.items():
            setattr(self, key, value)


    def add_layer_button(self, y, layer):
        print('add layer at:', y)
        new_layer_button = LayerButton(layer, parent=self, text=f'layer_{len(self.layer_buttons)}')
        self.layer_buttons.insert(y, new_layer_button)
        return new_layer_button


    def sort_layer_buttons(self):
        self.layer_buttons.sort(key=lambda x : x.connected_layer.z, reverse=True)
        print('---', self.layer_buttons)
        for i, c in enumerate(self.layer_buttons):
            c.y = i
            c.text = str(i)

        self.layer_move_indicator.enabled = False


    def input(self, key):
        if held_keys['control'] and held_keys['shift'] and key == 'n':
            self.otoblop.add_layer()



if __name__ == '__main__':
    app = Ursina()
    Sprite('photoshop_ui', color=color.gray, z=1, scale=.8)
    layer_menu = LayerMenu()
    layer_menu.y = -.45
    layer_menu.x = .5*camera.aspect_ratio - (.25/2) - .0025
    from color_sliders import ColorMenu
    color_menu = ColorMenu()
    # color_menu.y=.35

    app.run()
