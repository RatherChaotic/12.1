# misc.py

from PIL import Image
import pygame as pg


class Misc(object):
    def __init__(self):
        """
        Initialize the MyClass object.
        """
        # Store the last time in milliseconds
        self.last = pg.time.get_ticks()
        # Store the delay value
        self.delay = None

    def get_delay(self, delay):
        """
        Check if a specified delay has passed since the last time this function was called.

        Args:
            delay (int): The delay in milliseconds.

        Returns:
            bool: True if the delay has passed, False otherwise.
        """
        # Update the delay attribute
        self.delay = delay

        # Get the current time in milliseconds
        now = pg.time.get_ticks()

        # Check if the specified delay has passed since the last time this function was called
        if now - self.last >= self.delay:
            # Update the last attribute to the current time
            self.last = now
            return True
        return False

    from typing import List
    from PIL import Image
    import pygame as pg

    def split_animated_gif(gif_file_path: str) -> List[pg.Surface]:
        """
        Splits an animated GIF into individual frames and returns a list of pygame surfaces.

        Args:
            gif_file_path (str): The file path of the GIF.

        Returns:
            List[pg.Surface]: A list of pygame surfaces representing each frame of the GIF.
        """
        # Initialize an empty list to store the frames
        frames = []

        # Open the GIF file
        gif = Image.open(gif_file_path)

        # Iterate over each frame in the GIF
        for frame_index in range(gif.n_frames):
            # Seek to the current frame
            gif.seek(frame_index)

            # Convert the frame to RGBA format
            frame_rgba = gif.convert("RGBA")

            # Create a pygame image from the RGBA frame
            pygame_image = pg.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )

            # Append the pygame image to the list of frames
            frames.append(pygame_image)

        # Return the list of frames
        return frames
