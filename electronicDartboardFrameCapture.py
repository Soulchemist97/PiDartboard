#!/usr/bin/env python3

__doc__ = "electronicDartboardFrameCapture: A Python library for electronic dart board interfaces."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.0"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Development"

import colorama as cc
import RPi.GPIO as GPIO
import time

# We need the following free RPi GPIO pins 
# [1,3v3;39,Ground;11,GPIO17;12,;13,GPIO27;15,GPIO22;29,GPIO5;31,GPIO6;33,GPIO13;35,GPIO19;37,GPIO26;16,GPIO23;18,GPIO24;22,GPIO25;32,GPIO12;36,GPIO16;38,GPIO20;40,GPIO21]
# Half of them should send a signal to the upper matrix layer
# Half of them should listen on the pins of the lower matrix layer   
freeGPIOSenderPins = [11,12,13,15,16,18,22,29]
freeGPIOListenerPins = [31,32,33,35,36,37,38,40]
pinHigh = 1
pinLow = 0


def consoleColorSetup():
    #initialize console colors
    cc.init()
    global lightGrey
    global white
    global red
    global green
    global yellow
    global reset
    lightGrey = cc.Fore.LIGHTBLACK_EX
    white = cc.Fore.LIGHTWHITE_EX
    red = cc.Fore.LIGHTRED_EX
    green = cc.Fore.LIGHTGREEN_EX
    yellow = cc.Fore.LIGHTYELLOW_EX
    reset = cc.Style.RESET_ALL

def help():
    #display splash screen
    print("""
    pyDartsFrameCapture: A Python library for electronic dart board interfaces.
    This is a library for capturing frames of the dart board matrix interface.
    """)

def frameCaptureNameInput():
    #manage user inputs
    print('Please input a name for the frame that is being captured: '+ green, end='')
    frameName = input()
    datetimeCompact = time.strftime("%Y%m%d_%H%M%S")
    frameName = frameName.replace(' ', '_')
    frameName = f'{frameName}_pyDartsFrame-{datetimeCompact}'
    print(f'{lightGrey}Set frame name: {frameName}{reset}')
    return frameName

def RPiGPIOSetup(frameName):

    ### Set Raspberry Pi GPIO pins to capture dartboard segment matrix data for each tile pressed ###
    GPIO.setmode(GPIO.BOARD)

    # Set up GPIO pins:
    ####Sender
    print(f'{lightGrey}Setting up sender GPIO pins{reset}')
    for pin in freeGPIOSenderPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass
        GPIO.setup(pin, GPIO.OUT)

    ####Listener
    print(f'{lightGrey}Setting up listener GPIO pins{reset}')
    for pin in freeGPIOListenerPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    # while loop to send signals to the upper matrix layer and compare to reference matrix to 
    referenceMatrix = []
    for pin in freeGPIOListenerPins:
        referenceMatrix.append(GPIO.input(pin))
    print(f'{lightGrey}Reference Matrix: {referenceMatrix}{reset}')
    return referenceMatrix
    
def getListenerMatrix(referenceMatrix):
    #Grab listener matrix by checking for changes on the GPIO pin voltages
    #Example output is: [0,0,0,1,0,0,0,0]
    #Example return is the index of above output: 3
    #Reminder: Index starts at 0!
    print(f'{lightGrey}Sending signals to upper matrix layer{reset}')
    for pin in freeGPIOSenderPins:
        GPIO.output(pin, GPIO.HIGH)

    print(f'{lightGrey}Listening on lower matrix layer...{reset}')
    print(f'{red}Please hold the button until further notice!{reset}')
    listenerMatrix = []
    while True:
        listenerMatrix = [GPIO.input(pin) for pin in freeGPIOListenerPins]
        if not listenerMatrix == referenceMatrix:
            print(f'{green}* Change detected{reset}')
            print(f'{lightGrey}Listener matrix for {yellow}{frameName}{lightGrey}: {green}{listenerMatrix}{reset}')
            break
        else:
            listenerMatrix = []
    listenerMatrixIndex = listenerMatrix.index(pinHigh)
    return listenerMatrixIndex

def getSenderMatrix(referenceMatrix, listenerMatrixIndex):
    #Grab sender matrix by checking for changes on the GPIO pin voltages of the defined listener pin
    #Example output is: [0,0,0,1,0,0,0,0]
    #Example return is the index of above output: 3
    #Reminder: index starts at 0!
    senderMatrix = []
    while True:
        for pin in freeGPIOSenderPins:
            GPIO.output(pin, GPIO.LOW) 
            GPIO.output(pin, GPIO.HIGH)
            for lpin in freeGPIOListenerPins:
                senderMatrix.append(GPIO.input(lpin))

            if not senderMatrix == referenceMatrix:
                print(f"{green}You're good!{reset}")
                print(f'{lightGrey}Sender matrix for {yellow}{frameName}{lightGrey}: {green}{senderMatrix}{reset} at SenderPin {yellow}{pin}{reset}')
                continue
            else:
                senderMatrix = []
        break
    senderMatrixIndex = senderMatrix.index(pinHigh)
    return senderMatrixIndex
    
def analyzeMatrices(senderMatrix, listenerMatrix):
    #analyze matrices given by previous functions
    listenerIndex = f'{yellow}Position: [{senderMatrix.index(pinHigh)}/{listenerMatrix.index(pinHigh)}]{reset}'
    print(listenerIndex)
        
def cleanUp():
    print(f'{lightGrey}Cleaning up...{reset}')
    for pin in freeGPIOSenderPins:
        GPIO.cleanup(pin)
    for pin in freeGPIOListenerPins:
        GPIO.cleanup(pin)

if __name__ == "__main__":
    #runOnce
    consoleColorSetup()
    help()
    while True:
        #runRepeatedly
        frameName = frameCaptureNameInput()
        referenceMatrix = RPiGPIOSetup(frameName)
        listenerMatrixIndex = getListenerMatrix(referenceMatrix)
        print(f'{green}Listener matrix index: {listenerMatrixIndex}{reset}')
        #senderMatrixIndex = getSenderMatrix(referenceMatrix)
        #matrixCoords = analyzeMatrices(senderMatrixIndex, listenerMatrixIndex)
        cleanUp()
        print('\n')
