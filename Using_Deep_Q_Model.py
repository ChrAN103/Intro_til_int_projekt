import Setup_til_Spil_v2 as env
from Deep_Q_learning_model import Agent
import matplotlib.pyplot as plt
import numpy as np

num_games = 10000

lwinsp = []
gscore = []
rounds = []
steplist = []

for j in range(53):

    agent = Agent(gamma=0.99, epsilon=1.0, lr=0.001, input_dims=[8], batch_size=5, n_actions=4, max_mem_size=100000, eps_end=0.01, eps_dec=0.00003,eps_remover=num_games*0.9)

    rounds.append(j)
    print("__________________________________________________________________________")
    print("Round nr. ",j+1)
    print("__________________________________________________________________________")

    scores = []

    eps_history = []
    x=[]
    y=[]
    count=0

    wins = 0
    loses = 0
    
    step = 0
    gamestep = []
    hundsteps = []

    all_steps = []
    o = []

    every_score = []
    allwins = 0
    percent_wins = []
    scoreone = []



    for i in range(num_games):
        score = 0
        reward = 0
        steps = 0
        done = False
        observations = env.setup()
        playercor, snow1, tsnow, fmap = observations
        #Generating state:
        #observation=env.states(playercor, snow1, tsnow)
        observation=env.states_deep(playercor, snow1, tsnow)
        
        while not done:
            # Chosing action given state
            action = agent.choose_action(observation)
            old_observation = observation
            key = ['w', 'a', 's', 'd'][action] 

            # Player move
            env.move(key, playercor, fmap)
            

            # Checking if win or lose:
            if env.win_lose(playercor, snow1)=="WIN":
                reward=100
                done=True
                allwins += 1
            if env.win_lose(playercor, snow1)=="LOSE" and reward==0:
                reward=-100
                done=True
            
            # Snowflake moves:
            env.snow_move(playercor, snow1, tsnow, fmap)

            # Checking if win or lose:
            if env.win_lose(playercor, snow1)=="LOSE" and reward==0:
                reward=-100
                done=True
            if reward==0:
                reward=-1
            
            # New state
            observation=env.states_deep(playercor, snow1, tsnow)
            
            # Giving reward
            score += reward

            agent.store_transition(old_observation, action, reward, observation, done)
            
            # Removing epsilon
            if i >= agent.eps_remover:
                if reward == 100:
                    wins += 1
                if reward == -100:
                    loses += 1

            agent.learn(i)
            reward = 0
            count += 1
            steps += 1
            step += 1

        gamestep.append(step)
        step = 0
        eps_history.append(agent.epsilon)
        
        x.append(i)
        y.append(score)
        o.append(score)
        every_score.append(score)

        
        if i%100==0:
            print('Game', i, 'Score:', score,",  epsilon = ",agent.epsilon,",  min score = ",np.min(o),",  max score = ",np.max(o),",  median score = ",np.median(o),",  mean score = ", np.mean(o))
            percent_wins.append(np.mean(allwins))
            scoreone.append(np.mean(every_score))
            hundsteps.append(np.mean(gamestep))
            gamestep = []
            allwins = 0
            every_score = []
            o = []
        
        
        # Counting steps:
        if len(y) >= agent.eps_remover:
            scores.append(y[-1])
            all_steps.append(steps)

    # Printing collected data:
    steplist.append(np.mean(all_steps))      
    
    lwinsp.append(wins/(loses+wins))
    print("list of winning percents = ", lwinsp)
    print("wins = ",wins, ", loses = ", loses)
    gscore.append(np.mean(scores))
    print("average scores for last 1000 rounds = ", gscore)
    print("count = ",count)
    print("Epsilon = ",agent.epsilon)

print("mean score for score list = ",np.mean(gscore))
print("mean of winning percent = ",np.mean(lwinsp))
print("Mean steps of last 1000 games of all episodes = ",np.mean(steplist))

print(percent_wins)
print(scoreone)
print("step list: ",hundsteps)

# plotting the points  
plt.plot(rounds, lwinsp) 
# naming the x axis 
plt.xlabel('Episode') 
# naming the y axis 
plt.ylabel('Win rate') 
# giving a title to my graph 
plt.title('Win rate for final 1000 games in every episode') 
# function to show the plot 
plt.show() 

# plotting the points  
plt.plot(rounds, gscore) 
# naming the x axis 
plt.xlabel('Episode') 
# naming the y axis 
plt.ylabel('Average score') 
# giving a title to my graph 
plt.title('Average score for final 1000 games in every episode') 
# function to show the plot 
plt.show() 

# plotting the points  
plt.plot(rounds, steplist) 
# naming the x axis 
plt.xlabel('Episode') 
# naming the y axis 
plt.ylabel('Average steps') 
# giving a title to my graph 
plt.title('Average steps for final 1000 games in every episode') 
# function to show the plot 
plt.show() 
