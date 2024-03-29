#!/usr/bin/env python3

__doc__ = "piDartboardRuntime: A Python runtime as translator between electronic dartboard matrix and Raspberry Pi."
__author__ = "ThisLimn0, Soulchemist97"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ThisLimn0, Soulchemist97"
__status__ = "Development"

###TODO###TODO###TODO###TODO###TODO##############################
## Edge case detection: if the listener matrix is set and the sender matrix is all nil, then the sender matrix is invalid. Timeout event?
## Edge case detection: if somehow an invalid matrix is identified, the program should not crash.
## Throw exception if no matrixFile could be found. matrixFile should be located in the same Folder as this python file.

import time
import pickle
import RPi.GPIO as GPIO

# We need the following free RPi GPIO pins
GPIOMODE = GPIO.BOARD
freeGPIOSenderPins = [11,12,13,15,16,18,22,29]
freeGPIOListenerPins = [31,32,33,35,36,37,38,40]
pinHigh = 1
pinLow = 0
# Mapped matrix file in the same directory as this python file
matrixFile = 'SensorDict.pkl'
# Trigger reset time (in seconds)
triggerResetTime = 0.5

def splash():
    #display splash screen
    print("""
    piDartboardRuntime: A Python runtime as translator between electronic dartboard matrix and Raspberry Pi.
    """)

def loadMappedMatrix(matrixFile):
    #Loads the matrix mapping and returns a dictionary of the matrix map
    with open(matrixFile, 'rb') as file:
        matrixMap = pickle.load(file)
    return matrixMap

def RPiGPIOSetup():
    ### Set Raspberry Pi GPIO pins to capture dartboard segment matrix data for each tile pressed ###
    GPIO.setmode(GPIOMODE)

    # Set up RPi GPIO pins:
    ####Sender
    for pin in freeGPIOSenderPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass
        GPIO.setup(pin, GPIO.OUT)

    ####Listener
    for pin in freeGPIOListenerPins:
        try:
            GPIO.cleanup(pin)
        except:
            pass
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # Capture reference matrix for later comparison
    #Example output is: [0, 0, 0, 0, 0, 0, 0, 0]
    referenceMatrix = []
    for pin in freeGPIOListenerPins:
        referenceMatrix.append(GPIO.input(pin))
    print(f'[DBG] Reference Matrix: {referenceMatrix}')
    return referenceMatrix

def getListenerMatrix(referenceMatrix):
    #Grab listener matrix by checking for changes on the GPIO pin signals
    #Example output is: [0, 0, 0, 1, 0, 0, 0, 0]
    #Example return is the index of above output: 3
    #Reminder: Index starts at 0!

    # Send signal through all sender pins
    for pin in freeGPIOSenderPins:
        GPIO.output(pin, GPIO.HIGH)

    listenerMatrix = []
    # Check if a tile was pressed by comparing the listener matrix with the reference matrix
    while True:
        listenerMatrix = [GPIO.input(pin) for pin in freeGPIOListenerPins]
        if not listenerMatrix == referenceMatrix:
            break
        else:
            listenerMatrix = []
    # Since this should only be one signal return it's index, we need it later to get the sender matrix
    listenerMatrixIndex = listenerMatrix.index(pinHigh)
    return listenerMatrix,listenerMatrixIndex

def getSenderMatrix(referenceMatrix, listenerMatrixIndex):
    #Grab sender matrix by checking for changes on the GPIO pin signals of the defined listener pin
    #Example output is: [1, 1, 1, 1, 0, 0, 0, 0]
    #Example return is the index of above output: 2
    #Reminder: index starts at 0!

    senderMatrix = []
    # Check if a tile was pressed by enumerating the pins that are sending signals to the listener pin we previously identified
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
        break
    return senderMatrix

def interpretSenderListener(senderMatrix, listenerMatrix, matrixMap):
    #Interpret sender and listener matrix to determine which tile was pressed
    #Example input: [1, 1, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]
    #Returns: interpretedResult=d14, alternativeInterpretedResult=Double 14

    #for entries in matrixMap:
    #    if entries.split(',')[1] == str(senderMatrix) and entries.split(',')[2] == str(listenerMatrix):
    #        interpretedResult = entries.split(',')[0]
    #        alternativeInterpretedResult = interpretedResult.replace('d', 'Double ').repalce('t', 'Triple ').replace('i', '').replace('o', '').replace('be', 'Bulls-Eye').replace('dbe', 'Double Bulls-Eye')
    #        break
    #ShortToLong = {"d":"double","t":"triple","i":"inner","o":"outer",'be': 'Bulls-Eye','dbe': 'Double Bulls-Eye','b': 'Bulls-Eye','x': 'Double Bulls-Eye'}
    #StrToInt = {{"d":lambda x: x*2,"t":lambda x: x*3,"i":lambda x: x,"o":lambda x: x,'be': lambda x: x*0+25,'dbe': lambda x: x*0+50,'b': lambda x: x*0+25,'x': lambda x: x*0+50}}

    throw = (str(senderMatrix),str(listenerMatrix))    
    shortResult = matrixMap.get(throw)

    #OneLetter_Str=interpretedResult.replace("dbe","x").replace("be","b")
    #scoreInteger = StrToInt.get(OneLetter_Str[0])(int(OneLetter_Str[1:]))

    #prefix=ShortToLong.get(interpretedResult[0])
    longResult = interpretedResult.replace('i', '').replace('o', '').replace('d', 'Double ').replace('t', 'Triple ').replace('be', 'Bulls-Eye').replace('dbe', 'Double Bulls-Eye')
    return shortResult, longResult, #scoreInteger
    
def cleanUp():
    print(f'Cleaning up GPIO mappings')
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

### If called as a module, return the interpreted result ###

def piBoardRuntime():
    global interpretedResult, alternativeInterpretedResult
    matrixMap = loadMappedMatrix(matrixFile)
    referenceMatrix = RPiGPIOSetup()
    while True:
        listenerMatrix,listenerMatrixIndex = getListenerMatrix(referenceMatrix)
        senderMatrix = getSenderMatrix(referenceMatrix, listenerMatrixIndex)
        interpretedResult, alternativeInterpretedResult = interpretSenderListener(senderMatrix, listenerMatrix, matrixMap)
        time.sleep(triggerResetTime)

### If called standalone, run the program in debug mode ###

if __name__ == "__main__":
    splash()
    print(f'Loading matrix mappings from file {matrixFile}')
    matrixMap = loadMappedMatrix(matrixFile)
    print('Starting listener...')
    referenceMatrix = RPiGPIOSetup()
    while True:
        print('Waiting for shot...')
        listenerMatrix,listenerMatrixIndex = getListenerMatrix(referenceMatrix)
        senderMatrix = getSenderMatrix(referenceMatrix, listenerMatrixIndex)
        interpretedResult, alternativeInterpretedResult = interpretSenderListener(senderMatrix, listenerMatrix, matrixMap)
        print(f'[DBG] {listenerMatrix}, {senderMatrix} --> {interpretedResult}/{alternativeInterpretedResult}')
        #prevent overly triggering
        time.sleep(triggerResetTime)
    cleanUp()

