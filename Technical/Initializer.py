from constants import *


def which_mode():
    event, values = sg.Window('Choose an option', [
        [sg.Text('Choose the save you want to load:')],
        [sg.Button('Hex', key="AppHex"),
         sg.Button('Standard', key="AppStandard")]]
                              ).read(close=True)
    return event
