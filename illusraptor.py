from ursina import *


app = Ursina()
camera.orthographic = True
camera.fov = 1
bg = Entity(model='quad', collider='box', color=color.black, scale=10)

app.line = None
app.rect = None
helper = Entity()
helper_2 = Entity()


def input(key):
    if bg.hovered and key == 'left mouse down':
        if not app.line:
            app.line = Entity(model='quad', origin_y=-.5, scale=.1, position=mouse.position)
        else:
            app.line = None

    elif bg.hovered and key == 'r':
        if not app.rect:
            app.rect = Entity(model='quad', origin=(-.5,-.5), position=mouse.position, scale=.05, double_sided=True, height_found=False)
        elif not app.rect.height_found:
            app.rect.height_found = True
            helper.position = app.rect.position + (app.rect.up * app.rect.scale_y)
            helper.rotation_z = app.rect.rotation_z
        else:
            app.rect = None


def update():
    if app.line:
        app.line.look_at_2d(mouse.position)
        app.line.scale_y = distance_2d(app.line, mouse.position)

    if app.rect:
        if not app.rect.height_found:
            app.rect.look_at_2d(mouse.position)
            app.rect.scale_y = distance_2d(app.rect, mouse.position)
        else:
            helper_2.parent = helper
            helper_2.world_position = mouse.position
            helper_2.y = 0
            if abs(helper_2.x) > .001:
                dist = helper_2.x
                helper_2.parent = scene
                app.rect.scale_x = dist


app.run()
