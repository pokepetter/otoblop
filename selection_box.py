from ursina import *
from enum import Enum


class SelectionMode(Enum):
    new_selection = ''
    add = '+'
    subtract = '-'


class SelectionBox(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.box = Draggable(
            parent=camera.ui,
            model=Quad(0, mode='line'),
            color=color.color(0,0,1,1),
            origin=(-.5,-.5,0),
            scale = (0,0,1),
            )

        self.dragging = False

        self.selection = list()
        self.mode = SelectionMode.new_selection
        self.square_selection = False

        self.tooltip = Text()


    def input(self, key):
        if key == 'left mouse down' and not self.box.hovered:
            if self.mode == SelectionMode.new_selection:
                self.clear_selection()

            self.box.position = mouse.position
            self.box.enabled = True
            self.dragging = True
            self.square_selection = False

        if key == 'left mouse up':
            self.dragging = False

            if self.mode in (SelectionMode.new_selection, SelectionMode.add):    # add to selection
                # self.selection.append((self.box.position, mouse.position))
                self.selection.append(Entity(
                    parent=camera.ui, model='quad', origin=self.box.origin, position=self.box.position,
                    scale=self.box.scale, color=color.color(120,.5,1,.3), double_sided=True))

            elif self.mode == SelectionMode.subtract:
                self.selection.append(Entity(
                    parent=camera.ui, model='quad', origin=self.box.origin, position=self.box.position,
                    scale=self.box.scale, color=color.color(0,.5,1,.3), double_sided=True))
                print('subtract!')

            self.box.enabled = False
            self.square_selection = True


        if self.dragging and key == 'shift':
            self.square_selection = True
        if key == 'shift up':
            self.square_selection = False


    def clear_selection(self):
        print('clear')
        # self.selection.clear()
        for e in self.selection:
            destroy(e)

    def update(self):
        if not mouse.left:
            if not held_keys['shift'] and not held_keys['alt']:
                self.mode = SelectionMode.new_selection
            elif held_keys['shift'] and not held_keys['alt']:
                self.mode = SelectionMode.add
            elif not held_keys['shift'] and held_keys['alt']:
                self.mode = SelectionMode.subtract

        self.tooltip.text = self.mode.value
        self.tooltip.position = mouse.position

        if self.dragging:
            self.box.scale_x = mouse.x - self.box.x
            self.box.scale_y = mouse.y - self.box.y

            if self.square_selection:
                target_scale = max(abs(self.box.scale_x), abs(self.box.scale_y))
                if self.box.scale_x >= 0:
                    self.box.scale_x = target_scale
                else:
                    self.box.scale_x = -target_scale

                if self.box.scale_y >= 0:
                    self.box.scale_y = target_scale
                else:
                    self.box.scale_y = -target_scale



if __name__ == '__main__':
    app = Ursina()
    SelectionBox()
    app.run()
