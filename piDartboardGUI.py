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
import json
import dearpygui.dearpygui as gui
from screeninfo import get_monitors
from Player_Manager import ScoreBoard


### Player Management Object / Class
SB = ScoreBoard() #{"PlayerName": {"Throws": [[],[]], "Score": 0}}

SB.addPlayer("Mathusan")
SB.addPlayer("ThisLimn0")
SB.addPlayer("Jan B")

SB.Throw(5)
SB.Throw(15)
###


### Create DearPyGui context ###
gui.create_context()
###


###
# Set current working directory
cwd = os.getcwd()
# Set directories for language files, images and fonts
languageDir = "./languages/"
imageDir = "./images/"
fontDir = "./fonts/"
applicationDefaults = "appDefaults.json"
langD = os.path.join(cwd, languageDir)
imgD = os.path.join(cwd, imageDir)
fontD = os.path.join(cwd, fontDir)
#print(langD)
###


###
# Load application default settings from file
def loadAppDefaults():
    if os.path.isfile(applicationDefaults) == True:
        with open(applicationDefaults, 'r') as f:
            appDefaults = json.load(f)
    else:
        with open(applicationDefaults, 'w') as file:
            appDefaults = {
                "language": "English",
            }
            json.dump(appDefaults, file, indent=4)
    return appDefaults
###

###
# Look for language files in the current working directory
def findLanguageFiles():
    languageFiles = []
    for file in os.listdir(languageDir):
        if file.endswith(".lang"):
            # load language name from within the file
            localLanguageName = json.load(open(f"{languageDir}{file}"))["localLanguageName"]
            languageFiles.append(localLanguageName)
            languageFiles.append(file)
    if languageFiles == []:
        print("No language files found!")
        return False
    return languageFiles
languageFiles = findLanguageFiles()
###


###
# Variable initialization
currentConfig = {}
gameModeSingle = {}
gameModeDouble = {}
gameModeMaster = {}
players = SB.PlayerNames
###


###
# Get information about primary monitor
n = 0
MonitorInfo = []
try:
    for m in get_monitors():
        if m.is_primary:
            MonitorInfo = str(m)
            MonitorHeight = m.height
            MonitorWidth = m.width
            n += 1
    if n == 0:
        print("No primary monitor found!")
