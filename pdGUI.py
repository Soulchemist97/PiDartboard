#!/usr/bin/env python3

__doc__ = "piDartboardGUI: GUI for the piDartboard project."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Development"

# Imports
import os
import sys
import time
import json
from PyQt5.QtCore import * # pip install PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from tkinter import Tk # pip install tkinter
from Player_Manager import ScoreBoard

print("piDartboardGUI: GUI for the piDartboard project.")

# Create QApplication object
app = QApplication([])


# Global Variables
cwd = os.getcwd() # Current Working Directory
language_dir = os.path.join(cwd, "languages\\") # Language files
image_dir = os.path.join(cwd, "images\\") # Image files
font_dir = os.path.join(cwd, "fonts\\") # Font files
ui_dir = os.path.join(cwd, "ui\\") # PyQt5 ui files
application_defaults = os.path.join(cwd, "appDefaults.json") # Application defaults
game_is_running = False # Game flag


# Set application information
app.setApplicationName("piDartboard.GUI")
app.setApplicationDisplayName(f"piDartboard")
app.setApplicationVersion(__version__)
app.setWindowIcon(QIcon(os.path.join(image_dir, "favicon.png")))
app.setStyle('Breeze')
app.setFont(QFont("Roboto", 10))


# Load application default settings from file
def load_application_defaults():
    if os.path.isfile(application_defaults) == True:
        with open(application_defaults, 'r') as f:
            app_defaults = json.load(f)
    else:
        with open(application_defaults, 'w') as file:
            app_defaults = {
                "language": "English",
            }
            json.dump(app_defaults, file, indent=4)
    return app_defaults
#app_defaults = load_application_defaults()


# Look for language files in the current working directory
def find_language_files():
    language_files = []
    for file in os.listdir(language_dir):
        if file.endswith(".lang"):
            # load language name from within the file
            local_language_name = json.load(open(f"{language_dir}{file}"))["localLanguageName"]
            international_language_name = json.load(open(f"{language_dir}{file}"))["internationalLanguageName"]
            language_files.append(local_language_name + " (" + international_language_name + ")")
            language_files.append(file)
    if language_files == []:
        print("No language files found!")
        return False
    return language_files
language_files = find_language_files()


# Get information about primary monitor
Screen = QDesktopWidget().screenGeometry()
screen_width = Screen.width()
screen_height = Screen.height()
screen_center = QDesktopWidget().availableGeometry().center()


# Register custom fonts
QFontDatabase.addApplicationFont(os.path.join(font_dir, "Roboto-Regular.ttf"))
QFontDatabase.addApplicationFont(os.path.join(font_dir, "Roboto-Bold.ttf"))


# Load images as pixmaps
dartL = QPixmap()
dartL.load(os.path.join(image_dir, "dartL.png"))
dartR = QPixmap()
dartR.load(os.path.join(image_dir, "dartR.png"))
dartboardI = QImage()
dartboardI.load(os.path.join(image_dir, "dartboard.png"))
logoSmall = QPixmap()
logoSmall.load(os.path.join(image_dir, "piDartboardLogoSmall.png"))


# Player manager dialog
class PlayerManager(QDialog):

    def __init__(self):
        super(PlayerManager,self).__init__()
        uic.loadUi(os.path.join(ui_dir, "PlayerManager.ui"), self)
        self.setWindowTitle("Player Manager")


