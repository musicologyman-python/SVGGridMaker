#!/usr/bin/env python3

import argparse
import functools
import io
import math
import re
import pyperclip
from typing import NamedTuple


NUMBER_RE = re.compile(r'^-?\d+$')

AXIS_CSS_CLASS_NAME = 'axis'
GRIDLINE_CSS_CLASS_NAME = 'gridline'
    

class GridParameters(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    increment: int
    extends: int

def make_grid(gp: GridParameters):
    with io.StringIO() as sp:
        prints = functools.partial(print, file=sp)

        # generate vertical lines
        for i in range(gp.min_x, gp.max_x + gp.increment, gp.increment):
            class_ = AXIS_CSS_CLASS_NAME if i == 0 else GRIDLINE_CSS_CLASS_NAME
            prints(f'<line x1="{i}" y1="{gp.min_y - gp.extends}" x2="{i}" '
                   f'y2="{gp.max_y + gp.extends}" class="{class_}"/>')

        # generate horizontal lines
        for i in range(gp.min_y, gp.max_y + gp.increment, gp.increment):
            class_ = AXIS_CSS_CLASS_NAME if i == 0 else GRIDLINE_CSS_CLASS_NAME
            prints(f'<line x1="{gp.min_x - gp.extends}" y1="{i}" '
                   f'x2="{gp.max_x + gp.extends}" '
                   f'y2="{i}" class="{class_}"/>')

        return sp.getvalue()
        
def command_line_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_x', type=int, default=0, 
                        help='The x-coordinate of the leftmost gridline')
    parser.add_argument('--max_x', type=int, default=850, 
                        help='The x-coordinate of the rightmost '
                                    'gridline')
    parser.add_argument('--min_y', type=int, default=0, 
                        help='The y-coordinate of the leftmost gridline')
    parser.add_argument('--max_y', type=int, default=1100, 
                        help='The y-coordinate of the leftmost gridline')
    parser.add_argument('-i', '--increment', type=int,
                        help='The number of units between gridlines')
    parser.add_argument('-e', '--extends', type=int,
                        help='The number of units the gridline extends '
                        'past the left/right/top/bottom-most perpendicular '
                        'gridline')
    return parser.parse_args()

            
def main():

    args = command_line_setup()
        
    min_x = args.min_x
    max_x = args.max_x
    min_y = args.min_y
    max_y = args.max_y
    incr = args.increment
    extends = args.extends

    if incr is None:
        incr = math.gcd(min_x, max_x, min_y, max_y)
    if extends is None:
        extends = incr // 2 

    gp = GridParameters(min_x = min_x,
                        max_x = max_x,
                        min_y = min_y,
                        max_y = max_y,
                        increment = incr,
                        extends = extends)
    
    grid_text = make_grid(gp)
    pyperclip.copy(grid_text)

    print()
    print("The following SVG elements have been generated and copied to "
          "the clipboard.")
    print(grid_text)
    print()


if __name__ == '__main__':
    main()
