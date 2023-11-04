# Playing “Blackjack” Using Q-Learning

This is a simple example of the reinforcement learning technique known as q-learning, being applied to “blackjack”. I implemented this without following a demo and apparently don’t actually know the rules of blackjack so what I’ve implemented is slightly different. I’ve put the rules I used below.

To run, first install deps with `pip install -r requirements.txt`, then run with `python app.py`.

### Rules

There are two players, the dealer and the agent.

Each game the players take turns deciding whether to “hit”, i.e. get another card, or “stay”, i.e. don’t get another card and give up the ability to get any more cards for this game. In this altered version, there are only 10 cards you can receive, an Ace through a 10. Every card is worth the number of points corresponding to its number, i.e. a 5 is worth 5 points. Ace is worth 1 point and cannot be used for 11 points as in typical blackjack.

The objective is to get as close to 21 points as possible without going over. If either player gets over 21 points they lose immediately. If both players “stay” then the player with the most points wins, with a draw going to the dealer.

The dealer’s simple logic is to always hit unless they have 15 points or more.

### Q-Learning Technique

My implementation of q-learning here is pretty ridiculously simple, but still gets some decent results! The way it works is that the agent contains a dictionary which stores the predicted value for every possible action for every possible state. Based on the results of each game it plays, it updates the predicted values of each decision action it took in each state it was in based on whether or not it won the game. This is incredibly “brute-forcey” as the agent can only reach reasonable levels of performance by experiencing every possible state and trying every possible action multiple times, but this is essentially how q-learning works.

### Results

As you can see in the matrix visualization below, the agent did learn a non-random strategy. The visualization shows the dealer’s score and the y-axis and the agent’s score on the x-axis. Each frame of the animation corresponds to Each cell corresponds to what the agent would do in that state, with blue meaning “stay” and white meaning “hit”. The animation shows the agent’s best predicted behavior changing as it learns through more games.

A “staircase” pattern can be seen forming in the bottom right of the visualization over time and the bottom left of the matrix becomes more white. This shows that in general the agent is learning to never stay with a lower score, and above a certain threshold, only hit when its score is lower than the dealer’s.

![The agent is learning to “walk the line” of hitting only when it’s going to lose otherwise](https://github.com/alexmlong/q-learning-blackjack/assets/794661/f6fa4ac1-c91a-44a5-9062-12867a1840ea)
