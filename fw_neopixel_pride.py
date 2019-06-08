# -*- coding: utf-8 -*-
"""
Pride Flag NetPixel Badge

Displays a bunch of different Pride flags on a NeoPixel grid. Designed for use
with the Adafruit Feather M0 Express and NeoPixel FeatherWing.

Full details at <http://github.com/tammymakesthings/cpy_neopixel_pride>

@author: tammy.cravit
@license: MIT
"""

import sys
from time import sleep

# Delay in seconds between frames of the animation.
ANIMATION_SPEED    = 0.3

# Time in seconds to hold each flag on screen before switching.
SHOW_PATTERN_DELAY = 15

# Intensity (0-1) of the NeoPixels. Higher intensity is brighter but draws
# more current.
PATTERN_INTENSITY  = 0.3

# The number of rows in the NeoPixel grid.
NUM_ROWS = 4

# The number of columns in the NeoPixel grid.
NUM_COLS = 8

# Board pin to which the NeoPixel is connected
neopixel_pin = None

# The NeoPixel object controlling the pixels.
pixels = None

# Do the hardware setup if we're running on CircuitPython.
if sys.implementation.name == "circuitpython":
    import time
    import board
    import neopixel

    # Control pin defaults to #6
    neopixel_pin = board.D6
    pixels = neopixel.NeoPixel(neopixel_pin, (NUM_ROWS * NUM_COLS),
                               brightness=PATTERN_INTENSITY, auto_write=False)

############################################################################
# Define all of the flag color palettes
############################################################################

flag_colors = {
        "-": (0,   0,   0),     # Black
        
        # LGBT Flag
        'A': (231, 0,   0),     # Electric Red
        'B': (224, 89,  17),     # Dark Orange
        'C': (255, 239, 0),     # Canary Yellow
        'D': (0,   129, 31),    # La Salle Green
        'E': (0,   68,  255),   # Blue (RYB)
        'F': (118, 0,   137),   # Patriarch

        # Trans Flag
        'G': (65,  175, 222),   # Maya Blue
        'H': (255, 255, 255),   # White
        'I': (217, 148, 144),   # Amaranth Pink

        # Bi Pride Flag
        'J': (215, 2,   112),   # Magenta
        'K': (115, 79,  150),   # Deep Lavender
        'L': (0,   56,  168),   # Royal
        
        # Nonbinary Flag
        'M': (255, 239, 0),    # Yellow
        'N': (230, 230, 230),   # White
        'O': (255, 20, 140),    # Lavender

        # Pansexual Flag
        'P': (255, 20, 140),    # Deep Pink
        'Q': (255, 218, 0),     # Sizzling Sunrise
        'R': (5, 174, 255)      # Blue Bolt
        }

############################################################################
# Define the actual flag patterns. Each pattern must refernece colors defined
# in the associated color map. The pattern contains one letter per column of
# the display.
############################################################################

patterns = {
        'pride_flag': {'pattern': '-ABCDEF-', 'colors': flag_colors},
        'trans_flag': {'pattern': '-JKLKJ--', 'colors': flag_colors},
        'bi_flag'   : {'pattern': '--JJKLL-', 'colors': flag_colors},
        'nb_flag'   : {'pattern': 'MMNNOO--', 'colors': flag_colors},
        'pan_flag'  : {'pattern': '-PPQQRR-', 'colors': flag_colors},
        }

############################################################################
# Helper functions
############################################################################


def clear_pixels(rows=NUM_ROWS, cols=NUM_COLS):
    """
    .. function:: clear_pixels([rows, cols])
    
    Clear the entire pixel array.
    
    Sets all of the pixels in the NeoPixel array to black and hten writes
    the values to the array. Has no effect if not running on a CircuitPython
    device.
    
    :param rows: number of rows in the array (defaults to value of NUM_ROWS)
    :param cols: number of cols in the array (defaults to value of NUM_COLS)
    :rtype: None
    """
    print("inside clearPixels({0}, {1})".format(rows, cols))
    if pixels is not None:
        pixels.fill(0, 0, 0)
        pixels.show()


def set_column(display_column, rgb_value):
    """
    .. function:: set_column(display_column, rgb_value)
    
    Set all pixels in one column of the display to the given color.
    
    :param display_column: The column on the display to set
    :param rgb_value: The RGB color to set the pixels to
    :type rgb_value: 3-tuple (R, G, B)
    :rtype: None
    """
    print('Called set_column({0}, {1})'.format(display_column, rgb_value))
    if pixels is not None:
        for i in range(0, NUM_ROWS):
            which_pixel = (i * NUM_COLS) + display_column
            pixels[which_pixel] = rgb_value


def slide_in_animation(the_pattern, color_map, animation_speed=ANIMATION_SPEED):
    """
    .. function:: slide_in_animation(the_pattern, color_map, animation_speed)
    
    Render the animation for a single flag.
    
    :param the_pattern: The flag pattern, rendered as a string. Each character
    in the string should match a color in the color map.
    :param color_map: The color map. The keys of the dictionary should be a
    character from the pattern. The value of the dictionary entries should be
    3-tuples with the R, G, B values for the specified color.
    :type color_map: dict
    :param animation_speed: The time (in seconds) to sleep between frames of
    the animation.
    :rtype: None
    """
    print("inside slideInAnimation({0}, {1}, {2})".format(the_pattern, color_map, animation_speed))
    for i in range(0, len(the_pattern)):
        starting_column = len(the_pattern) - i - 1
        ending_column = len(the_pattern)
        which_letter = 0
        
        print("Animation: Repetition {0}, starting column={1}".format(i+1, starting_column))
        for j in range(0, starting_column):
            set_column(j, (0,0,0))
            print("-", sep='', end='')
        for j in range(starting_column, ending_column):
            print(the_pattern[which_letter], sep='', end='')
            set_column(j, color_map[the_pattern[which_letter]])
            which_letter += 1
        print('\n')
        if sys.implementation.name == "circuitpython":
            pixels.show()
        sleep(animation_speed)


def renderAllPatterns(the_patterns):
    for pattern_name, pattern_data in the_patterns.items():
        print("renderAllPatterns(): rendering flag: {0}".format(pattern_name))
        the_pattern = pattern_data['pattern']
        color_map   = pattern_data['colors']
        slide_in_animation(the_pattern, color_map)
        sleep(SHOW_PATTERN_DELAY)


############################################################################
# Main execution loop
############################################################################

if __name__=="__main__":
    while True:
        renderAllPatterns(patterns)