except:
    print("No monitor found! Setting default values.")
    MonitorWidth = 1920
    MonitorHeight = 1080
    pass
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
def callback_handler(sender, callback_type, callback_id, value):
    print(f'{sender} was pressed')
    if callback_type != 'None':
        print(f'Callback: {callback_type} with id {callback_id} and value {value}')

    ##### Debug Code
    if sender == 'refreshWindow':
        print(sender,"was pressed")
        refreshWindows()

    if sender == "DebugPoints":
        print(sender,"was pressed")
        SB.Throw(5)
        refreshWindows()


    if sender == "NextPlayer":
        SB.TogglePlayer()
        refreshWindows()
        print(SB.PlayerNames)

    if sender == "ResetThrows":
        SB.ResetCurrentThrow()
        refreshWindows()
    #### Debug Code


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

    # Game Menu - Game Modes - Out check
    if sender == 'GameModeSingleOut':
        # get all current configurations
        gameModeSingle = gui.get_value("GameModeSingleOut")
        gameModeDouble = gui.get_value("GameModeDoubleOut")
        gameModeMaster = gui.get_value("GameModeMasterOut")
        print(f"[DBG] {gameModeSingle}, {gameModeDouble}, {gameModeMaster}")
        if gameModeDouble == True:
            gui.set_value("GameModeDoubleOut", False)
            print('[DBG] GameModeDoubleOut was active, deactivated')
        if gameModeMaster == True:
            gui.set_value("GameModeMasterOut", False)
            print('[DBG] GameModeMasterOut was active, deactivated')
        gui.set_value("GameModeSingleOut", True)
        print('[DBG] GameModeSingleOut is now active')
    if sender == 'GameModeDoubleOut':
        # get all current configurations
        gameModeSingle = gui.get_value("GameModeSingleOut")
        gameModeDouble = gui.get_value("GameModeDoubleOut")
        gameModeMaster = gui.get_value("GameModeMasterOut")
        # check if the desired mode is already active
        if gameModeSingle == True:
            gui.set_value("GameModeSingleOut", False)
        if gameModeMaster == True:
            gui.set_value("GameModeMasterOut", False)
        gui.set_value("GameModeDoubleOut", True)
        print('[DBG] GameModeDoubleOut is now active')
    if sender == 'GameModeMasterOut':
        # get all current configurations
        gameModeSingle = gui.get_value("GameModeSingleOut")
        gameModeDouble = gui.get_value("GameModeDoubleOut")
        gameModeMaster = gui.get_value("GameModeMasterOut")
        # check if the desired mode is already active
        if gameModeSingle == True:
            gui.set_value("GameModeSingleOut", False)
        if gameModeDouble == True:
            gui.set_value("GameModeDoubleOut", False)
        gui.set_value("GameModeMasterOut", True)
        print('[DBG] GameModeMasterOut is now active')
    # Language Menu - Close Button
    if sender == 'langClose':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed')
    # Language Menu - OK Button
    if sender == 'langOK':
        gui.configure_item("languageSelection", show=False)
        print('Language menu closed and language changed')

    # Help Button
    if sender == 'gameHelp':
        currentConfig = gui.get_item_configuration("helpWindow")
        if currentConfig['show'] == True:
            gui.configure_item("helpWindow", show=False)
            print('Help menu was open, closed')
        else:
            gui.configure_item("helpWindow", show=True)
            print('Help menu opened')

    # MainWindow - Add Player Button
    if sender == 'mainWindowAddPlayer':
        currentConfig = gui.get_item_configuration("playerManagerAddPlayerWindow")
        if currentConfig['show'] == True:
            gui.configure_item("playerManagerAddPlayerWindow", show=False)
            print('Add Player menu was open, closed')
        else:
            gui.configure_item("playerManagerAddPlayerWindow", show=True)
            print('Add Player menu opened')

    # MainWindow - Remove Player Button
    if sender == 'mainWindowRemovePlayer':
        currentConfig = gui.get_item_configuration("playerManagerRemovePlayerWindow")
        if currentConfig['show'] == True:
            gui.configure_item("playerManagerRemovePlayerWindow", show=False)
            print('Remove Player menu was open, closed')
        else:
            gui.configure_item("playerManagerRemovePlayerWindow", show=True)
            print('Remove Player menu opened')

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

    # Player Manager - Add Player Button
    if sender == 'playerManagerAddPlayer':
        gui.configure_item("playerManagerAddPlayerWindow", show=True)
        print('Player manager add player window opened')

    # Player Manager - Remove Player Button
    if sender == 'playerManagerRemovePlayer':
        gui.configure_item("playerManagerRemovePlayerWindow", show=True)
        print('Player manager remove player window opened')

    # Player Manager - Add Player - Close Button
    if sender == 'playerManagerAddPlayerCancelBtn':
        gui.configure_item("playerManagerAddPlayerWindow", show=False)
        print('Player manager add player window closed')

    # Player Manager - Add Player - Add Button
    if sender == 'playerManagerAddPlayerBtn':
        AddPlayerName = gui.get_value("playerManagerAddPlayerName")
        if AddPlayerName != "":
            SB.addPlayer(AddPlayerName)
            gui.configure_item("playerManagerAddPlayerName", default_value='')
            gui.configure_item("playerManagerAddPlayerWindow", show=False)
            print(f'Player {AddPlayerName} was added, Player Manager Add Player window closed')
        else:
            print('Player name cannot be empty')

    # Player Manager - Remove Player - Remove Button
    if sender == 'playerManagerRemovePlayerBtn':
        RemovePlayerName = gui.get_value("playerManagerRemovePlayerName")
        if RemovePlayerName != "":
            SB.removePlayer(RemovePlayerName)
            print(f'Player {RemovePlayerName} was removed, Remove Player window closed')

    # Player Manager - Remove Player - Cancel Button
    if sender == 'playerManagerRemovePlayerCancelBtn':
        gui.configure_item("playerManagerRemovePlayerWindow", show=False)
        print('Remove Player window closed')


    # Test trigger for experimental functions
    if sender == 'testTrigger':
        gui.configure_item("collectDarts", show=True)
        currentPlayerName, currentPlayerScore, currentPlayerIdRotation = proceedToNextPlayer()
        print(f'Current player: {currentPlayerName}: {currentPlayerScore} {currentPlayerIdRotation}')
        time.sleep(3)
        gui.set_value("currentPlayerItem", f"{currentPlayerName}: ")
        gui.set_value("currentPlayerScore", currentPlayerScore)
        for id in overviewWindowItems:
            currentPlayerOnOverview = currentPlayerIdRotation[id - 1]
            for players in currentPlayerIdRotation:
                if not players == currentPlayerIdRotation[0]:
                    gui.set_value(f"followingPlayer{id}Name", f' {currentPlayerOnOverview["name"]}:')
                    gui.set_value(f"followingPlayer{id}Score", f'{currentPlayerOnOverview["score"]}')
        print('Updated GUI')
        gui.configure_item("collectDarts", show=False)
        gui.set_value("DebugBox", str(SB))

    if sender == 'playerManagerAddPlayer' :
        SB.addPlayer(gui.get_value('AddPlayerBox'))
        print(SB)
