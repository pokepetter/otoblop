from ursina import *
import brush


class ColorMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray.tint(-.1),
            origin=(.5,.5),
            collider='box',
            scale_x=.25,
            scale_y=.2,
            x=.5*camera.aspect_ratio,
            y=.35,
            highlight_color=Button.color,
            pressed_color=Button.color,
            pressed_scale=1,
            )

        try:
            self.brush = base.otoblop.brush
        except:
            self.brush = None

        self.sliders = list()
        for i, name in enumerate(('r', 'g', 'b')):
            slider = ThinSlider(min=0, max=255, step=1, text=name, dynamic=True,
                world_parent=self, scale=(1.5, 4), position=(-.9,-.1-((i+1)*.125),-1),
                on_value_changed=self.on_slider_changed, name='name')

            self.sliders.append(slider)
            setattr(self, name+'_slider', slider)


        self.h_slider = ThinSlider(name='h', min=0, max=360, step=1, text='h', dynamic=True,
            world_parent=self, scale=(1.5, 4), position=(-.9,-.1-((1)*.125),-1),
            on_value_changed=self.on_slider_changed)

        self.s_slider = ThinSlider(name='s', min=0, max=100, step=1, text='s', dynamic=True,
            world_parent=self, scale=(1.5, 4), position=(-.9,-.1-((2)*.125),-1),
            on_value_changed=self.on_slider_changed)

        self.v_slider = ThinSlider(name='v', min=0, max=100, step=1, text='v', dynamic=True,
            world_parent=self, scale=(1.5, 4), position=(-.9,-.1-((3)*.125),-1),
            on_value_changed=self.on_slider_changed)


        self.sliders.extend([self.h_slider, self.s_slider, self.v_slider])


        for slider in self.sliders:
            # print(slider)
            slider.knob.world_scale_x = slider.knob.world_scale_y
            slider.label.world_scale_x = slider.label.world_scale_y
            slider.label.x = .56


        self.preview = Entity(model='quad', parent=self, scale=(.3,.3), color=color.red, origin=(-.5,.5),
            y=-.1-(4*.125),
            x = -.9,
            )

        self.mode = 'hsv'
        self.mode_button = Button(parent=self, model=Circle(mode='line'), scale=(.1,.1), x=-.08, y=-.1-(0*.125), color=color.white)
        self.mode_button.world_scale = .25
        self.mode_button.on_click = self.toggle_mode
        self.border = Entity(parent=self, model=Quad(segments=0, mode='line'), origin=self.origin, color=self.color.tint(-.1))

    def toggle_mode(self):
        if self.mode == 'rgb':
            self.mode = 'hsv'
        else:
            self.mode = 'rgb'



    def on_slider_changed(self):
        if self.mode == 'rgb':
            value = color.rgb(self.r_slider.value, self.g_slider.value, self.b_slider.value)
        else:
            value = color.color(self.h_slider.value, self.s_slider.value/100, self.v_slider.value/100)

        if self.brush:
            self.brush.brush_color = value

        self.preview.color = value


    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value == 'rgb':
            self.r_slider.value = int(self.preview.color.r * 255)
            self.g_slider.value = int(self.preview.color.g * 255)
            self.b_slider.value = int(self.preview.color.b * 255)

            self.r_slider.enabled = True
            self.g_slider.enabled = True
            self.b_slider.enabled = True
            self.h_slider.enabled = False
            self.s_slider.enabled = False
            self.v_slider.enabled = False


        if value == 'hsv':
            self.h_slider.value = int(self.preview.color.h)
            self.s_slider.value = int(self.preview.color.s * 100)
            self.v_slider.value = int(self.preview.color.v * 100)

            self.r_slider.enabled = False
            self.g_slider.enabled = False
            self.b_slider.enabled = False
            self.h_slider.enabled = True
            self.s_slider.enabled = True
            self.v_slider.enabled = True

        self._mode = value




if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 100
    window.color = color.gray
    ColorMenu()

    app.run()
