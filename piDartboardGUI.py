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
import time
import dearpygui.dearpygui as gui
from screeninfo import get_monitors

#get Info about primary monitor
n = 0
MonitorInfo = []
for m in get_monitors():
    if m.is_primary:
        MonitorInfo = str(m)
        MonitorHeight = m.height
        MonitorWidth = m.width

gui.create_context()

def clicked():
    print('clicked on the dartboard')

def callback_handler(sender):
    print(f'{sender} was pressed')
    if sender == 'exitBtn':
        gui.configure_item("exiting", show=True)
        print('Exiting...')
        time.sleep(0.1)
        gui.destroy_context()
    if sender == 'langBtn':
        gui.configure_item("languageSelection", show=True)
        print('Language menu opened')
    if sender == 'langClose':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed')
    if sender == 'langOK':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed and language changed')

###
#Load Images
# Load favicon image into memory
faviconData = {}
faviconData = gui.load_image("./images/favicon.png")
with gui.texture_registry():
    print(f'Loading image: {faviconData=}')
    logoImage = gui.add_static_texture(width=faviconData[0], height=faviconData[1], default_value=faviconData[3], tag="logoImage")
# Load dartboard image into memory
dartboardData = {}
dartboardData = gui.load_image("./images/dartboard.png")
with gui.texture_registry():
    print(f'Loading image: {dartboardData=}')
    dartboardImage = gui.add_static_texture(width=dartboardData[0], height=dartboardData[1], default_value=dartboardData[3], tag="dartboardImage")
#
###

with gui.viewport_menu_bar():
    with gui.menu(label="Game"):
        gui.add_menu_item(label="New Game", callback=callback_handler)
        gui.add_menu_item(label="Load Game", callback=callback_handler)
        gui.add_menu_item(label="Save", callback=callback_handler)
        gui.add_menu_item(label="Save As", callback=callback_handler)
        gui.add_menu_item(label="Manual Mode", callback=callback_handler)
    with gui.menu(label="Settings"):
        gui.add_menu_item(label="Player", callback=callback_handler)
        with gui.menu(label="Player 1"):
            gui.add_menu_item(label="Name", callback=callback_handler)
            gui.add_menu_item(label="Color", callback=callback_handler)
            gui.add_menu_item(label="Score", callback=callback_handler)
    gui.add_menu_item(label="Language", tag='langBtn', callback=callback_handler)
    gui.add_menu_item(label="Help", tag='hlpBtn',callback=callback_handler)
    gui.add_menu_item(label="Exit", tag='exitBtn', callback=callback_handler)
    gui.add_text(f"piDartboard {__version__}", pos=(1780,0))
    gui.add_image(logoImage, height=20, width=20, pos=(1900,2))



with gui.window(tag="Main"):
    # Fix space occupied by top bar
    gui.add_spacer(height=13)
    with gui.group(tag="playerOverview", pos=(20,30)):
        with gui.group(horizontal=True, tag='CurrentPlayer'):
            gui.add_text("Jannis:", tag='currentPlayerItem')
            gui.add_text("301", tag='currentScoreItem')
        with gui.group(horizontal=True, tag='followingPlayers'):
            gui.add_text("Lino:")
            gui.add_text("301")
        with gui.group(horizontal=True, tag='followingPlayers2'):
            gui.add_text("Jan:")
            gui.add_text("301")
        with gui.group(horizontal=True, tag='followingPlayers3'):
            gui.add_text("Darc:")
            gui.add_text("301")
        with gui.group(horizontal=True):
            gui.add_button(label="Add player", tag='addPlr',callback=callback_handler)
            gui.add_button(label="Remove player", tag='rmvPlr', callback=callback_handler)
    gui.add_text(f'[DBG] Primary Monitor: {MonitorInfo}', pos=(5,1055))



# Even windows without borders have an invisible border of around 4px, resize wrapper window +8px to compensate
# Calculate dartboard position horizontally: windowWidth - dartboardWidth
# Calculate dartboard position vertically: windowHeight - dartboardHeight
dartboardW = 908
dartboardH = 908
dartboardPositionW = MonitorWidth - dartboardW + 3
dartboardPositionH = MonitorHeight - dartboardH + 3
# Dartboard should be fixed to the bottom right corner of the screen
with gui.window(tag="dartboard", pos=(dartboardPositionW,dartboardPositionH), width=dartboardW, height=dartboardH, no_title_bar=True, no_scrollbar=True, no_background=True, no_move=True, no_resize=True):
    gui.add_text(f'Last throw:', pos=(4,0))
    gui.add_image(dartboardImage, width=dartboardW-8, height=dartboardH-8, pos=(4,4))
    with gui.item_handler_registry():
        gui.add_item_clicked_handler(callback=clicked)
# gui.bind_item_handler_registry('dartboardClicked', 'dartboard')



# Language selection window
with gui.window(tag="languageSelection", show=False, width=250, height=150, pos=(800,400), no_resize=True):
    gui.add_text(' Select a language:')
    gui.add_combo(items=['English', 'Deutsch (German)'], tag='langCombo', callback=callback_handler)
    
    with gui.group(horizontal=True):
        gui.add_button(label="OK", tag='langOK', callback=callback_handler)
        gui.add_button(label="Cancel", tag='langClose', callback=callback_handler)



with gui.window(label="Exiting", show=False, id="exiting", width=170, pos=(850,450), no_resize=True, no_title_bar=True):
    gui.add_text('Exiting...')



# Set icon
try:
    gui.set_viewport_small_icon('./favicon.ico')
except:
    Exception


# Register fonts
with gui.font_registry():
    defaultFont = gui.add_font("./fonts/Roboto-Regular.ttf", 18)
    titleFont = gui.add_font("./fonts/Roboto-Regular.ttf", 48)
    bigFont = gui.add_font("./fonts/Roboto-Regular.ttf", 72)
    currentPlayerFont = gui.add_font("./fonts/Roboto-Regular.ttf", 84)
    currentPlayerScoreFont = gui.add_font("./fonts/Roboto-Regular.ttf", 108)
    gui.bind_font(defaultFont)
    gui.bind_item_font('exiting', titleFont)
    gui.bind_item_font('dartboard', titleFont)
    gui.bind_item_font('currentPlayerItem', currentPlayerFont)
    gui.bind_item_font('currentScoreItem', currentPlayerScoreFont)
    gui.bind_item_font('followingPlayers', titleFont)
    gui.bind_item_font('followingPlayers2', titleFont)
    gui.bind_item_font('followingPlayers3', titleFont)



# Start window maximized
gui.create_viewport(title='piDartboard', decorated=False, width=1920, height=1080)
gui.setup_dearpygui()
gui.show_viewport()
gui.set_primary_window('Main', True)
gui.maximize_viewport()
gui.start_dearpygui()
gui.destroy_context()