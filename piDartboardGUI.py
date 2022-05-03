#!/usr/bin/env python3

__doc__ = "piDartboardGUI: GUI for the piDartboard project."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Development"


# Imports
import os
import time
import dearpygui.dearpygui as gui
from screeninfo import get_monitors
from Player_Manager import ScoreBoard


###
# Create DearPyGui context
gui.create_context()
###


###
# Set current working directory
cwd = os.getcwd()
###


# Variable initialization
currentConfig = {}

player1 = {
    "name": "Jannis",
    "score": 301,
    "id": 1
}
player2 = {
    "name": "Lino",
    "score": 301,
    "id": 2
}
player3 = {
    "name": "Jan",
    "score": 301,
    "id": 3
}
player4 = {
    "name": "Darc",
    "score": 301,
    "id": 4
}

players = [player1, player2, player3, player4]

currentPlayerIdRotation = [1, 2, 3, 4]
currentPlayerName = player1["name"]
currentPlayerScore = player1["score"]


###
# Get information about primary monitor
n = 0
MonitorInfo = []
for m in get_monitors():
    if m.is_primary:
        MonitorInfo = str(m)
        MonitorHeight = m.height
        MonitorWidth = m.width
#
###


###
# Proceed to next player
def proceedToNextPlayer():
    currentPlayerIdRotation.append(currentPlayerIdRotation.pop(0))
    currentPlayerName = players[currentPlayerIdRotation[0] - 1]["name"]
    currentPlayerScore = players[currentPlayerIdRotation[0] - 1]["score"]
    return currentPlayerName, currentPlayerScore, currentPlayerIdRotation
###


###
# Handle outside signals
def outsideSignal_handler(signal):
    print(f'Signal received: {signal}')
    if signal == 'skipToNextPlayer':
        pass
###


###
# Handle all events
def callback_handler(sender):
    print(f'{sender} was pressed')

    ### Main Window Buttons ###
    # Exit Button
    if sender == 'gameExitNow':
        gui.configure_item("exiting", show=True)
        print('Exiting...')
        time.sleep(0.1)
        gui.destroy_context()
    
    # Language Button
    if sender == 'gameLanguage':
        currentConfig = gui.get_item_configuration("languageSelection")
        if currentConfig['show'] == True:
            gui.configure_item("languageSelection", show=False)
            print('Language menu was open, closed')
        else:
            gui.configure_item("languageSelection", show=True)
            print('Language menu opened')
    # Language Menu - Close Button
    if sender == 'langClose':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed')
    # Language Menu - OK Button
    if sender == 'langOK':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed and language changed')
    
    # MainWindow - Player Manager Button
    if sender == 'playerManagerButton':
        currentConfig = gui.get_item_configuration("playerManagerWindow")
        if currentConfig['show'] == True:
            gui.configure_item("playerManagerWindow", show=False)
            print('Player manager was open, closed')
        else:
            gui.configure_item("playerManagerWindow", show=True)
            print('Player manager opened')
    
    # Settings - Player Manager Button
    if sender == 'togglePlayerManager':
        currentConfig = gui.get_item_configuration("playerManagerWindow")
        if currentConfig['show'] == True:
            gui.configure_item("playerManagerWindow", show=False)
            print('Player manager was open, closed')
        else:
            gui.configure_item("playerManagerWindow", show=True)
            print('Player manager opened')
    
    # Player Manager - Close Button
    if sender == 'playerManagerCloseBtn':
        gui.configure_item("playerManagerWindow", show=False)

    # Test trigger for experimental functions
    if sender == 'testTrigger':
        gui.configure_item("collectDarts", show=True)
        currentPlayerName, currentPlayerScore, currentPlayerIdRotation = proceedToNextPlayer()
        print(f'Current player: {currentPlayerName}: {currentPlayerScore} {currentPlayerIdRotation}')
        time.sleep(3)
        gui.configure_item("collectDarts", show=False)
###


###
# Refresh all shown windows
def refreshWindows():
    pass
###


###
# Load Images
# load dartL image into memory
dartL = {}
dartL = gui.load_image('./images/dartL.png')
with gui.texture_registry():
    print(f'Loading image: {dartL=}')
    dartL = gui.add_static_texture(width=dartL[0], height=dartL[1], default_value=dartL[3], tag="dartL")
# load dartR image into memory
dartR = {}
dartR = gui.load_image('./images/dartR.png')
with gui.texture_registry():
    print(f'Loading image: {dartR=}')
    dartR = gui.add_static_texture(width=dartR[0], height=dartR[1], default_value=dartR[3], tag="dartR")
