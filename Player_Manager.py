## Player Manager
import numpy as np

class ScoreBoard:

    n_active = 0 #Index of active player
    PlayerNames = []
    ScoreBoard = {} #{"PlayerName": {"Throws": [[],[]], "Score": 0}}

    target = 301
    arrows = 3
    DoubleOut = False

    Current_Throw = []

    def __str__(self):
        return str(self.ScoreBoard)

    def refresh(self):
        self.ActivePlayer = self.PlayerNames[self.n_active % len(self.PlayerNames)]
        if self.ScoreBoard[self.getActivePlayer()].get("Score") != None:
            self.Current_Score = self.ScoreBoard[self.ActivePlayer]["Score"] - np.sum(self.Current_Throw)

        for Player,Values in self.ScoreBoard.items():           
            self.PointCalculation(Player) 
            self.ScoreCalculation(Player)
            self.AverageScoreCalculation(Player) 
            self.RoundCalculation(Player)
            self.CheckWin(Player)
            

    def PointCalculation(self,name):
        self.ScoreBoard[name]["Points"] = np.sum(self.ScoreBoard[name]["Throws"])
        return self.ScoreBoard[name]["Points"]

    def ScoreCalculation(self,name):
        self.ScoreBoard[name]["Score"] = self.target - self.ScoreBoard[name]["Points"]
        return self.ScoreBoard[name]["Score"]

    def AverageScoreCalculation(self,name):
        if len(self.ScoreBoard[name]["Throws"]) > 0:
            self.ScoreBoard[name]["Average Points"] = np.average(self.ScoreBoard[name]["Throws"]).round(2)
        else:
            self.ScoreBoard[name]["Average Points"] = 0
        return self.ScoreBoard[name]["Average Points"]

    def RoundCalculation(self,name):
        self.ScoreBoard[name]["Played rounds"] = len(self.ScoreBoard[name]["Throws"])
        return self.ScoreBoard[name]["Played rounds"]

    def CheckWin(self,name):
        Score = self.ScoreBoard[name]["Score"]

        if Score < 0:
            print("Fail")
            self.ScoreBoard[name]["Throws"].pop()
            return False
        elif Score == 0 and self.LastMultiplicator>=2:
            return True
        if Score == 0 and self.DoubleOut == False:
            return True        
        else:
            return False


    def CurrentThrow_Round(self,number):
        """

        Args:
            number (int): Number of Throw

        Returns:
            Throw Value: Value of number-th Throw
        """
        try: 
            return self.Current_Throw[number-1]
        except IndexError:
            return "-"


    def CurrentRoundPoints(self):
        return int(np.sum(self.Current_Throw))


    def CurrentPlayerScore(self):
        """
        Returns:
            Total Score of current Player
        """
        self.CurrentPlayerScore = self.ScoreBoard[self.getActivePlayer()]["Score"] + np.sum(self.Current_Throw)
        return self.CurrentPlayerScore

    def getCurrentScore(self):
        self.Current_Score = self.target - self.ScoreBoard[self.getActivePlayer()]["Points"] - np.sum(self.Current_Throw)
        return self.Current_Score
    

    def setTargetScore(self, target):
        self.target = target
        return self.target
        
    def setArrows(self, arrows):
        self.arrows = arrows

    def addPlayer(self, name):
        if name not in self.PlayerNames:
            self.PlayerNames.append(name)
        ## Add to dictionary
        if self.ScoreBoard.get(name) == None: 
            self.ScoreBoard[name] = {"Throws": [], "Score": 0, "Points": 0, "Average Points": 0, "Played rounds": 0}

    def removePlayer(self, name):
        self.PlayerNames.remove(name)
        self.ScoreBoard.pop(name)

    def getPlayerNames(self):
        return self.PlayerNames
    

    def TogglePlayer(self):
        self.PlayerNames.append(self.PlayerNames.pop(0)) #Swap first to last player
        self.setActivePlayer(self.PlayerNames[0])
        return self.ActivePlayer


    def setActivePlayer(self, name):
        self.ActivePlayer = name
        return self.ActivePlayer

    def getActivePlayer(self):
        self.ActivePlayer = self.PlayerNames[0]
        return self.ActivePlayer

    def Throw(self,Throw,Multiplicator=1):
        self.Current_Throw.append(Throw)
        return Throw,Multiplicator

    def addThrows(self, name, throws,multiplicator=1):
        self.LastMultiplicator = multiplicator
        self.ScoreBoard[name]["Throws"].append(throws)
        return self.ScoreBoard[name]["Throws"]

    def ResetCurrentThrow(self):
        self.Current_Throw = []
        return self.Current_Throw

    def addScore(self, name, score):
        if self.ScoreBoard.get(name):
            self.ScoreBoard[name]["Points"] += score
        else:
            self.ScoreBoard[name]["Points"] = score

    def getScore(self, name):
        if self.ScoreBoard[name].get("Score"):
            return self.ScoreBoard[name]["Score"]
        else:
            return 0

    def getScoreBoard(self):
        return self.ScoreBoard

    def getScoreBoardSorted(self):
        return sorted(self.ScoreBoard.items(), key=lambda x: x["Score"], reverse=True)

    

    # def NextPlayer(self):
    #     self.addThrows(self.getActivePlayer(), self.Current_Throw)
    #     self.ResetCurrentThrow()

    #     self.n_active += 1
    #     if self.n_active >= len(self.PlayerNames):
    #         self.n_active = 0
    #     self.ActivePlayer = self.PlayerNames[self.n_active % len(self.PlayerNames)]

    #     return self.ActivePlayer

    def SaveScoreBoard(self,):
        with open("Scoreboards.json", "a") as file:
            file.write(str(self.ScoreBoard) +"\n")


if __name__ == '__main__':

    SB = ScoreBoard()
    ## Add Players
    SB.addPlayer('Jannis')
    SB.addPlayer('Lino')
    SB.addPlayer('Jan')
    SB.addPlayer('Alex')

    SB.refresh()

    ## Set Target, ## Set Arrows
    SB.setTargetScore(301)
    SB.setArrows(3)

    ## Throw
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())


    SB.NextPlayer()

    #Throw
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())
    SB.Throw(np.random.randint(1,25))
    print(SB.getCurrentScore())

    SB.NextPlayer()

    
    SB.refresh()
    SB.SaveScoreBoard()
    print(SB)  