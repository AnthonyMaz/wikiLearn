import os

import requests
import wikipedia
import tempfile
from itertools import cycle
import argparse
import random
import os.path
import pyglet
from pyglet.gl import *


try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True, )
    window = pyglet.window.Window(fullscreen=True, resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.gl.glClearColor(0, 0, 0, 0)


def update_pan_zoom_speeds():
    global _pan_speed_x
    global _pan_speed_y
    global _zoom_speed
    _pan_speed_x = random.randint(-20, 20)
    _pan_speed_y = random.randint(-20, 20)
    _zoom_speed = random.uniform(0.02, 0.10)
    return _pan_speed_x, _pan_speed_y, _zoom_speed


def build_playlist(wikipage):
    global _playlist

    wiki_media = wikipedia.page(wikipage).images

    temp_dir_path = tempfile.mkdtemp(prefix='wiki-learn-')

    image_urls = list(filter(lambda x: ".jpg" in x or ".png" in x or ".svg" in x, wiki_media))

    for image_url in image_urls:
        image_name = os.path.basename(image_url)
        r = requests.get(image_url, allow_redirects=True)
        open(temp_dir_path + os.sep + image_name, 'wb').write(r.content)

    image_paths = get_image_paths(temp_dir_path)
    _playlist = cycle(image_paths)

    return _playlist


def update_pan(dt):
    sprite.x += dt * _pan_speed_x
    sprite.y += dt * _pan_speed_y


def update_zoom(dt):
    sprite.scale += dt * _zoom_speed


def update_opacity(dt):
    sprite.opacity += 1


def update_image(dt):
    sprite.opacity = 255
    window.clear()

    next_image = next(_playlist)
    this_image, next_image = next_image, next(_playlist)

    img = pyglet.image.load(this_image)
    sprite.image = img
    sprite.scale = get_scale(window, img)
    sprite.x = 0
    sprite.y = 0
    update_pan_zoom_speeds()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale


@window.event
def on_draw():
    sprite.draw()


def render_slideshow(wikipage):
    _pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()
    _playlist = build_playlist(wikipage)

    next_image = next(_playlist)
    this_image, next_image = next_image, next(_playlist)

    first_frame = pyglet.image.load(this_image)

    global sprite
    sprite = pyglet.sprite.Sprite(first_frame)
    sprite.scale = get_scale(window, first_frame)

    pyglet.clock.schedule_interval(update_image, 2.5)
    pyglet.clock.schedule_interval(update_pan, 1 / 60.0)
    pyglet.clock.schedule_interval(update_zoom, 1 / 60.0)
    pyglet.clock.schedule_interval(update_opacity, 1 / 60.0)

    pyglet.app.run()