###


###
# Refresh all shown windows
def refreshWindows():
    # Refresh main window

    Tag_Value = {
    "throw1Text": f'1.: {SB.CurrentThrow_Round(1)}',
    "throw2Text": f'2.: {SB.CurrentThrow_Round(2)}',
    "throw3Text": f'3.: {SB.CurrentThrow_Round(3)}',
    "roundScoreItem": f'{SB.CurrentRoundPoints()}',
    "currentPlayerItem": f"{SB.getActivePlayer()}:",
    "currentScore": SB.getActivePlayerScore(),
    "followingPlayer1Item": players[1],
    "followingPlayer2Item": players[2],
    "followingPlayer1Score": SB.getPlayerScore(players[1]),
    "followingPlayer2Score": SB.getPlayerScore(players[2]),
    }

    for tag, value in Tag_Value.items():
        gui.set_value(tag, value)
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
            gui.add_separator()
            gui.add_menu_item(label="Single Out", tag='GameModeSingleOut', default_value=False, check=True, callback=callback_handler)
            gui.add_menu_item(label="Double Out", tag='GameModeDoubleOut', default_value=True, check=True, callback=callback_handler)
            gui.add_menu_item(label="Master Out", tag='GameModeMasterOut', default_value=False, check=True, callback=callback_handler)
    with gui.menu(label="Settings"):
        gui.add_menu_item(label="Player Manager", tag='togglePlayerManager', callback=callback_handler)
        #Quick settings for each player if possible
        for player in players:
            with gui.menu(label=player):
                gui.add_menu_item(label="Edit name", tag=f'settingsPlayer{player}NameEdit', callback=callback_handler)
                gui.add_menu_item(label="Edit score", tag=f'settingsPlayer{player}ScoreEdit', callback=callback_handler)
                gui.add_menu_item(label="Remove from game", tag=f'settingsPlayer{player}Remove', callback=callback_handler)
                gui.add_menu_item(label="Make current player", tag=f'settingsPlayer{player}MakeCurrentPlayer', callback=callback_handler)
        # with gui.menu(label=f"{player1['name']}"):
        #     gui.add_menu_item(label=f"Edit name", tag='Player1_NameSettings', callback=callback_handler)
        #     gui.add_menu_item(label="Edit score", tag='Player1_ScoreSettings', callback=callback_handler)

    gui.add_menu_item(label="Language", tag='gameLanguage', callback=callback_handler)
    gui.add_menu_item(label="Help", tag='gameHelp',callback=callback_handler)
    gui.add_menu_item(label="Exit", tag='gameExitNow', callback=callback_handler)

    ### Debug Menu
    with gui.menu(label="DebugWindow"):
        gui.add_menu_item(label="Refresh", tag='refreshWindow', callback=callback_handler)
        gui.add_menu_item(label="DebugPoints",tag="DebugPoints" ,callback=callback_handler)
        gui.add_menu_item(label="NextPlayer",tag="NextPlayer", callback=callback_handler)
        gui.add_menu_item(label="ResetThrows",tag="ResetThrows", callback=callback_handler)


    gui.add_spacer(width=55)
    gui.add_menu_item(label="TestTrigger", tag='testTrigger', callback=callback_handler)
    gui.add_text(f"piDartboard {__version__}", pos=(1780,0), color=(255,255,255,60))
    gui.add_image(logoImage, height=20, width=20, pos=(1900,2))
###


