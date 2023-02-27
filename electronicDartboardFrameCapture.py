#!/usr/bin/env python3

__doc__ = "electronicDartboardFrameCapture: Map the interface matrix of an electronic dartboard to csv and pickle."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Stable"

import colorama as cc
import pickle
import RPi.GPIO as GPIO

###TODO###TODO###TODO###TODO###TODO##############################
## Edge case detection: if the listener matrix is set and the sender matrix is all nil and stuck in second loop. Timeout event?
## Automatic process of naming frame data after a specific list with possibility to correct last frame or to abort. Maybe even save and load a project?
## Save finished matrixMap to a pickle file for improved reading speed as well als a readable csv and provide a conversion tool between the two.
## Detect if not run on RPi

#NOTE############################################################
# We need the following free RPi GPIO pins:
# [11,GPIO17;12,GPIO18;13,GPIO27;15,GPIO22;29,GPIO5;31,GPIO6;33,GPIO13;35,GPIO19;37,GPIO26;16,GPIO23;18,GPIO24;22,GPIO25;32,GPIO12;36,GPIO16;38,GPIO20;40,GPIO21]
# Half of them should send a signal to the upper matrix layer
# Half of them should listen on the pins of the lower matrix layer
#
# IMOPRTANT:
#   You have to wire up the GPIO pins the same way to the upper and lower dartboard matrix you wire them up later as a finished game machine. We wired the SenderPins to the lower matrix layer and the ListenerPins to the upper matrix layer. But you obviously don't have to do it like us.
#
# Our Wiring:
#                                               [upper dartboard input matrix layer]
#   [lower dartboard input matrix layer]            [1] [2] [3] [4] [5] [6] [7] [8]
#     [1] [2] [3] [4] [5] [6] [7] [8]                |   |   |   |   |   |   |   |
#      |   |   |   |   |   |   |   |                 |   |   |   |   |   |   |   |
#     [11][12][13][15][16][18][29][22]              [31][32][33][35][36][37][38][40]
#   [                             RaspberryPi3 GPIO                                ]

GPIOMODE = GPIO.BOARD
freeGPIOSenderPins = [11,12,13,15,16,18,22,29]
freeGPIOListenerPins = [31,32,33,35,36,37,38,40]
pinHigh = 1
pinLow = 0

#Initialize console colors
cc.init()
lightGrey = cc.Fore.LIGHTBLACK_EX
white = cc.Fore.LIGHTWHITE_EX
red = cc.Fore.LIGHTRED_EX
green = cc.Fore.LIGHTGREEN_EX
yellow = cc.Fore.LIGHTYELLOW_EX
reset = cc.Style.RESET_ALL

def splash():
    #Display a splash screen once at initial startup
    print("""
    electronicDartsFrameCapture: Map the interface matrix of an electronic dartboard to csv and pickle.
    """)

def frameNameInput():
    #This part of the script calls for a user input of the tile that is about to be pressed
    #For us things like 't20' or 'be' worked just fine
    #It is later saved to a pickle file
    print(f'Please specify a name for the frame that is being captured: {green}', end=f'{reset}')
    frameName = input()
    print(f'{lightGrey}Frame: {frameName}{reset}')
    return frameName

def RPiGPIOSetup(frameName):

    ### Set Raspberry Pi GPIO pins to capture dartboard segment matrix data for each tile pressed ###
    GPIO.setmode(GPIOMODE)

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

    # Get a reference matrix when nothing is pressed (startup)
    referenceMatrix = []
    for pin in freeGPIOListenerPins:
        referenceMatrix.append(GPIO.input(pin))
    print(f'{lightGrey}Reference Matrix: {referenceMatrix}{reset}')
    return referenceMatrix

def getListenerMatrix(referenceMatrix):
    #Grab listener matrix by checking for changes on the GPIO pin signals
    #Example output is: [0, 0, 0, 1, 0, 0, 0, 0]
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
    return listenerMatrix,listenerMatrixIndex

def getSenderMatrix(referenceMatrix, listenerMatrixIndex):
    #Grab sender matrix by checking for changes on the GPIO pin voltages of the defined listener pin
    #Example output is: [0, 0, 1, 0, 0, 0, 0, 0]
    #Example return is the index of above output: 2
    #Reminder: index starts at 0!
    senderMatrix = []
    while True:
        for pin in freeGPIOSenderPins:
            GPIO.output(pin, GPIO.LOW)
            GPIO.output(pin, GPIO.HIGH)
            senderMatrix.append(GPIO.input(freeGPIOListenerPins[listenerMatrixIndex]))
            if not senderMatrix == referenceMatrix:
                GPIO.output(pin, GPIO.LOW)
                continue
            else:
                senderMatrix = []
                GPIO.output(pin, GPIO.LOW)
        print(f"{green}You're good!{reset}")
        break
    return senderMatrix

def cleanUp():
    print(f'{lightGrey}Cleaning up...{reset}')
    for pin in freeGPIOSenderPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass
    for pin in freeGPIOListenerPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass

####SaveFileFormat n=Number=1
###o1;[senderMatrix];[listenerMatrix]
#Outer Ring(n)
###i1;[senderMatrix];[listenerMatrix]
#Inner Ring(n)
###d1;[senderMatrix];[listenerMatrix]
#Double Ring
###t1;[senderMatrix];[listenerMatrix]
#Triple Ring
###be;[senderMatrix];[listenerMatrix]
#Bulls-Eye
###dbe;[senderMatrix];[listenerMatrix]
#Double Bulls-Eye

if __name__ == "__main__":
    #runOnce
    splash()
    while True:
        #runRepeatedly
        frameName = frameNameInput()
        referenceMatrix = RPiGPIOSetup(frameName)
        listenerMatrix,listenerMatrixIndex = getListenerMatrix(referenceMatrix)
        senderMatrix = getSenderMatrix(referenceMatrix, listenerMatrixIndex)
        print(f'{lightGrey}Listener matrix and index for {yellow}{frameName}{lightGrey}: {green}{listenerMatrix}{lightGrey}Index: {green}{listenerMatrixIndex}{reset}')
        print(f'{lightGrey}Sender matrix for {yellow}{frameName}{lightGrey}: {green}{senderMatrix}{reset}')
        # save mapping to a csv file
        with open("DartboardCapture.csv","a") as file:
            print(f'{lightGrey}Saving to DartboardCapture.csv{reset}')
            file.write(f"{frameName};{str(senderMatrix)};{str(listenerMatrix)}\n")
        cleanUp()
        print('\n')