import PySimpleGUI as sg
import time
import toml
from popup import show_input_popup


data = toml.load("./config.toml")
x = data["display"]["x"]
y = data["display"]["y"]
bg = data["display"]["bg_color"]
text_color = data["display"]["text_color"]
font_size = data["display"]["font_size"]
alpha_channel = data["display"]["alpha_channel"]

sg.set_options(font=("Courier New", font_size))
layout = [[sg.Text("Time: ", key='-TIMER-', background_color=bg, pad=(0, 0), enable_events=True, text_color=text_color)]]
window = sg.Window(
    'title',
    layout,
    grab_anywhere=True,
    keep_on_top=True,
    margins=(0,0),
    no_titlebar=True,
    location=(x, y),
    font=("Courier New", font_size),
    alpha_channel=alpha_channel,
    )
if not data["display"]["background"]:
    window.finalize()
    window.SetTransparentColor(bg)

periods = {
    "day": data["durations_minutes"]["day"] * 60,
    "night": data["durations_minutes"]["night"] * 60
}
start_time = time.time()
starting_minutes = int(time.strftime("%M"))

if starting_minutes < 50:
    current_period = "day"
    remaining_time =  60 * starting_minutes
else:
    current_period = "night"
    remaining_time = periods[current_period] - (60 - starting_minutes) * 60

start_time -= remaining_time + int(time.strftime("%S"))

while True:
    if remaining_time <= 0:
        if current_period == "day":
            current_period = "night"
        else:
            current_period = "day"
        remaining_time = periods[current_period]
        start_time = time.time()

    event, values = window.read(timeout=1000)  # Update every second

    if event == sg.WIN_CLOSED:
        break
    elif event == "-TIMER-":
        new_count, new_font_size= show_input_popup(periods["day"] // 60, periods["night"] // 60, font_size)
        if new_count not in [None, "Exit"]:
            period = new_count[0] # started, day, night
            periods["day"] = new_count[1]
            periods["night"] = new_count[2]

            remaining_time = periods[period]
            start_time = time.time()
        if new_font_size:
            font_size = new_font_size
            window['-TIMER-'].update(font=("Courier New", font_size))

        if new_count == "Exit":
            break

    elapsed_time = time.time() - start_time
    remaining_time = max(periods[current_period] - elapsed_time, 0)
    remaining_minutes = int(remaining_time // 60)
    remaining_seconds = int(remaining_time - (remaining_minutes * 60))
    if remaining_minutes < 10:
        remaining_minutes = "0"+str(remaining_minutes)
    if remaining_seconds < 10:
        remaining_seconds = "0"+str(remaining_seconds)
    window['-TIMER-'].update(f'{current_period}: {remaining_minutes}:{remaining_seconds}')

window.close()
