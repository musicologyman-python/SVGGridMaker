import dataclasses
from functools import partial
import io

def _to_int(s) -> int:
    match s:
        case None | '':
            return 0.0
        case int():
            return s
        case _:
            return int(s)

@dataclasses.dataclass
class GridParameters():

    min_x: int
    max_x: int
    min_y: int
    max_y: int
    major_axis_incr: int
    minor_axis_incr: int

    def __init__(self, min_x, max_x, min_y, max_y, major_axis_incr, 
                 minor_axis_incr):
        self.min_x = _to_int(min_x)
        self.max_x = _to_int(max_x)
        self.min_y = _to_int(min_y)
        self.max_y = _to_int(max_y)
        self.major_axis_incr = _to_int(major_axis_incr)
        self.minor_axis_incr = _to_int(minor_axis_incr)

class GridGenerator():

    def __init__(self, grid_parameters):
        self.min_x = grid_parameters.min_x
        self.max_x = grid_parameters.max_x
        self.min_y = grid_parameters.min_y
        self.max_y = grid_parameters.max_y
        self.major_axis_incr = grid_parameters.major_axis_incr
        self.minor_axis_incr = grid_parameters.minor_axis_incr

    def _generate_vertical_grid_lines(self, fp):
        prints = partial(print, file=fp)
        y_start = self.min_y - self.major_axis_incr / 2
        y_end = self.max_y + self.major_axis_incr / 2
        for i in range(self.min_x, self.max_x, self.major_axis_incr):
             prints(f'<line x1="{i}" y1="{y_start}" '
                    f'x2="{i}" y2="{y_end}" />')
        
    def _generate_horizontal_grid_lines(self, fp):
        prints = partial(print, file=fp)
        x_start = self.min_x - self.major_axis_incr / 2
        x_end = self.max_x + self.major_axis_incr / 2
        for i in range(self.min_y, self.max_y, self.major_axis_incr):
             prints(f'<line x1="{x_start}" y1="{i}" '
                    f'x2="{x_end}" y2="{i}" />')

    def _get_grid_commands(self, generate_grid):
        with io.StringIO() as fp:
            generate_grid(fp)
            return fp.getvalue()

    def do_it(self):
        v = self._get_grid_commands(self._generate_horizontal_grid_lines)
        w = self._get_grid_commands(self._generate_vertical_grid_lines)

        return f'{v}\n{w}'
            
