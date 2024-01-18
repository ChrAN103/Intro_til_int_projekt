import random
import numpy as np

random.seed(1)

# Defines and generates all the necessary variabel:
def setup():
    # Generate map:
    fmap = [[" "for num in range(10)] for num in range(10)]

    # List of snowflake coordinate(s):
    snow1 =[]
    # Type of snowflake:
    tsnow = []
    # Generate snoflake(s) coordinate(s) and add to map
    for nsnow in range(2):
        dsnow = [0,random.randrange(0,len(fmap[0]),1)]
        fmap[0][dsnow[1]] = "*"
        tsnow.append(random.randrange(0,3,1))
        snow1.append(dsnow) 
    
    #Generate player coordinate
    playercor = [9,random.randrange(0,len(fmap[0]),1)]
    fmap[9][playercor[1]] = "P"
    return [playercor, snow1, tsnow, fmap]


# Printing start and level:
def starting(fmap):
    print("_________________________________________________")
    print("Welcome to SnowAngel")
    print("Get back to heaven without hitting the snowflake(s)")
    print("Angel: P         Snowflake: * ")
    print("_________________________________________________")
    print_map(fmap)
   

#Getting state from all the coordinates
def states(playercor, snow1,tsnow):
    x = ""
    for i in range(len(snow1)):
        x += str(snow1[i][0])+str(snow1[i][1])+str(tsnow[i])
    return str(playercor[0])+str(playercor[1])+x

def states_deep(playercor, snow1, tsnow):
    state=np.array((playercor[0], playercor[1]), dtype=np.float32)
    for i in snow1:
        for j in i:
            state=np.append(state, j)
    for i in tsnow:
        state=np.append(state, i)    
    return state

# WIN or LOSE:
def win_lose(playercor, snow1):
    # Støder ind i snefnug (AKA. taber):
    for i in snow1:
        if i == playercor:
           return "LOSE"
        
    # Reaches top (AKA: vinder):
    if playercor[0] == 0:
        return "WIN"
    
    return ""
    

#Action from input
def move(key, playercor, fmap):
    # Left:
    if key == "a" and playercor[1]>0:
        # Update board:
        fmap[playercor[0]][playercor[1]] = " "
        # Update player-coordinate:
        playercor[1] -= 1
    # Right:
    if key == "d" and playercor[1]<len(fmap[0])-1:
        fmap[playercor[0]][playercor[1]] = " "
        playercor[1] += 1
    # Up
    if key == "w" and playercor[0]>0:
        fmap[playercor[0]][playercor[1]] = " "
        playercor[0] -= 1
    # Down
    if key == "s" and playercor[0]<len(fmap)-1:
        fmap[playercor[0]][playercor[1]] = " "
        playercor[0] += 1

    fmap[playercor[0]][playercor[1]] = "P"  
     


def snow_move(playercor, snow1, tsnow, fmap):
    for i in range(len(snow1)):
        # Sletter snefnug fra forrige position, men sørger for den ikke sletter player(p) hvis de går til pladsen:
        if fmap[snow1[i][0]][snow1[i][1]] != fmap[playercor[0]][playercor[1]]:
            fmap[snow1[i][0]][snow1[i][1]] = " "
        # Snefnug falder
        snow1[i][0] += 1
        
        # Rykker skråt hvis specifik type sne:
        if tsnow[i] == 1:
            snow1[i][1] += 1
        if tsnow[i] == 2:
            snow1[i][1] -= 1

        while snow1[i][1] < 0:
            snow1[i][1] = len(fmap[0]) + snow1[i][1]
        while snow1[i][1] >= len(fmap[0]):
            snow1[i][1] = len(fmap[0]) - snow1[i][1]

        # Rykker sne
        if 0 < snow1[i][0] < len(fmap):
            fmap[snow1[i][0]][snow1[i][1]] = "*"
        # Spawner snefnug i toppen hvis bunden er nået:
        else: 
            fmap[0][snow1[i][1]] = "*"
            snow1[i] = [0,snow1[i][1]]


def print_map(fmap):
    for i in fmap:
        print("|"+"|".join(i)+"|")
