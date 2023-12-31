import PySimpleGUI as sg


def show_input_popup(day: int, night: int, font_size: int):
    layout = [
        [sg.Text('Day length:')],
        [
            sg.InputText(default_text=day, key='day-minutes', size=(10, 1)),
            sg.Text('minutes', size=(10, 1))],
        # [sg.InputText(default_text='0', key='day-seconds', size=(10, 1)),
        #  sg.Text('seconds', size=(10, 1))],
        [sg.Button('Start day')],

        [sg.Text('Night length:')],
        [
            sg.InputText(default_text=night, key='night-minutes', size=(10, 1)),
            sg.Text('minutes', size=(10, 1))],
        # [sg.InputText(default_text='0', key='night-seconds', size=(10, 1)),
        #  sg.Text('seconds', size=(10, 1))],
        [sg.Button('Start night')],

        [
            sg.InputText(default_text=font_size, key='font-size', size=(3, 1)),
            sg.Text('Font Size', size=(10, 1))],
        [sg.Button('Set font size')],
        [sg.Button('Cancel')],
        [sg.Button('Exit')]
    ]

    win = sg.Window('Set Countdown Duration', layout, keep_on_top=True, finalize=True)

    while True:
        event, values = win.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            win.close()
            return None, None
        if event == "Exit":
            win.close()
            return "Exit", None

        try:
            font_size = int(values["font-size"])
            day_minutes = int(values['day-minutes'])
            #day_seconds = int(values["day-seconds"])
            night_minutes = int(values['night-minutes'])
            # night_seconds = int(values["night-seconds"])
            day_length = day_minutes * 60# + day_seconds
            night_length = night_minutes * 60# + night_seconds
        except ValueError:
            sg.popup_ok('Invalid input. Please enter a valid number.')
            continue
            #return None, None

        if event == 'Set font size':
            win.close()
            return None, font_size
        if event == "Start day":
            win.close()
            return ("day", day_length, night_length), None
        if event == "Start night":
            win.close()
            return ("night", day_length, night_length), None
