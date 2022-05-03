#!/usr/bin/env python3

__doc__ = "piDartboardGUI: GUI for the piDartboard project."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Development"

###TODO###TODO###TODO###TODO###TODO##############################
##
##
from subprocess import call
import time
import dearpygui.dearpygui as gui

gui.create_context()

def callback_handler(sender):
    print(f'{sender} was pressed')
    if sender == 42:
        gui.configure_item("exiting", show=True)
        print('Exiting...')
        time.sleep(0.1)
        gui.destroy_context()

with gui.window(label="Exiting", show=False, id="exiting", width=170, pos=(850,450), no_resize=True, no_title_bar=True):
    gui.add_text('Exiting...')

with gui.font_registry():
    defaultFont = gui.add_font("./fonts/Roboto-Regular.ttf", 18)
    titleFont = gui.add_font("./fonts/Roboto-Regular.ttf", 48)
    bigFont = gui.add_font("./fonts/Roboto-Regular.ttf", 72)
    gui.bind_font(defaultFont)
    gui.bind_item_font('exiting', titleFont)


with gui.viewport_menu_bar():
    gui.add_image('./images/favicon.png', height=35)
    with gui.menu(label="Game"):
        gui.add_menu_item(label="New Game", callback=callback_handler)
        gui.add_menu_item(label="Load Game", callback=callback_handler)
        gui.add_menu_item(label="Save", callback=callback_handler)
        gui.add_menu_item(label="Save As", callback=callback_handler)

    with gui.menu(label="Settings"):
        gui.add_menu_item(label="Player", callback=callback_handler)
        with gui.menu(label="Player 1"):
            gui.add_menu_item(label="Name", callback=callback_handler)
            gui.add_menu_item(label="Color", callback=callback_handler)
            gui.add_menu_item(label="Score", callback=callback_handler)
        gui.add_menu_item(label="Setting 1", callback=callback_handler, check=True)
        gui.add_menu_item(label="Setting 2", callback=callback_handler)

    gui.add_menu_item(label="Help", callback=callback_handler)

    gui.add_menu_item(label="Exit", callback=callback_handler)

with gui.window(tag="Main", pos=(0,80)):
    # Fix space occupied by top bar
    gui.add_spacer(height=12)
    gui.add_input_text(label="string", default_value="Quick brown fox", callback=callback_handler)
    gui.add_button(label='Send', callback=callback_handler)
    gui.add_slider_float(label="float", default_value=0.273, max_value=1)        

try:
    gui.set_viewport_small_icon('./favicon.ico')
except:
    Exception
# Start window maximized
gui.create_viewport(title='piDartboard', decorated=False, width=1920, height=1080)
gui.setup_dearpygui()
gui.show_viewport()
gui.set_primary_window('Main', True)
gui.maximize_viewport()
gui.start_dearpygui()
gui.destroy_context()