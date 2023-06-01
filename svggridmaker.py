from collections import namedtuple

from svg_grid_creator import GridParameters, GridGenerator
import pyperclip
import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color

layout = [[sg.Column([
            [sg.Text('Minimum X:', size=(12, 1)), 
             sg.InputText(size=(4, 1), justification='right',
                          key='-MINIMUM_X-')],
            [sg.Text('Maximum X:', size=(12, 1)), 
             sg.InputText(size=(4, 1), justification='right',
                          key='-MAXIMUM_X-')]
            ]),
           sg.Column([
            [sg.Text('Minimum Y:', size=(12, 1)), 
             sg.InputText(size=(4, 1), justification='right',
                          key='-MINIMUM_Y-')],
            [sg.Text('Maximum Y:', size=(12, 1)), sg.InputText(size=(4, 1), justification='right',
                          key='-MAXIMUM_Y-')]])],
           [sg.HorizontalSeparator()],
           [sg.Text('Major Axis Increment:', size=(22, 1)),
            sg.InputText(size=(4, 1), justification='right', 
                         key='-MAJOR_AXIS_INCR-')],
           [sg.Text('Minor Axis Increment:', size=(22, 1)),
            sg.InputText(size=(4, 1), justification='right', 
                         key='-MINOR_AXIS_INCR-')],
           [sg.Button('Generate Grid Text', key='-GENERATE_GRID_TEXT-')],
           [sg.Multiline(key='-RESULTS-', font='Menlo 12',
                         size=(40, 15))],
           [sg.Button('Copy Grid Text', key='-COPY_GRID_TEXT-')]
          ]
            

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    match window.read():
        case sg.WIN_CLOSED, _:
            break
        case '-GENERATE_GRID_TEXT-', values:
            gp = GridParameters(min_x = values['-MINIMUM_X-'].strip(),
                                max_x = values['-MAXIMUM_X-'].strip(),
                                min_y = values['-MINIMUM_X-'].strip(),
                                max_y = values['-MAXIMUM_X-'].strip(),
                                minor_axis_incr = values['-MINOR_AXIS_INCR-'].strip(),
                                major_axis_incr = values['-MAJOR_AXIS_INCR-'].strip())

            window['-RESULTS-'].update(GridGenerator(gp).do_it())
        case '-COPY_GRID_TEXT-', value:
            pyperclip.copy(value['-RESULTS-'])
        case _, values:
            print(f'You entered {values}') 

window.close()
