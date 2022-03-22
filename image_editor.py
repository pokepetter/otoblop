from ursina import *
from PIL import ImageGrab



app = Ursina(borderless=False, current_tool=None)
camera.orthographic = True
camera.fov = 1.5

canvas = Entity(model='quad', scale_x=16/9)
# canvas.shadow = Entity(parent=canvas, model='quad', color='#111133', z=.01)
# canvas.shadow.world_position += Vec3(.01,-.01,0)

shortcuts = {'v':'move', 'm':'box_select', 'l':'lasso_tool'}

EditorCamera(zoom_speed=.1, zoom_smoothing=.1, rotation_speed=0)

def input(key):
    if held_keys['control'] and key == 'v':
        img = ImageGrab.grabclipboard()
        print('paste image:', img)
        if img:
            tex = Texture(img)
            print(tex.width / tex.height)
            layer = Draggable(parent=scene, model='quad', texture=tex, lock=(0,0,1), z=-1, color=color.white, highlight_color=color.white)
            print(layer)

    if key in shortcuts and not held_keys['control'] and not held_keys['shift'] and not held_keys['alt']:
        app.current_tool = shortcuts[key]
        print('change tool to:', app.current_tool)







app.run()
