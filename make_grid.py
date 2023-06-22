#!/usr/bin/env python3

import functools
import io
import math
import re
import pyperclip
from typing import NamedTuple


NUMBER_RE = re.compile(r'^-?\d+$')

class GridParameters(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    increment: int
    extension: int

def make_grid(gp: GridParameters):
    with io.StringIO() as sp:
        prints = functools.partial(print, file=sp)
        for i in range(gp.min_x, gp.max_x + gp.increment, gp.increment):
            class_ = "axis" if i == 0 else "gridline"
            prints(f'<line x1="{i}" y1="{gp.min_y - gp.extension}" x2="{i}" '
                   f'y2="{gp.max_y + gp.extension}" class="{class_}"/>')
        for i in range(gp.min_y, gp.max_y + gp.increment, gp.increment):
            class_ = "axis" if i == 0 else "gridline"
            prints(f'<line x1="{gp.min_x - gp.extension}" y1="{i}" '
                   f'x2="{gp.max_x + gp.extension}" '
                   f'y2="{i}" class="{class_}"/>')

        return sp.getvalue()
        

def prompt_for_signed_integer(prompt, default=None):

    response = input(prompt).strip()
    
    if not response and default is not None:
        response = default

    while True:
        match response:
            case int() | float():
                return response

        if NUMBER_RE.search(response) is not None:
                return int(response)

        response = input(f'The value "{response.trim()}" is not an integer. '
                         'Please enter an integer or "q" (case insensitive) '
                         'to abort: ')
        if response.trim().lower() == 'q':
            sys.exit(-1)
             
def main():

    NUMBER_RE = re.compile(r'^\s*-?\d+\s*$')

    try:
        min_x = prompt_for_signed_integer(
                'Enter the minimum horizontal value (min_x): ' )
        while True:
            max_x = prompt_for_signed_integer(
                    'Enter the maximum horizontal value (max_x): ' )
            if min_x >= max_x:
                print(f"The maximum value for x must be greater than {min_x}.")
            else:
                break

        min_y = prompt_for_signed_integer(
                'Enter the minimum horizontal value (min_y): ' )
        while True:
            max_y = prompt_for_signed_integer(
                    'Enter the maximum horizontal value (max_y): ' )
            if min_y >= max_y:
                print(f"The maximum value for y must be greater than {min_y}.")
            else:
                break


        default_incr = math.gcd(min_x, max_x, min_y, max_y)
        incr = prompt_for_signed_integer(
                f'Enter the grid increment(default={default_incr}): ', 
                default=default_incr)
        extension = prompt_for_signed_integer(f'How far will the grid line '
                    'extend before the first and after the last perpendicular '
                    f'grid line? (default {incr/2}) ', default=incr/2)

        gp = GridParameters(min_x = min_x,
                            max_x = max_x,
                            min_y = min_y,
                            max_y = max_y,
                            increment = incr,
                            extension = extension)
        
        grid_text = make_grid(gp)
        pyperclip.copy(grid_text)

        print()
        print("The following SVG elements have been generated and copied to "
              "the clipboard.")
        print(grid_text)
        print()

    except SystemExit:
        ...

if __name__ == '__main__':
    main()
