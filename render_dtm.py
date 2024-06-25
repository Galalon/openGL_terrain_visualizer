from OpenGL.GL import glGenTextures, glTexImage2D, glBegin, glEnd
from OpenGL.raw.GL.ARB.internalformat_query2 import GL_TEXTURE_2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glTexParameteri, GL_TEXTURE_WRAP_S, GL_REPEAT, GL_TEXTURE_WRAP_T, \
    GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_TEXTURE_MAG_FILTER, GL_RGB, glEnable, glTexCoord2f, glVertex3f, glDisable
from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture
from OpenGL.raw.GL.VERSION.GL_4_0 import GL_QUADS
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from OpenGL.GL import GL_LINES


# Initialize texture
def init_texture(image):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[1], image.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    return texture_id


# Function to render the DTM with texture
def render_dtm(x, y, z, texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    len_x =  len(x) - 1
    len_y =  len(y) - 1

    for i in range(len_x):
        for j in range(len_y):
            glTexCoord2f(i / len_x, j / len_y)
            glVertex3f(x[i, j], y[i, j], z[i, j])

            glTexCoord2f((i + 1) / len_x, j / len_y)
            glVertex3f(x[i + 1, j], y[i + 1, j], z[i + 1, j])

            glTexCoord2f((i + 1) / len_x, (j + 1) / len_y)
            glVertex3f(x[i + 1, j + 1], y[i + 1, j + 1], z[i + 1, j + 1])

            glTexCoord2f(i / len_x, (j + 1) / len_y)
            glVertex3f(x[i, j + 1], y[i, j + 1], z[i, j + 1])
    glEnd()

    glDisable(GL_TEXTURE_2D)


# Function to render the DTM wireframe
def render_dtm_wireframe(x, y, z):
    glBegin(GL_LINES)
    len_x = len(x) - 1
    len_y = len(y) - 1

    for i in range(len_x):
        for j in range(len_y):
            glVertex3f(x[i, j], y[i, j], z[i, j])
            glVertex3f(x[i + 1, j], y[i + 1, j], z[i + 1, j])

            glVertex3f(x[i + 1, j], y[i + 1, j], z[i + 1, j])
            glVertex3f(x[i + 1, j + 1], y[i + 1, j + 1], z[i + 1, j + 1])

            glVertex3f(x[i + 1, j + 1], y[i + 1, j + 1], z[i + 1, j + 1])
            glVertex3f(x[i, j + 1], y[i, j + 1], z[i, j + 1])

            glVertex3f(x[i, j + 1], y[i, j + 1], z[i, j + 1])
            glVertex3f(x[i, j], y[i, j], z[i, j])
    glEnd()