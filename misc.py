# misc.py

from PIL import Image
import pygame as pg


class Misc(object):
    def __init__(self):
        self.last = pg.time.get_ticks()
        self.delay = None

    def get_delay(self, delay):
        self.delay = delay
        now = pg.time.get_ticks()
        if now - self.last >= self.delay:
            self.last = now
            return True
        return False

    def split_animated_gif(gif_file_path):
        ret = []
        gif = Image.open(gif_file_path)
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            frame_rgba = gif.convert("RGBA")
            pygame_image = pg.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            ret.append(pygame_image)
        return ret