# load favicon image into memory
faviconData = {}
faviconData = gui.load_image("./images/favicon.png")
with gui.texture_registry():
    print(f'Loading image: {faviconData=}')
    logoImage = gui.add_static_texture(width=faviconData[0], height=faviconData[1], default_value=faviconData[3], tag="logoImage")
# load dartboard image into memory
dartboardData = {}
dartboardData = gui.load_image("./images/dartboard.png")
with gui.texture_registry():
    print(f'Loading image: {dartboardData=}')
    dartboardImage = gui.add_static_texture(width=dartboardData[0], height=dartboardData[1], default_value=dartboardData[3], tag="dartboardImage")
###


###
# Menu bar
with gui.viewport_menu_bar():
    with gui.menu(label="Game"):
        gui.add_menu_item(label="Restart", tag='restartGame', callback=callback_handler)
        gui.add_menu_item(label="Save", tag='saveGame', callback=callback_handler)
        gui.add_menu_item(label="Save As", tag='saveGameAs', callback=callback_handler)
        gui.add_menu_item(label="Manual Mode", tag='manualGameMode', callback=callback_handler)
        with gui.menu(label="Game Modes"):
            gui.add_menu_item(label="301", tag='GameMode301', callback=callback_handler)
            gui.add_menu_item(label="501", tag='GameMode501', callback=callback_handler)
            gui.add_menu_item(label="701", tag='GameMode701', callback=callback_handler)
            gui.add_menu_item(label="Double Out", tag='GameModeDoubleOut', default_value=True, check=True, callback=callback_handler)
    with gui.menu(label="Settings"):
        gui.add_menu_item(label="Player Manager", tag='togglePlayerManager', callback=callback_handler)
        #Quick settings for each player if possible
        for player in players:
            with gui.menu(label=player["name"]):
                gui.add_menu_item(label="Edit name", tag=f'settingsPlayer{player["id"]}NameEdit', callback=callback_handler)
                gui.add_menu_item(label="Edit score", tag=f'settingsPlayer{player["id"]}ScoreEdit', callback=callback_handler)
                gui.add_menu_item(label="Remove from game", tag=f'settingsPlayer{player["id"]}Remove', callback=callback_handler)
                gui.add_menu_item(label="Make current player", tag=f'settingsPlayer{player["id"]}MakeCurrentPlayer', callback=callback_handler)
        # with gui.menu(label=f"{player1['name']}"):
        #     gui.add_menu_item(label=f"Edit name", tag='Player1_NameSettings', callback=callback_handler)
        #     gui.add_menu_item(label="Edit score", tag='Player1_ScoreSettings', callback=callback_handler)
        
    gui.add_menu_item(label="Language", tag='gameLanguage', callback=callback_handler)
    gui.add_menu_item(label="Help", tag='gameHelp',callback=callback_handler)
    gui.add_menu_item(label="Exit", tag='gameExitNow', callback=callback_handler)
    gui.add_spacer(width=55)
    gui.add_menu_item(label="TestTrigger", tag='testTrigger', callback=callback_handler)
    gui.add_text(f"piDartboard {__version__}", pos=(1780,0), color=(255,255,255,60))
    gui.add_image(logoImage, height=20, width=20, pos=(1900,2))
###


