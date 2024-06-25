from OpenGL.raw.GL.VERSION.GL_1_0 import glMatrixMode, GL_PROJECTION, glLoadIdentity, GL_MODELVIEW, glRotatef, \
    glTranslatef
from OpenGL.raw.GLU import gluPerspective


class CameraConfig:
    def __init__(self):
        self.y_fov = 45
        self.x_fov = 60
        self.near_clip = 0.1
        self.far_clip = 2000
        self.camera_pos = [0,0,0]
        self.camera_rot = [0, 0, 1]


class Camera:

    def __init__(self, cfg:CameraConfig):
        self.cfg = cfg

    def set_up(self):
        Camera.create_camera(self.cfg.y_fov,self.cfg.x_fov,self.cfg.near_clip,self.cfg.far_clip)
        Camera.euler_rotate(self.cfg.camera_rot)
        # Then translate to the position
        Camera.translate(self.cfg.camera_pos)

    @staticmethod
    def create_camera(y_fov, x_fov, near_clip, far_clip):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(y_fov, x_fov / y_fov,near_clip,far_clip)  # Adjust the far plane to fit the entire DTM
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def translate(camera_pos):
        assert len(list(camera_pos)) == 3, "invalid position length"
        glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

    @staticmethod
    def euler_rotate(euler_angles):
        # rotation is based on Z-X-Z euler angles see documentation: https://mathworld.wolfram.com/EulerAngles.html
        glRotatef(euler_angles[2], 0, 0, 1)  # Rotate around Z-axis
        glRotatef(euler_angles[1], 1, 0, 0)  # Rotate around X-axis
        glRotatef(euler_angles[0], 0, 0, 1)  # Rotate around Z-axis
