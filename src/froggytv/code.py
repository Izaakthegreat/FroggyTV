# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import time

import board
from bpm import Bpm
from debug import Debug
from hardware import Button, Encoder, Output
from screens import GateScreen, HomeScreen, Screens
from state import ALPHABET, State
from triggers import FanOut, Periodic


# ~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State(4)
screens = [
    HomeScreen.make("home", state),
    GateScreen.make("A", state),
    GateScreen.make("B", state),
    GateScreen.make("C", state),
    GateScreen.make("D", state),
]
screen_list = Screens(state, screens)
encoder = Encoder()
play_button = Button(board.GP11).make_pin_reader()
page_button = Button(board.GP12).make_pin_reader()
encoder_button = Button(board.GP13).make_pin_reader()

outputs = [
    Output("home", board.LED),
    Output("A", board.GP1),
    Output("B", board.GP2),
    Output("C", board.GP3),
    Output("D", board.GP4),
]
bpm = Bpm(120)
callables = [Periodic(bpm.resolution, output) for output in outputs]
fan_out = FanOut(callables)

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current()

debug = Debug(False)

now = time.monotonic_ns()
bpm.start(now)
ct = 0
UPDATE_RATE = 100
while True:
    bpm.update(now, fan_out)
    debug.update(now)

    if ct == UPDATE_RATE:
        ct = 0

        play_button.update()
        page_button.update()
        encoder_button.update()

        if play_button.fell:
            state.toggle_play()
            screen_list.screens[0].update_play_button(state.get_play())

        if page_button.fell:
            screen_list.next_screen()

        if encoder_button.fell:
            screen_list.next_element()

        focused_element = screen_list.get_focused_element()
        if encoder.update(focused_element.state):
            focused_element.update()
            # TODO assumes only home OR gate screens exist
            on_home_screen = focused_element.screen.name == "home"
            on_bpm_element = focused_element.name == "bpm"
            if on_home_screen and on_bpm_element:
                bpm.set_bpm(state.get_bpm().value)
            elif focused_element.name == "div":
                callable_index = ALPHABET.index(focused_element.screen.name) + 1
                new_mult = state.get_div(focused_element.screen.name).value
                callables[callable_index].set_mult(new_mult)

    if state.get_play():
        # screen_list.screens[0].froge.spin(now, state.get_bpm().value)
        pass

    now = time.monotonic_ns()
    ct += 1
