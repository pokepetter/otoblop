from ursina import *
from PIL import Image, ImageChops



class Layer(Entity):
    def __init__(self, width=1024, height=1024, col=color.clear, **kwargs):
        super().__init__(**kwargs)
        self.scale = (90, 90)
        self.model = 'quad'
        self.collider = BoxCollider(self, size=(10,10,.1))  # make a click area bigger than the layer to be able to click outside and still draw.
        self.layer_button = None

        self.i = 0
        self.width = width
        self.height = height
        self.scale_x *= width / height

        self.outline = Entity(
            parent=self,
            model=Mesh(vertices=[(-.5,-.5,0), (.5,-.5,0), (.5,.5,0), (-.5,.5,0)], triangles=[(0,1,2,3,0),], mode='line'),
            z=-.2,
            color=color.cyan,
            )

        col = tuple(int(e*255) for e in col)
        self.img = Image.new('RGBA', (width, height), col)
        self.texture = Texture(self.img)
        self.texture.filtering = None



    def input(self, key):
        # if key == 'left mouse down':
        #     self.undo_img = self.img.copy()

        if key == 'scroll up' and not mouse.left and held_keys['alt']:
            camera.fov /= 1.1
            camera.fov = max(camera.fov, 0)
            print(camera.fov)

        if key == 'scroll down' and not mouse.left and held_keys['alt']:
            prev_cam_fov = camera.fov
            camera.fov *= 1.1
            camera.fov = min(camera.fov, 300)
            print(camera.fov)
            if prev_cam_fov < 200 and camera. fov >= 200:
                print('mipmap level:', 2)
                self.mipmap = 2


        if held_keys['control'] and key == '0':
            camera.fov = 100





        # if held_keys['control'] and key == 'z':
        #     # print('undo')
        #     if self.undo_img:
        #         self.img = self.undo_img
        #         self.texture._texture.setRamImage(self.img.tobytes())

        # if key == '-' and self.h > 0:
        #     self.h -= 1
        #     self.layers[self.history[self.h][1]] = self.history[self.h][0]
        # if key == '+' and self.h < len(self.history)-1:
        #     self.h += 1
        #     self.layers[self.history[self.h][1]] = self.history[self.h][0]

            # self.current_layer._cached_image = self.undo_img
            # b = self.current_layer._cached_image.tobytes()
            # self.texture._texture.setRamImage(b)


    def update(self):
        if held_keys['space']:
            camera.x -= mouse.velocity[0] * 10
            camera.y -= mouse.velocity[1] * 10

        # self.i += 1
        # if self.i > 100 and self.texture:  # update image less often to reduce lag.
        #     b = self.img.tobytes()
        #     self.texture._texture.setRamImage(b)
        #     self.i = 0