###
# Main window
with gui.window(tag="Main", no_scrollbar=True):
    # Fix space occupied by top bar
    gui.add_spacer(height=13)
    # Draw overlay to highlight current player
    with gui.drawlist(width=15, height=800, pos=(4,45)):
        with gui.draw_layer():
            gui.draw_line((3, 0), (3, 145), color=(0, 255, 0, 255), thickness=8)
            arrowTopBase = 0
            iterator = 100
            iteratorPlus = 110
            i = 1
            #generate arrows bottom up for each player except current player
            for player in players[1:]:
                i+=1
                gui.draw_arrow(p1=(4,arrowTopBase+i*iterator), p2=(4,arrowTopBase+iteratorPlus+i*iterator), color=(255, 255, 255, 255), thickness=6)
                # gui.draw_arrow(p1=(4, arrowTopBase+(players.index(player)+1)*iterator), p2=(4, arrowTopBase+2*iterator) , )
            # gui.draw_arrow(p1=(4, 175), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            # gui.draw_arrow(p1=(4, 210), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            # gui.draw_arrow(p1=(4, 245), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
            # gui.draw_arrow(p1=(4, 280), p2=(4, 135), color=(255, 255, 255, 255), thickness=4)
    # for players in currentPlayerIdRotation:
    #     with gui.group(tag='playerOverview', pos=(20,30)):
    #         if players == currentPlayerIdRotation[0]:
    #             # Draw current player
    #             with gui.group(horizontal=True, tag='CurrentPlayer'):
    #                 gui.add_text(f"{currentPlayerName}:", tag='currentPlayerItem')
    #                 gui.add_text(f"{currentPlayerScore}", tag='currentScoreItem')
    #         else:
    #             # Draw following players
    #             with gui.group(horizontal=True, tag=f'FollowingPlayer{players}'):
    #                 gui.add_text(f'{players["name"]}:', tag=f'FollowingPlayer{players["id"]}Item')
    #                 gui.add_text(f'{players["score"]}', tag=f'FollowingPlayer{str({players["id"]})}ScoreItem')
    with gui.group(tag="playerOverview", pos=(20,30)):

        with gui.group(horizontal=True, tag='CurrentPlayer'):

            gui.add_text(f"{SB.getActivePlayer()}: ", tag='currentPlayerItem')
            gui.add_text(f"{SB.getActivePlayerScore()}", tag='currentScoreItem')

        # for entries in overviewWindowItems:
        #     with gui.group(horizontal=True, tag=f'followingPlayer{entries}'):
        #         playerFStringHelper=f'player{entries}'
        #         gui.add_text(f"{playerFStringHelper['name']}:", tag=f'followingPlayer{entries}Item')
        #         gui.add_text(f'{entries}', tag=f'followingPlayer{entries}Score')
        with gui.group(horizontal=True, tag='followingPlayers1'):
            gui.add_text(f" {players[1]}: ", tag='followingPlayer1Item', color=(255,255,255,230))
            gui.add_text(f"{SB.getPlayerScore(players[1])}", tag='followingPlayer1Score', color=(255,255,255,230))
        with gui.group(horizontal=True, tag='followingPlayers2'):
            gui.add_text(f" {players[2]}: ", tag='followingPlayer2Item', color=(255,255,255,190))
            gui.add_text(f"{SB.getPlayerScore(players[2])}", tag='followingPlayer2Score', color=(255,255,255,190))

        gui.add_spacer(height=10)
        with gui.group(horizontal=True, tag='mainWindowButtons'):
            gui.add_button(label="  +  ", tag='mainWindowAddPlayer', callback=callback_handler)
            gui.add_spacer(width=5)
            gui.add_button(label="  -  ", tag='mainWindowRemovePlayer', callback=callback_handler)
            gui.add_spacer(width=5)
            gui.add_button(label=" Player Manager ", tag='playerManagerButton', callback=callback_handler)
            gui.add_spacer(width=5)
            gui.add_button(label=" Edit ", tag="mainEditButton", callback=callback_handler)

    gui.add_text(f'[DBG] {str(SB)}', pos=(5,1055),tag="DebugBox")
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
    gui.draw_circle(center=dartboardMiddlePos, radius=10, color=(0,255,0,255), thickness=3)
    # draw cross in circle
    gui.draw_line((dartboardMiddlePos[0]-7, dartboardMiddlePos[1]-7), (dartboardMiddlePos[0]+7, dartboardMiddlePos[1]+7), color=(0,255,0,255), thickness=2)
    gui.draw_line((dartboardMiddlePos[0]+7, dartboardMiddlePos[1]-7), (dartboardMiddlePos[0]-7, dartboardMiddlePos[1]+7), color=(0,255,0,255), thickness=2)
    # point arrow to circle
    # gui.draw_arrow(p1=(dartboardMiddlePos[0] + 8, dartboardMiddlePos[1] + 8), p2=(dartboardMiddlePos[0] + 50, dartboardMiddlePos[1] + 50), color=(100,255,255,255), thickness=5)
