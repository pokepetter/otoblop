from ursina import *
from PIL import Image, ImageChops
import numpy
import time
from brush import Brush
from eyedropper import Eyedropper
from palette import Palette
from panda3d.core import Texture as PandaTexture
from layer import Layer

window.vsync = False
input_handler.rebind('x', '-')
input_handler.rebind('d', '+')

class Otoblop(Ursina):
    def __init__(self):
        super().__init__()

        camera.orthographic = True
        camera.fov = 100
        window.color = color.gray
        self.cursor = Cursor(model=Circle(mode="lines"))

        # self.layer = Layer(512, 512)
        self.layer = Layer(1920, 1080)

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


app = Otoblop()
from ursina.prefabs.dropdown_menu import DropdownMenu
from ursina.prefabs.dropdown_menu import DropdownMenuButton as MenuButton

DropdownMenu(
    text = 'File',
    buttons = (
        MenuButton('New'),
        MenuButton('Open'),
        MenuButton('Save'),
        MenuButton('Save as...'),
        MenuButton('Settings'),
        MenuButton('Exit', on_click='application.quit'),
        )
)


app.run()
