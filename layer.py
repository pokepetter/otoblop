from ursina import *
from PIL import Image, ImageChops



class Layer(Entity):
    def __init__(self, width=1024, height=1024, col=color.clear, **kwargs):
        super().__init__(**kwargs)
        self.scale = (90, 90)
        self.model = 'quad'
        self.collider = BoxCollider(self, size=(10,10,.1))
        # self.collider = 'box'
        # make a click area bigger than the layer to be able to click outside and still draw.
        # self.bg = Entity(parent=self, z=1, collider='box', scale=(10, 10))

        self.i = 0
        # self.pressure = .1
        self.width = width
        self.height = height
        self.scale_x *= width / height

        self.outline = Entity(
            parent=self,
            model=Mesh(vertices=[(-.5,-.5,0), (.5,-.5,0), (.5,.5,0), (-.5,.5,0)], triangles=[(0,1,2,3,0),], mode='line'),
            z=-.2,
            color=color.cyan,
            # scale=(1/self.scale_x, 1/self.scale_y)
            )

        # self.subsections = list()
        # for y in range(2):
        #     for x in range(2):
        #         self.subsections.append(
        #             Entity(
        #                 parent = self,
        #                 model = 'quad',
        #                 color = color.blue,
        #                 scale = .5,
        #
        #                 )
        #
        #         )
        #

        col = tuple(int(e*255) for e in col)
        self.img = Image.new('RGBA', (width, height), col)
        self.texture = Texture(self.img)
        # self.texture.filtering = 'mipmap'
        self.texture.filtering = None


        self.mipmap = 1
        # self.temp_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        # self.temp_layer = Entity(parent=self, model='quad', z=-1, color=(1, 1, 1, 1))
        # self.temp_texture = Texture(self.temp_image)
        # self.temp_layer.texture = self.temp_texture

        # for y in range(2):
        #     for x in range(2):
        #         b = Button(parent=self, model='quad', color=col, collider='box', scale=.5, position=(x/2, y/2))
        #         b.img = Image.new('RGBA', (width//2, height//2), (255, 255, 255, 255))
        #         b.texture = Texture(b.img)
        #         b.temp_image = Image.new('RGBA', (width//2, height//2), (0, 0, 0, 0))
        #         b.temp_layer = Entity(parent=b, model='quad', z=-1, color=color.clear)
        #         b.temp_texture = Texture(b.temp_image)
        #         b.temp_layer.texture = b.temp_texture
        #         b.width = width//2
        #         b.height = height//2


    def input(self, key):
        # if key == 'left mouse down':
        #     self.undo_img = self.img.copy()

        if key == 'scroll up' and not mouse.left:
            camera.fov /= 1.25
            camera.fov = max(camera.fov, 0)
            print(camera.fov)

        if key == 'scroll down' and not mouse.left:
            prev_cam_fov = camera.fov
            camera.fov *= 1.25
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
