from ursina import *

class MeshBrush(Entity):
    def __init__(self):
        super().__init__()



    def input(self, key):
        if key == 'left mouse down':
            self.start = Vec3(mouse.x * window.aspect_ratio, mouse.y, 0)

        if key == 'left mouse up':
            self.end = Vec3(mouse.x * window.aspect_ratio, mouse.y, 0)

            # try:
            #     destroy(self.line)
            # except:
            #     pass

            start_point = Entity(parent=camera.ui, position=self.start, model='cube', scale=(.01,.01,.01), color=color.lime)
            end_point = Entity(parent=camera.ui, position=self.end, model='cube', scale=(.01,.01,.01), color=color.orange)
            start_point.look_at(end_point)
            end_point.look_at(start_point)

            thickness = .05
            self.line = Entity(
                parent = camera.ui,
                # model = Mesh(
                #     verts = (
                #         self.start + (start_point.down * thickness),
                #         self.end + (end_point.down * thickness),
                #         self.end + (end_point.up * thickness),
                #         self.start + (start_point.up * thickness)
                #         ),
                #     uvs = ((0,0), (1,0), (1,1), (0,1))
                #     # thickness = 10,
                #     # mode = 'line',
                #     ),
                position = self.start,
                model = 'cube',
                origin = (0, 0, -.5),

                texture = 'shore',
                )
            self.line.look_at(end_point)
            self.line.scale *= thickness /2
            self.line.scale_z = distance(start_point, end_point)
            start_point.world_parent = self.line
            end_point.world_parent = self.line
            # self.line.world_parent = scene


if __name__ == '__main__':
    app = Ursina()
    MeshBrush()
    EditorCamera()
    camera.orthographic = True
    app.run()
