from ursina import *
from PIL import Image

class B(Entity):

    def __init__(self):
        super().__init__()
        self.model = 'quad'
        # self.texture = 'shore'
        self.collider = 'box'
        self.scale *= 6
        self.width, self.height = 2048, 2048

        self.brush = Image.open('textures/' + 'round_soft.png').transpose(Image.FLIP_TOP_BOTTOM)
        self.brush_pixels = self.brush.load()

        self.img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        self.texture_buffer = Texture()
        self.texture_buffer.setup2dTexture(self.width, self.height, Texture.TUnsignedByte, Texture.FRgba)
        self.texture_buffer.setRamImageAs(self.img.tobytes(), "RGBA")

        self.texture = self.texture_buffer

        self.i = 0
        # newpixels = self.img.load()
        # for x in range(self.img.width):
        #     for y in range(self.img.height):
        #         # newpixels[x, y] = tuple([int(round(e*255, 0)) for e in color.random_color()])
        #         newpixels[x, y] = tuple([int(round(e*255, 0)) for e in color.black])

    def set_pixel(self, x, y, col):
        newpixels = self.img.load()
        t = time.time()
        for ox in range(self.brush.width):
            for oy in range(self.brush.height):
                try:
                    # if x+ox < 0 or y+oy < 0 or x+ox >= self.img.width or y+oy >= self.img.height:
                    #     continue
                    # if self.brush_pixels[ox, oy][3] <= 0:
                    #     continue

                    # original_color = newpixels[x+ox, y+oy]
                    # target_color = col
                    # a = max(.01, self.brush_pixels[ox, oy][3]/255)
                    # target_color = tuple([int(e[0]+(e[1]-e[0])*a) for e in zip(original_color, target_color)])
                    # target_color = [255,255,0,255]
                    newpixels[x+ox, y+oy] = (255,255,0,255)
                except:
                    pass

        # print(time.time() - t)
        # t = time.time()
        # self.texture.setRamImageAs(self.img.tobytes(), "RGBA")
        # print(time.time() - t)


    def input(self, key):
        if key == 'u':
            self.texture.setRamImageAs(self.img.tobytes(), "RGBA")


    def update(self):
        # print(mouse.velocity)
        if mouse.left and self.hovered and abs(mouse.velocity[0]) + abs(mouse.velocity[1]) >= .001:
            # Entity(parent=self.b, position=mouse.point, z=-.1, model='quad', color=color.orange, scale=(.01,.01))
            x = int((mouse.point[0] + .5) * self.width)
            y = int((mouse.point[1] + .5) * self.height)
            self.set_pixel(x, y, [0,255,0,255])

            # return
            self.i += time.dt
            if self.i > .05:  # update image less often to reduce lag.
                b = self.img.tobytes()
                self.texture_buffer.setRamImage(b)
                self.texture = self.texture_buffer
                self.i = 0
a = Ursina()
camera.orthographic = True
camera.fov = 8
B()
a.run()