###
# Main window
with gui.window(tag="Main"):
    # Fix space occupied by top bar
    gui.add_spacer(height=13)
    # Draw overlay to highlight current player
    with gui.drawlist(width=15, height=400, pos=(4,45)):
        with gui.draw_layer():
            gui.draw_line((3, 0), (3, 100), color=(0, 255, 0, 255), thickness=8)
            gui.draw_arrow(p1=(4, 175), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            gui.draw_arrow(p1=(4, 210), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            gui.draw_arrow(p1=(4, 245), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            gui.draw_arrow(p1=(4, 280), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
    with gui.group(tag="playerOverview", pos=(20,30)):
        with gui.group(horizontal=True, tag='CurrentPlayer'):
            gui.add_text(f"{currentPlayerName}:", tag='currentPlayerItem')
            gui.add_text(f"{currentPlayerScore}", tag='currentScoreItem')
        with gui.group(horizontal=True, tag='followingPlayers'):
            gui.add_text(f" {player2['name']}:")
            gui.add_text(f"{player2['score']}")
        with gui.group(horizontal=True, tag='followingPlayers2'):
            gui.add_text(f" {player3['name']}:")
            gui.add_text(f"{player3['score']}")
        with gui.group(horizontal=True, tag='followingPlayers3'):
            gui.add_text(f" {player4['name']}:")
            gui.add_text(f"{player4['score']}")
        with gui.group(horizontal=True):
            gui.add_button(label="Player Manager", tag='playerManagerButton', callback=callback_handler)
            gui.add_button(label="Edit", tag="mainEditButton", callback=callback_handler)
    gui.add_text(f'[DBG] Primary Monitor: {MonitorInfo}', pos=(5,1055))
###


###
# Dartboard
# Even windows without borders have an invisible border of around 4px, resize wrapper window +8px to compensate
# Calculate dartboard position horizontally: windowWidth - dartboardWidth
# Calculate dartboard position vertically: windowHeight - dartboardHeight
dartboardW = 908
dartboardH = 908
dartboardPositionW = MonitorWidth - dartboardW + 3
dartboardPositionH = MonitorHeight - dartboardH + 3
# Dartboard should be fixed to the bottom right corner of the screen
with gui.window(tag="dartboard", pos=(dartboardPositionW,dartboardPositionH), width=dartboardW, height=dartboardH, no_title_bar=True, no_scrollbar=True, no_background=True, no_move=True, no_resize=True):
    gui.add_image(dartboardImage, width=dartboardW-8, height=dartboardH-8, pos=(4,4))
# gui.bind_item_handler_registry('dartboardClicked', 'dartboard')
###


###
# Dartboard overlay
# Draw overlay to highlight current throw
dartboardMiddleW = dartboardW/2 - 8
dartboardMiddleH = dartboardH/2 - 8
dartboardMiddlePos = (dartboardMiddleW, dartboardMiddleH)
with gui.window(tag="dartboardOverlay", pos=(dartboardPositionW,dartboardPositionH), width=dartboardW, height=dartboardH, no_title_bar=True, no_scrollbar=True, no_background=True, no_move=True, no_resize=True):
    # draw circle on overlay where the dart hit
    gui.draw_circle(center=dartboardMiddlePos, radius=10, color=(0,255,0,255), thickness=2)
    # draw cross in circle
    gui.draw_line((dartboardMiddlePos[0]-7, dartboardMiddlePos[1]-7), (dartboardMiddlePos[0]+7, dartboardMiddlePos[1]+7), color=(0,255,0,255), thickness=2)
    gui.draw_line((dartboardMiddlePos[0]+7, dartboardMiddlePos[1]-7), (dartboardMiddlePos[0]-7, dartboardMiddlePos[1]+7), color=(0,255,0,255), thickness=2)
    # point arrow to circle
    gui.draw_arrow(p1=(dartboardMiddlePos[0] + 8, dartboardMiddlePos[1] + 8), p2=(dartboardMiddlePos[0] + 50, dartboardMiddlePos[1] + 50), color=(100,255,255,255), thickness=5)
###


###
# Dartboard Info Widget
# Dartboart throw info window should translate over the dartboard
dartboardInfoPositionW = MonitorWidth - dartboardW
dartboardInfoPositionH = MonitorHeight - dartboardH - 155
with gui.window(tag="dartboardInfo", pos=(dartboardInfoPositionW,dartboardInfoPositionH), width=dartboardW, height=dartboardH, no_title_bar=True, no_scrollbar=True, no_background=True, no_move=True, no_resize=True):
    with gui.group(horizontal=True, pos=(4,0)):
        with gui.group(horizontal=True, pos=(0,20)):
            gui.add_text('Remaining:')
            gui.add_image(dartL, tag='throw1', width=50, height=50)
            gui.add_image(dartL, tag='throw2', width=50, height=50)
            gui.add_image(dartL, tag='throw3', width=50, height=50)
        gui.add_spacer(width=60)
        gui.add_text('Last throw:')
        gui.add_text('{throwInfo}')
    with gui.group(horizontal=False, tag='throwOverview', pos=(4,80)):
        gui.add_text('1.: {throw1}')
        gui.add_text('2.: {throw2}')
        gui.add_text('3.: {throw3}')
###


###
# Player Manager
# Player manager window should be a pop-up style window in the middle of the screen
playerManagerW = 500
playerManagerH = 600
playerManagerPositionW = MonitorWidth/2 - playerManagerW/2
playerManagerPositionH = MonitorHeight/2 - playerManagerH/2
with gui.window(label='Player Manager', tag="playerManagerWindow", show=False, pos=(playerManagerPositionW,playerManagerPositionH), width=playerManagerW, height=playerManagerH, no_resize=True):
    with gui.group(horizontal=False, pos=(5,30)):
        for player in players:
            with gui.group(horizontal=True):
                gui.add_text(f'{player["name"]}:')
                gui.add_text(f'{player["score"]}')
                gui.add_button(label='Edit', tag=f'playerManagerPlayer{player["id"]}Edit', callback=callback_handler)
    with gui.group(horizontal=True, pos=(playerManagerW/20,playerManagerH-45)):
        gui.add_button(label=" Add player ", tag='playerManagerAddPlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=" Remove player ", tag='playerManagerRemovePlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=" Edit player ", tag='playerManagerEditPlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=' Close ', tag='playerManagerCloseBtn', callback=callback_handler)


###
# Language selection window
with gui.window(tag="languageSelection", show=False, width=250, height=118, pos=(800,400), no_resize=True, no_scrollbar=True):
    gui.add_text('Select a language:', pos=(8,26))
    gui.add_combo(items=['English', 'Deutsch (German)'], tag='langCombo', width=235, pos=(8,55), callback=callback_handler)
    
    with gui.group(horizontal=True, pos=(135,86)):
        gui.add_button(label=" OK ", tag='langOK', callback=callback_handler)
        gui.add_button(label=" Cancel ", tag='langClose', callback=callback_handler)
###


###
# Collect your darts window
collectDartsW = 800
collectDartsH = 180
collectDartsPositionW = MonitorWidth / 2- collectDartsW 
collectDartsPositionH = (MonitorHeight + 20) / 2 - collectDartsH + 120
dartImageResponsiveSideLength = collectDartsH - 20
with gui.window(tag="collectDarts", show=False, width=collectDartsW, height=collectDartsH, pos=(collectDartsPositionW,collectDartsPositionH), no_resize=True, no_scrollbar=True, no_title_bar=True):
    with gui.group(horizontal=True, tag='collectDartsGroup'):
        gui.add_image(dartL, width=dartImageResponsiveSideLength, height=dartImageResponsiveSideLength, pos=(10,10))
        gui.add_text('Please collect your darts!', pos=(collectDartsW/4.7,collectDartsH/5.35))
        gui.add_image(dartR, width=dartImageResponsiveSideLength, height=dartImageResponsiveSideLength, pos=(collectDartsW-(dartImageResponsiveSideLength+10),10))
###


###
# Exit tooltip
with gui.window(label="Exiting", show=False, id="exiting", width=300, pos=(800,450), no_resize=True, no_title_bar=True, no_move=True):
    gui.add_spacer(height=40)
    gui.add_text('  Exiting...', pos=(4,0))
###


###
# Fonts
with gui.font_registry():
    robotoDefault18 = gui.add_font("./fonts/Roboto-Regular.ttf", 18)
    robotoTitle36 = gui.add_font("./fonts/Roboto-Regular.ttf", 36)
    robotoTitle48 = gui.add_font("./fonts/Roboto-Regular.ttf", 48)
    robotoBig72 = gui.add_font("./fonts/Roboto-Regular.ttf", 72)
    robotoGiant108 = gui.add_font("./fonts/Roboto-Regular.ttf", 108)
    gui.bind_font(robotoDefault18)
    gui.bind_item_font('exiting', robotoBig72)
    gui.bind_item_font('dartboard', robotoTitle48)
    gui.bind_item_font('dartboardInfo', robotoTitle48)
    gui.bind_item_font('currentPlayerItem', robotoGiant108)
    gui.bind_item_font('currentScoreItem', robotoGiant108)
    gui.bind_item_font('followingPlayers', robotoTitle48)
    gui.bind_item_font('followingPlayers2', robotoTitle48)
    gui.bind_item_font('followingPlayers3', robotoTitle48)
    gui.bind_item_font('throwOverview', robotoTitle36)
    gui.bind_item_font('collectDartsGroup', robotoTitle48)
###


###
# Set app icon
try:
    gui.set_viewport_small_icon('./images/favicon.ico')
except:
    Exception
###


# Start window maximized
gui.create_viewport(title='piDartboard', decorated=False, width=1920, height=1080)
gui.setup_dearpygui()
gui.show_viewport()
gui.set_primary_window('Main', True)
gui.maximize_viewport()
gui.start_dearpygui()
gui.destroy_context()