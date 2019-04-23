from ursina import *
from PIL import Image, ImageChops
import numpy
import time
from brush import Brush
from eyedropper import Eyedropper
from palette import Palette
from panda3d.core import Texture as PandaTexture


class Otoblop(Ursina):
    def __init__(self):
        super().__init__()

        camera.orthographic = True
        camera.fov = 16
        window.color = color.gray
        self.cursor = Cursor(model=Circle(mode="lines"))

        self.canvas = Canvas(512, 512)

        # instantiate tools
        self.brush = Brush()
        self.eyedropper = Eyedropper()
        self.tools = (self.brush, self.eyedropper)
        self.active_tool = self.brush

        self.palette = Palette()

    def input(self, key):
        super().input(key)
        if key == "b":
            self.active_tool = self.brush

        if key == "alt":
            self.prev_tool = self.active_tool
            self.active_tool = self.eyedropper
            print("tyoo", self.active_tool)

        if key == "alt up":
            self.active_tool = self.prev_tool

    @property
    def active_tool(self):
        return self._active_tool

    @active_tool.setter
    def active_tool(self, value):
        print("set active tool to:", value)
        for t in self.tools:
            if t is not value:
                t.enabled = False

        value.enabled = True
        self._active_tool = value



class Canvas(Entity):
    def __init__(self, width=1024, height=1024, color=color.white):
        super().__init__()
        self.scale *= 7
        self.model = 'quad'
        # self.collider = "box"
        # make a click area bigger than the canvas to be able to click outside and still draw.
        self.bg = Entity(parent=self, z=1, collider='box', scale=(10, 10))

        self.i = 0
        # self.pressure = .1
        self.width = width
        self.height = height
        self.scale_x *= width / height

        self.layers = list()
        self.add_layer()
        self.current_layer = self.layers[0]
        # self.img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        # self.texture_buffer = Texture(self.img)
        self.texture = self.current_layer


    def add_layer(self):
        self.layers.append(Texture(Image.new("RGBA", (self.width, self.height), (255, 0, 255, 255))))


    def input(self, key):
        # if key == "left mouse down":
        #     self.undo_img = self.img.copy()

        if key == "scroll up":
            camera.fov -= 1
            camera.fov = max(camera.fov, 0)

        if key == "scroll down":
            camera.fov += 1
            camera.fov = min(camera.fov, 200)

        # if held_keys["control"] and key == "z":
        #     # print('undo')
        #     if self.undo_img:
        #         self.img = self.undo_img
        #         b = self.img.tobytes()
        #         self.texture_buffer._texture.setRamImage(b)
        #         self.texture = self.texture_buffer

    def update(self):
        if held_keys["space"]:
            camera.x -= mouse.velocity[0] * 10
            camera.y -= mouse.velocity[1] * 10

        self.i += 1
        if self.i > 2 and self.texture:  # update image less often to reduce lag.
            b = self.current_layer._cached_image.tobytes()
            self.texture._texture.setRamImage(b)
            # self.texture = self.texture_buffer
            self.i = 0


app = Otoblop()
app.run()