###


###
# Dartboard Info Widget
# Dartboart throw info window should translate over the dartboard
dartboardInfoPositionW = MonitorWidth - dartboardW
dartboardInfoPositionH = MonitorHeight - dartboardH - 155
with gui.window(tag="dartboardInfo", pos=(dartboardInfoPositionW,dartboardInfoPositionH), width=dartboardW, height=dartboardH, no_title_bar=True, no_scrollbar=True, no_background=True, no_move=True, no_resize=True):
    with gui.group(horizontal=False, pos=(dartboardW/3-10,10), tag="dartboardInfoGroup"):
        gui.add_spacer(height=20)
        gui.add_text(f'Round Score: {SB.CurrentRoundPoints()}')
        gui.add_spacer(height=10)
        with gui.group(horizontal=True, tag="dartboardInfoRounds"):
            gui.add_text(f'1.: {SB.CurrentThrow_Round(1)}',tag='throw1Text')
            gui.add_spacer(width=50)
            gui.add_text(f'2.: {SB.CurrentThrow_Round(2)}',tag='throw2Text')
            gui.add_spacer(width=50)
            gui.add_text(f'3.: {SB.CurrentThrow_Round(3)}',tag='throw3Text')
        with gui.group(horizontal=True):
            # gui.add_text('Remaining:')

            gui.add_image(dartR, tag='throw1Pic', width=75, height=75, pos=(dartboardW-245,20))
            gui.add_image(dartR, tag='throw2Pic', width=75, height=75, pos=(dartboardW-170,20))
            gui.add_image(dartR, tag='throw3Pic', width=75, height=75, pos=(dartboardW-90,20))
            gui.add_image(dartR, tag='throw1ShotPic', width=75, height=75, pos=(dartboardW-245,20), tint_color=(255,255,255,80))
            gui.add_image(dartR, tag='throw2ShotPic', width=75, height=75, pos=(dartboardW-170,20), tint_color=(255,255,255,80))
            gui.add_image(dartR, tag='throw3ShotPic', width=75, height=75, pos=(dartboardW-90,20), tint_color=(255,255,255,80))
            gui.add_text(f'SHOTS REMAINING', tag='dartboardInfoRemaining', pos=(dartboardW-145,100), color=(255,255,255,60))
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
                gui.add_text(f'{player}:')
                gui.add_text(f'{SB.ScoreCalculation(player)}')
                gui.add_button(label='Edit', tag=f'playerManagerPlayer{player}Edit', callback=callback_handler)

        gui.add_input_text(tag='AddPlayerBox', callback=callback_handler) # Eingabe Box

    with gui.group(horizontal=True, pos=(playerManagerW/20,playerManagerH-45)):
        gui.add_button(label=" Add player ", tag='playerManagerAddPlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=" Remove player ", tag='playerManagerRemovePlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=" Edit player ", tag='playerManagerEditPlayer', callback=callback_handler)
        gui.add_spacer(width=15)
        gui.add_button(label=' Close ', tag='playerManagerCloseBtn', callback=callback_handler)
###


###
# Player Manager Add Player Window
# Player manager add player window should be a pop-up style window in the middle of the screen
playerManagerAddPlayerW = 400
playerManagerAddPlayerH = 200
playerManagerAddPlayerPositionW = MonitorWidth/2 - playerManagerAddPlayerW/2
playerManagerAddPlayerPositionH = MonitorHeight/2 - playerManagerAddPlayerH/2
with gui.window(tag="playerManagerAddPlayerWindow", show=False, pos=(playerManagerAddPlayerPositionW,playerManagerAddPlayerPositionH), width=playerManagerAddPlayerW, height=playerManagerAddPlayerH, no_resize=True, no_title_bar=True):
    with gui.group(horizontal=False, pos=(5,4)):
        gui.add_text('               Add Player')
        gui.add_input_text(tag='playerManagerAddPlayerName', hint='Name', width=playerManagerAddPlayerW-10)
    with gui.group(horizontal=True, pos=(4,playerManagerAddPlayerH-55)):
        gui.add_spacer(width=60)
        gui.add_button(label="  Add  ", tag='playerManagerAddPlayerBtn', callback=callback_handler)
        gui.add_spacer(width=20)
        gui.add_button(label=" Cancel ", tag='playerManagerAddPlayerCancelBtn', callback=callback_handler)
