import pandas as pd
import pickle

path = input("CSV Filepath: ")
df = pd.read_csv(path,sep=";")

dict={} 

for entry in df.iloc:
    TileName = entry[0]
    Sender = entry[1]   #json.loads(entry[1])
    Listener = entry[2] #json.loads(entry[2])

    new = { (Sender,Listener) : TileName}

    dict.update(new)
    print(new)

with open(input("Pickle relative Filepath: "),"wb") as file:
    pickle.dump(dict,file)