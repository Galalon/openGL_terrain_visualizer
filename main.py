import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt

from camera import CameraConfig,Camera
from dtm_preprocess import preprocess_terrain_data
from render_dtm import render_dtm,render_dtm_wireframe,init_texture


# Function to handle window resizing
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


# Create a checkerboard texture
def create_checkerboard_texture(size=1000, num_squares=500):
    image = np.zeros((size, size, 3), dtype=np.uint8)
    s = size // num_squares
    for i in range(num_squares):
        for j in range(num_squares):
            if (i + j) % 2 == 0:
                image[i * s:(i + 1) * s, j * s:(j + 1) * s] = 255  # White square
            else:
                image[i * s:(i + 1) * s, j * s:(j + 1) * s] = 0  # Black square
    return image

# Function to render the scene
def render_scene(window, dtm_grid, texture_id,camera:Camera,mode='texture'):
    x, y, z = dtm_grid
    camera.set_up()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Render the DTM
    assert mode in ['texture','wireframe']
    if mode == 'texture':
        render_dtm(x, y, z, texture_id)
    else:
        render_dtm_wireframe(x, y, z)

    # Swap buffers and process events
    glfw.swap_buffers(window)
    glfw.poll_events()


# Function to save the rendered image
def save_screenshot(window, filename):
    width, height = glfw.get_framebuffer_size(window)
    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes(mode="RGB", size=(width, height), data=pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL stores images upside down
    image.save(filename)


# Initialize GLFW and OpenGL
def init_glfw_and_opengl(window_size):
    if not glfw.init():
        raise Exception("Failed to initialize GLFW")

    window = glfw.create_window(window_size[0], window_size[1], "DTM Renderer", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    return window


# Main function
def main(dtm_filepath, ortho_path, output_filepath, window_size, camera):

    orthophoto, dtm_grid = preprocess_terrain_data(dtm_filepath, ortho_path)
    window = init_glfw_and_opengl(window_size)
    texture_id = init_texture(orthophoto)

    # Render a single frame
    render_scene(window, dtm_grid, texture_id, camera)
    save_screenshot(window, output_filepath)

    glfw.terminate()


if __name__ == "__main__":
    dtm_filepath = r'.\example\DTM1\DTM\dtm\w001001.adf'
    image_filepath = r'.\example\Orthophotograph\Orthophotograph\pam8C50cm180.tif'
    output_filepath = r'.\output\dtm_render.png'
    window_size = [1024, 720]  # xy
    camera_config = CameraConfig()
    camera_config.y_fov=60
    camera_config.x_fov = camera_config.y_fov * window_size[0] / window_size[1]
    camera_config.camera_pos = [500, 500, 60]
    camera_config.camera_rot = [30, -60, 0]
    camera = Camera(camera_config)

    main(dtm_filepath, image_filepath, output_filepath, window_size, camera)

    screenshot = cv2.imread(output_filepath)
    plt.imshow(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
    plt.show()
