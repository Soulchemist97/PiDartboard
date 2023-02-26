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
from screeninfo import get_monitors # pip install screeninfo
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


# Set application information
app.setApplicationName("piDartboard.GUI")
app.setApplicationDisplayName(f"piDartboard - {__version__}")
app.setApplicationVersion(__version__)
app.setWindowIcon(QIcon(os.path.join(image_dir, "favicon.png")))
app.setStyle('Fusion')
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


# Register custom fonts
QFontDatabase.addApplicationFont(os.path.join(font_dir, "Roboto-Regular.ttf"))
QFontDatabase.addApplicationFont(os.path.join(font_dir, "Roboto-Bold.ttf"))


# Load images as pixmaps
dartL = QPixmap(os.path.join(image_dir, "dartL.png"))
dartR = QPixmap(os.path.join(image_dir, "dartR.png"))
dartboardI = QPixmap(os.path.join(image_dir, "dartboard.png"))
logoSmall = QPixmap(os.path.join(image_dir, "piDartboardLogoSmall.png"))


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

        # Menu bar actions
        MenubarGame_actionRestart = self.findChild(QAction, 'menubar_Game_actionRestart')
        MenubarGame_actionRestart.triggered.connect(self.Restart)
        MenubarGame_actionSave = self.findChild(QAction, 'menubar_Game_actionSave')
        MenubarGame_actionSave.triggered.connect(self.Save)
        MenubarGame_actionSaveAs = self.findChild(QAction, 'menubar_Game_actionSaveAs')
        MenubarGame_actionSaveAs.triggered.connect(self.SaveAs)
        MenubarGame_actionManualMode = self.findChild(QAction, 'menubar_Game_actionManualMode')
        MenubarGame_actionManualMode.setCheckable(True)
        MenubarGame_actionManualMode.triggered.connect(self.ManualMode)

        GameModes_action301 = self.findChild(QAction, 'menuGame_Modes_action301')
        GameModes_action301.setCheckable(True)
        GameModes_action301.triggered.connect(self.GameModeSwitch, 301)
        GameModes_action301.setChecked(True) # Set default game mode

        GameModes_action501 = self.findChild(QAction, 'menuGame_Modes_action501')
        GameModes_action501.setCheckable(True)
        GameModes_action501.triggered.connect(self.GameModeSwitch, 501)

        GameModes_action701 = self.findChild(QAction, 'menuGame_Modes_action701')
        GameModes_action701.setCheckable(True)
        GameModes_action701.triggered.connect(self.GameModeSwitch, 701)

        GameModes_SingleOut = self.findChild(QAction, 'menuGame_Modes_actionSingle_Out')
        GameModes_SingleOut.setCheckable(True)
        GameModes_SingleOut.triggered.connect(self.GameModeSwitch, "SingleOut")

        GameModes_DoubleOut = self.findChild(QAction, 'menuGame_Modes_actionDouble_Out')
        GameModes_DoubleOut.setCheckable(True)
        GameModes_DoubleOut.setChecked(True) # Set default game mode
        GameModes_DoubleOut.triggered.connect(self.GameModeSwitch, "DoubleOut")

        GameModes_MasterOut = self.findChild(QAction, 'menuGame_Modes_actionMaster_Out')
        GameModes_MasterOut.setCheckable(True)
        GameModes_MasterOut.triggered.connect(self.GameModeSwitch, "MasterOut")

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

        # Status bar
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Finished loading!")
        #dartboardImage = self.findChild(QGraphicsView, 'dartboardView')
        #dartboardImage.setPixmap(dartboardI) #Doesn't work!!!! FUCK!
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

    def PlayerManager_show(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Player Manager button!", 2000)

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

    def Save(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Save button!", 2000)

    def SaveAs(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Save As button!", 2000)

    def GameModeSwitch(self, mode):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage(f"Clicked Game Mode {mode} button!", 2000)

    def LanguageSettings(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Language button!", 2000)

    def PlayerPlaceholder(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Nothing happened...", 2000)

    def ManualMode(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Manual Mode button!", 2000)

    def Restart(self):
        StatusBar = self.findChild(QStatusBar, 'statusBar')
        StatusBar.showMessage("Clicked Restart button!", 2000)



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
    print(f"Primary Monitor: {MonitorWidth}x{MonitorHeight}")
    AppWindow = MainWindow()
    AppWindow.show()
    sys.exit(app.exec_())