###


###
# Player Manager Remove Player Window
# Player manager remove player window should be a pop-up style window in the middle of the screen
playerManagerRemovePlayerW = 200
playerManagerRemovePlayerH = 100
playerManagerRemovePlayerPositionW = MonitorWidth/2 - playerManagerRemovePlayerW/2
playerManagerRemovePlayerPositionH = MonitorHeight/2 - playerManagerRemovePlayerH/2
with gui.window(label='Remove Player', tag="playerManagerRemovePlayerWindow", show=False, pos=(playerManagerRemovePlayerPositionW,playerManagerRemovePlayerPositionH), width=playerManagerRemovePlayerW, height=playerManagerRemovePlayerH, no_resize=True, no_title_bar=True):
    with gui.group(horizontal=False, pos=(5,4)):
        gui.add_text(' Remove Player:')
        playerList = []
        for player in players:
            playerList.append(player)
        gui.add_combo(items=playerList, tag=f'playerManagerRemovePlayerCombo', width=190, callback=callback_handler)
    with gui.group(horizontal=True, pos=(4,playerManagerRemovePlayerH-35)):
        gui.add_spacer(width=20)
        gui.add_button(label=" Remove ", tag='playerManagerRemovePlayerBtn', callback=callback_handler)
        gui.add_spacer(width=10)
        gui.add_button(label=" Cancel ", tag='playerManagerRemovePlayerCancelBtn', callback=callback_handler)


###
# Language selection window
LanguageSelectionWindowW = 250
LanguageSelectionWindowH = 118
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
# Help window
HelpWindowW = 1200
HelpWindowH = 800
with gui.window(label="Help", tag="helpWindow", show=False, width=1200, height=800, pos=(100,100), no_resize=True,):
    gui.add_text(f'piDartboard Version: {__version__} - Help Document', pos=(5,22))
###


###
# Exit tooltip
ExitTooltipW = 300
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
    robotoGiant100 = gui.add_font("./fonts/Roboto-Regular.ttf", 100)
    robotoGiant170 = gui.add_font("./fonts/Roboto-Regular.ttf", 170)
    robotoGiantBold170 = gui.add_font("./fonts/Roboto-Bold.ttf", 170)
    gui.bind_font(robotoDefault18)
    gui.bind_item_font('mainWindowButtons', robotoTitle36)
    gui.bind_item_font('exiting', robotoBig72)
    gui.bind_item_font('dartboard', robotoTitle48)
    gui.bind_item_font('dartboardInfo', robotoTitle48)
    gui.bind_item_font('currentPlayerItem', robotoGiant170)
    gui.bind_item_font('currentScoreItem', robotoGiantBold170)
    gui.bind_item_font('followingPlayers1', robotoGiant100)
    gui.bind_item_font('followingPlayers2', robotoGiant100)
    # gui.bind_item_font('followingPlayers3', robotoGiant100)
    # gui.bind_item_font('followingPlayers4', robotoGiant100)
    # gui.bind_item_font('followingPlayers5', robotoGiant100)
    # gui.bind_item_font('followingPlayers6', robotoGiant100)
    # gui.bind_item_font('followingPlayers7', robotoGiant100)
    gui.bind_item_font('dartboardInfoGroup', robotoTitle48)
    gui.bind_item_font('dartboardInfoRounds', robotoTitle36)
    gui.bind_item_font('collectDartsGroup', robotoTitle48)
    gui.bind_item_font('dartboardInfoRemaining', robotoDefault18)
    gui.bind_item_font('playerManagerAddPlayerWindow', robotoTitle36)
###



###
# Set app icon
try:
    gui.set_viewport_small_icon('./images/favicon.ico')
except:
    Exception
###


# Start window maximized
gui.create_viewport(title='piDartboard', decorated=False, width=MonitorWidth, height=MonitorHeight)
gui.setup_dearpygui()
gui.show_viewport()
gui.set_primary_window('Main', True)
gui.maximize_viewport()
gui.start_dearpygui()
gui.destroy_context()