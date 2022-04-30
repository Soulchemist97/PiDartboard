import datetime as dt
# import RPIO
import RPi.GPIO as GPIO

#Raspberry Pi Pins
freeGPIOListenerPins = [31,32,33,35,36,37,38,40] #Input
freeGPIOSenderPins = [11,12,13,15,16,18,22,29] #Output 



def setupListenerPins():
    for pin in freeGPIOListenerPins:
        GPIO.cleanup(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class SensorFrame():
    
    name = "Frame"
    referenceMatrix = []

    def setName(self,Name):
        self.name = Name
        return self.name

    def CurrentTime(self):
        """Save Current time and date to str

        Returns:
            currentTime (str): Current time as str
        """
        self.currentTime = dt.datetime.now()
        self.currentTime_str = self.currentTime.strftime("%H:%M:%S %d.%m.%Y")
        return self.currentTime_str
    
    def CaptureReferenceMatrix(self):
        self.referenceMatrix = [GPIO.input(pin) for pin in freeGPIOListenerPins]
        return self.referenceMatrix

    def CaptureListenerMatrix(self):
        self.listenerMatrix = [GPIO.input(pin) for pin in freeGPIOListenerPins]
        return self.listenerMatrix

    def CaptureFrame(self):
        pass
    
    def Detect(self):
        setupListenerPins()
        self.CaptureReferenceMatrix()

        while True: #Start Detection
            self.CaptureListenerMatrix()
            
            # Trigger
            if self.referenceMatrix != self.listenerMatrix:
                
                print(self.listenerMatrix)
                self.ListenerPin = self.listenerMatrix.index(1)
                
                #Pins Resetten
                for pin in freeGPIOSenderPins:
                    GPIO.output(pin, GPIO.LOW) 
                    GPIO.output(pin, GPIO.HIGH)

                self.senderMatrix = [GPIO.input(pin) for pin in freeGPIOListenerPins]
                

                if self.referenceMatrix != senderMatrix:
                    self.SenderPin = self.senderMatrix.index(1)
                    print(f'Sender matrix for {self.name}: {senderMatrix}')
                    break
                else:
                    senderMatrix = []
                    continue
                
        return (self.ListenerPin,self.SenderPin)

    def main():
        pass



if __name__ == '__main__':

    print("...",flush=True,end="\r")

    GPIO.setmode(GPIO.BOARD)

    Frame = SensorFrame()
    Frame.setName("t20")

    Frame.Detect()