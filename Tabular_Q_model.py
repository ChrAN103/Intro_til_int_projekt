import Setup_til_Spil_v2
from collections import defaultdict
import numpy as np
import random

def tabular_q_learning (rounds, epsiodes, eps_dec, eps_remover):
    #List for data storage for all models
    win_rate_overall=[]
    mean_score_overall=[]
    
    for j in range(rounds):
        print("_________________________________________________")
        print("Round nr. ", j+1, " out of ", rounds,".")
        print("_________________________________________________")

        # Setting variables for each round
        score_round=[]
        win_lose_round=[]
        steps_round=[]
        epsilon=1
        steps=0
        y_win, y_score, y_steps, x = [],[],[],[]
        

        # Defines necessary variabels for q-learning. This being 4 possibilities in each state
        actions = ['w', 'a', 's', 'd']
        q_table = defaultdict(lambda: [0, 0, 0, 0])

        for i in range(epsiodes):    

            done=False

            # Defines and generates all the necessary variables from game:
            startsetup = Setup_til_Spil_v2.setup()
            playercor = startsetup[0]
            snow1 = startsetup[1]
            tsnow = startsetup[2]
            fmap = startsetup[3]
            
            # Resetting win/lose check after each epsiode
            checking_lose=False
            checking_win=False

            # Resetting variables after each epsiode
            score = 0

            while not done:

                # Choice of action:
                # Every state is described as a string containing coordinates of player and
                # the coordinates of the snowflakes and the type of snow: 
                # "P(x)P(y)" + ("S(x)S(y) + type of snow") * amount of snowflakes
                q = q_table[Setup_til_Spil_v2.states(playercor, snow1,tsnow)]
                if random.random() > epsilon:
                    best_action_index = random.choice([i for i in range(len(q)) if q[i] == max(q)])
                else:
                    best_action_index=random.randrange(0,3,1)
                action = actions[best_action_index]
                    
                # Makes player move:
                Setup_til_Spil_v2.move(action, playercor, fmap)
                
                # Checking for Win/Loss after player move:
                if Setup_til_Spil_v2.win_lose(playercor, snow1) == "LOSE":
                    checking_lose=True
                elif Setup_til_Spil_v2.win_lose(playercor, snow1) == "WIN":
                    checking_win=True

                # Makes snowflakes move:
                Setup_til_Spil_v2.snow_move(playercor, snow1,tsnow , fmap)

                # Checking for loss after snowflake move
                if Setup_til_Spil_v2.win_lose(playercor, snow1) == "LOSE" and not checking_win:
                    checking_lose=True
                
                # Updating steps
                steps+=1

                # Defining rewards:
                if checking_win:
                    reward = 100
                elif checking_lose:
                    reward = -100
                else:
                    reward = -1
                
                # Updating score and win/lose list
                score += reward
                if reward==100:
                    win_lose_round.append(1)
                if reward==-100:
                    win_lose_round.append(0)
                
                # Updating Q-table:
                q[best_action_index] = reward+np.max(q_table[Setup_til_Spil_v2.states(playercor, snow1,tsnow)])*0.99

                # Updating epsilon
                if i < eps_remover:
                    epsilon = epsilon - eps_dec if epsilon > 0.01 else 0.01
                if i >= eps_remover:
                    epsilon = 0
                        

                # Restart if Win/Lose:
                if checking_lose or checking_win:
                    # Resetting game
                    startsetup = Setup_til_Spil_v2.setup()
                    playercor=startsetup[0]
                    snow1=startsetup[1]
                    tsnow=startsetup[2]
                    fmap=startsetup[3]

                    checking_lose=False
                    checking_win=False
                    done=True
                    
                    # Score update
                    score_round.append(score)
                    score = 0

                    # Steps_overall update
                    steps_round.append(steps)
                    steps=0
                    
                    # Following the progress
                    if i%1000==0:
                        print("Episode: ", i, ",   Win rate: ", np.mean(win_lose_round[-1000:]), ",    Mean score last 1000: ", np.mean(score_round[-1000:]))

                    # Collecting data for graphs
                    if i%100==0:
                        x.append(i)
                        y_win.append(np.mean(win_lose_round[-100:]))
                        y_score.append(np.mean(score_round[-100:]))
                        y_steps.append(np.mean(steps_round[-100:]))



        # Data for each independent round
        win_rate_overall.append(np.mean(win_lose_round[-1000:]))
        mean_score_overall.append(np.mean(score_round[-1000: ]))
        print("Win rate for each round: ", win_rate_overall)
        print("Mean score for each round: ", mean_score_overall)

        # Only print if data for graphs should be shown
        # print("x ", x)
        # print("y_win ",y_win)
        # print("y_score ",y_score)
        print("y_steps: ",y_steps)


# Choosing between the AI or manual player
print("For Q-learning type 'I'. For manual play press any other key.")
Play=input()

# Q-learning:
if Play=="I":
    # Setting variables for q learning here
    tabular_q_learning(rounds=1, epsiodes=10000, eps_dec=0.00003, eps_remover=9000)
  

# Manuelt spil:
else:
    # Defines and generates all the necessary variabel:
    startsetup = Setup_til_Spil_v2.setup()
    playercor=startsetup[0]
    snow1=startsetup[1]
    tsnow=startsetup[2]
    fmap=startsetup[3]
    Setup_til_Spil_v2.starting(fmap)
    while True:
        # Checking for Win/Lose:
        if Setup_til_Spil_v2.win_lose(playercor, snow1) != "":
            print(Setup_til_Spil_v2.win_lose(playercor, snow1))
            break
        
        key = input()
        # Quit:
        if key=='q':
            break
        
        # Player move:
        Setup_til_Spil_v2.move(key, playercor, fmap)
        # Checking for Win/Lose:
        if Setup_til_Spil_v2.win_lose(playercor, snow1) != "":
            print(Setup_til_Spil_v2.win_lose(playercor, snow1))
            break
        # Snow move:
        Setup_til_Spil_v2.snow_move(playercor, snow1, tsnow, fmap)
        # Printing updated map:
        Setup_til_Spil_v2.print_map(fmap)