# Main window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(os.path.join(ui_dir, "MainWindow.ui"), self)
        self.setWindowTitle("Game Setup")

        # Connect menu bar actions
        MenubarGame_actionRestart = self.findChild(QAction, 'menubar_Game_actionRestart')
        MenubarGame_actionRestart.triggered.connect(self.Restart)
        MenubarGame_actionRestart.setStatusTip("Restart the game (all unsaved data will be lost)")

        MenubarGame_actionLoad = self.findChild(QAction, 'menubar_Game_actionLoad')
        MenubarGame_actionLoad.triggered.connect(self.Load)
        MenubarGame_actionLoad.setStatusTip("Load a saved game")

        MenubarGame_actionSave = self.findChild(QAction, 'menubar_Game_actionSave')
        MenubarGame_actionSave.triggered.connect(self.Save)
        MenubarGame_actionSave.setStatusTip("Save your current game")
        MenubarGame_actionSave.setShortcut("F5")

        MenubarGame_actionSaveAs = self.findChild(QAction, 'menubar_Game_actionSaveAs')
        MenubarGame_actionSaveAs.triggered.connect(self.SaveAs)
        MenubarGame_actionSaveAs.setStatusTip("Save your current game at a custom location")

        MenubarGame_actionManualMode = self.findChild(QAction, 'menubar_Game_actionManualMode')
        MenubarGame_actionManualMode.setCheckable(True)
        MenubarGame_actionManualMode.triggered.connect(self.ManualMode)
        MenubarGame_actionManualMode.setStatusTip("Enable manual shot input mode")

        GameModes_action301 = self.findChild(QAction, 'menuGame_Modes_action301')
        GameModes_action301.setCheckable(True)
        GameModes_action301.triggered.connect(lambda: self.GameModeSwitch("301", game_is_running))
        GameModes_action301.setChecked(True) # Set default game mode

        GameModes_action501 = self.findChild(QAction, 'menuGame_Modes_action501')
        GameModes_action501.setCheckable(True)
        GameModes_action501.triggered.connect(lambda: self.GameModeSwitch("501", game_is_running))

        GameModes_action701 = self.findChild(QAction, 'menuGame_Modes_action701')
        GameModes_action701.setCheckable(True)
        GameModes_action701.triggered.connect(lambda: self.GameModeSwitch("701", game_is_running))

        GameModes_SingleOut = self.findChild(QAction, 'menuGame_Modes_actionSingle_Out')
        GameModes_SingleOut.setCheckable(True)
        GameModes_SingleOut.triggered.connect(lambda: self.GameModeSwitch("SingleOut", game_is_running))

        GameModes_DoubleOut = self.findChild(QAction, 'menuGame_Modes_actionDouble_Out')
        GameModes_DoubleOut.setCheckable(True)
        GameModes_DoubleOut.setChecked(True) # Set default game mode
        GameModes_DoubleOut.triggered.connect(lambda: self.GameModeSwitch("Double Out", game_is_running))

        GameModes_MasterOut = self.findChild(QAction, 'menuGame_Modes_actionMaster_Out')
        GameModes_MasterOut.setCheckable(True)
        GameModes_MasterOut.triggered.connect(lambda: self.GameModeSwitch("MasterOut", game_is_running))

        # Transform checkable actions into radio buttons
        ActionGroupGameModeScoring = QActionGroup(self)
        ActionGroupGameModeScoring.addAction(GameModes_action301)
        ActionGroupGameModeScoring.addAction(GameModes_action501)
        ActionGroupGameModeScoring.addAction(GameModes_action701)
        ActionGroupGameMode = QActionGroup(self)
        ActionGroupGameMode.addAction(GameModes_SingleOut)
        ActionGroupGameMode.addAction(GameModes_DoubleOut)
        ActionGroupGameMode.addAction(GameModes_MasterOut)

        MenubarSettings_Undo = self.findChild(QAction, 'menubar_Settings_actionUndo')
        MenubarSettings_Undo.triggered.connect(self.UndoAction)
        MenubarSettings_Redo = self.findChild(QAction, 'menubar_Settings_actionRedo')
        MenubarSettings_Redo.triggered.connect(self.RedoAction)
        MenubarSettings_Language = self.findChild(QAction, 'menubar_Settings_actionLanguage')
        MenubarSettings_Language.triggered.connect(self.LanguageSettings)
        MenubarSettings_PlayerManager = self.findChild(QAction, 'menubar_Settings_actionPlayerManager')
        MenubarSettings_PlayerManager.triggered.connect(self.PlayerManager_show)
        MenubarSettings_PlayerPlaceholder = self.findChild(QAction, 'menubar_Settings_actionPlayerPlaceholder')
        MenubarSettings_PlayerPlaceholder.triggered.connect(self.PlayerPlaceholder)

        # Load dartboard image
        dartboardImage = self.findChild(QLabel, 'dartboardView')
        dartboardImage.setGeometry(screen_width - 820, screen_height - 910, 800, 800) #x, y, width, height
        dartboardImageFile = QPixmap()
        dartboardImageFile.load(os.path.join(image_dir, "dartboard.png"))
        dartboardImage.setScaledContents(True)
        dartboardImage.setPixmap(dartboardImageFile)

        # Load shot indicators
        shot_file = QPixmap()
        shot_file.load(os.path.join(image_dir, "dartR.png"))
        shot_one = self.findChild(QLabel, 'Shot1Indicator')
        shot_two = self.findChild(QLabel, 'Shot2Indicator')
        shot_three = self.findChild(QLabel, 'Shot3Indicator')
        shot_x_base = screen_width - 110 # outer x position of the shots - 1920-120=1800
        shot_one.setGeometry(shot_x_base - 135, 5, 100, 100) #x, y, width, height
        shot_two.setGeometry(shot_x_base - 70, 5, 100, 100) #x, y, width, height
        shot_three.setGeometry(shot_x_base, 5, 100, 100) #x, y, width, height
        shot_one.setScaledContents(True)
        shot_two.setScaledContents(True)
        shot_three.setScaledContents(True)
        shot_one.setPixmap(shot_file)
        shot_two.setPixmap(shot_file)
        shot_three.setPixmap(shot_file)

        shots_remaining = self.findChild(QLabel, 'darts_ShotsRemaining')
        shots_remaining.setGeometry(screen_width - 180, 60, 200, 120) #x, y, width, height
        shots_remaining.setFont(QFont('Roboto', 14, QFont.Bold))
        shots_remaining.opacity_effect = QGraphicsOpacityEffect()
        shots_remaining.opacity_effect.setOpacity(0.4)
        shots_remaining.setGraphicsEffect(shots_remaining.opacity_effect)

        # Player data
        CurrentPlayerLabel = self.findChild(QLabel, 'CurrentPlayer')
        CurrentPlayerLabel.setFont(QFont('Roboto', 60))
        CurrentPlayerLabel.setGeometry(20, 0, 550, 200) #x, y, width, height
        CurrentScoreLabel = self.findChild(QLabel, 'CurrentScore')
        CurrentScoreLabel.setFont(QFont('Roboto', 60, QFont.Bold))
        CurrentScoreLabel.setGeometry(550, 0, 500, 200) #x, y, width, height

        PlayerScoreAreaX = screen_width - 850
        PlayerScoreAreaY = 15
        PlayerRoundScoreLabel = self.findChild(QLabel, 'RoundScoreLabel')
        PlayerRoundScoreLabel.setFont(QFont('Roboto', 25))
        PlayerRoundScoreLabel.setGeometry(PlayerScoreAreaX, PlayerScoreAreaY, 200, 30) #x, y, width, height
        PlayerRoundScoreCumulativeLabel = self.findChild(QLabel, 'RoundScoreCumulated')
        PlayerRoundScoreCumulativeLabel.setFont(QFont('Roboto', 25, QFont.Bold))
        PlayerRoundScoreCumulativeLabel.setGeometry(PlayerScoreAreaX + 210, PlayerScoreAreaY, 200, 30) #x, y, width, height

        PlayerRoundOneScoreLabel = self.findChild(QLabel, 'RoundScoreFirstLabel')
        PlayerRoundOneScoreLabel.setFont(QFont('Roboto', 18))
        PlayerRoundOneScoreLabel.setGeometry(PlayerScoreAreaX, PlayerScoreAreaY + 40, 200, 30) #x, y, width, height
        PlayerRoundOneScoreNumberLabel = self.findChild(QLabel, 'RoundScoreFirstThrow')
        PlayerRoundOneScoreNumberLabel.setFont(QFont('Roboto', 18, QFont.Bold))
        PlayerRoundOneScoreNumberLabel.setGeometry(PlayerScoreAreaX + 60, PlayerScoreAreaY + 40, 200, 30) #x, y, width, height
        PlayerRoundTwoScoreLabel = self.findChild(QLabel, 'RoundScoreSecondLabel')
        PlayerRoundTwoScoreLabel.setFont(QFont('Roboto', 18))
        PlayerRoundTwoScoreLabel.setGeometry(PlayerScoreAreaX, PlayerScoreAreaY + 80, 200, 30) #x, y, width, height
        PlayerRoundTwoScoreNumberLabel = self.findChild(QLabel, 'RoundScoreSecondThrow')
        PlayerRoundTwoScoreNumberLabel.setFont(QFont('Roboto', 18, QFont.Bold))
        PlayerRoundTwoScoreNumberLabel.setGeometry(PlayerScoreAreaX + 60, PlayerScoreAreaY + 80, 200, 30) #x, y, width, height
        PlayerRoundThreeScoreLabel = self.findChild(QLabel, 'RoundScoreThirdLabel')
        PlayerRoundThreeScoreLabel.setFont(QFont('Roboto', 18))
        PlayerRoundThreeScoreLabel.setGeometry(PlayerScoreAreaX, PlayerScoreAreaY + 120, 200, 30) #x, y, width, height
        PlayerRoundThreeScoreNumberLabel = self.findChild(QLabel, 'RoundScoreThirdThrow')
        PlayerRoundThreeScoreNumberLabel.setFont(QFont('Roboto', 18, QFont.Bold))
        PlayerRoundThreeScoreNumberLabel.setGeometry(PlayerScoreAreaX + 60, PlayerScoreAreaY + 120, 200, 30) #x, y, width, height

        NextPlayerLabel = self.findChild(QLabel, 'UpcomingPlayerCombo')
        NextPlayerLabel.setFont(QFont('Roboto', 40))
        NextPlayerLabel.setGeometry(25, 100, 650, 200) #x, y, width, height
        NextPlayerLabel.opacity_effect = QGraphicsOpacityEffect()
        NextPlayerLabel.opacity_effect.setOpacity(0.8)
        NextPlayerLabel.setGraphicsEffect(NextPlayerLabel.opacity_effect)

        UpcomingPlayerLabel = self.findChild(QLabel, 'UpcomingPlayerAfterCombo')
        UpcomingPlayerLabel.setFont(QFont('Roboto', 40))
        UpcomingPlayerLabel.setGeometry(25, 180, 650, 200) #x, y, width, height
        UpcomingPlayerLabel.opacity_effect = QGraphicsOpacityEffect()
        UpcomingPlayerLabel.opacity_effect.setOpacity(0.8)
        UpcomingPlayerLabel.setGraphicsEffect(UpcomingPlayerLabel.opacity_effect)

        PlayerManagerShowButton = self.findChild(QPushButton, 'MainWindowButtonPlayerManager')
        PlayerManagerShowButton.clicked.connect(self.PlayerManager_show)
        PlayerAddButton = self.findChild(QPushButton, 'MainWindowButtonAddPlayer')
        PlayerAddButton.clicked.connect(self.AddPlayer)
        PlayerRemoveButton = self.findChild(QPushButton, 'MainWindowButtonRemovePlayer')
        PlayerRemoveButton.clicked.connect(self.RemovePlayer)
        PlayerEditButton = self.findChild(QPushButton, 'MainWindowButtonEditPlayer')
        PlayerEditButton.clicked.connect(self.EditPlayer)
        UndoButton = self.findChild(QPushButton, 'MainWindowButtonRevertAction')
        UndoButton.clicked.connect(self.UndoAction)

        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage(f"Finished loading! - PiDartboard v{__version__} - Monitor1: {screen_width}x{screen_height}")

    def PlayerManager_show(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Player Manager button!", 2000)
        self.PlayerManager = PlayerManager()
        self.PlayerManager.show()

    def AddPlayer(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Add Player button!", 2000)

    def RemovePlayer(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Remove Player button!", 2000)

    def EditPlayer(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Edit Player button!", 2000)

    def UndoAction(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Undo button!", 2000)

    def RedoAction(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Redo button!", 2000)

    def Load(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Load button!", 2000)

    def Save(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Save button!", 2000)

    def SaveAs(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Save As button!", 2000)

    def GameModeSwitch(self, modeswitch, game_is_running):
        if game_is_running:
            StatusBar = self.findChild(QStatusBar, 'statusBar')
            StatusBar.showMessage("You cannot change the game mode while a game is running!", 2000)
            return
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage(f"Clicked Game Mode {modeswitch} button!", 2000)
        game_is_running = True

    def LanguageSettings(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Language button!", 2000)

    def PlayerPlaceholder(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Nothing happened...", 2000)
        self.CurrentPlayerStatus()

    def ManualMode(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Manual Mode button!", 2000)

    def Restart(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Restart button!", 2000)

    def CurrentPlayerStatus(self):
        StatusLine = self.findChild(QLine, 'CurrentPlayerStatusLine')



# Tester
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = False

        self.button = QPushButton('change the colors of the buttons', self)
        self.button.clicked.connect(self.click)
        lay = QVBoxLayout(self)
        lay.addWidget(self.button)

        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor(3, 18, 14))

        self.palette.setColor(QPalette.Button, QColor('red'))

        self.setPalette(self.palette)

    def click(self):
        print("click")
        if not self.flag:
            self.palette.setColor(QPalette.Button, QColor(62, 80, 91))
        else:
            self.palette.setColor(QPalette.Button, QColor(0, 0, 128))

        self.setPalette(self.palette)
        self.flag = not self.flag




if __name__ == "__main__":
    print(f"Available Languages: {language_files}")
    AppWindow = MainWindow()
    AppWindow.showMaximized()
    sys.exit(app.exec_())