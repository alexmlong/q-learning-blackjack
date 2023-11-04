import random

import matplotlib.pyplot as plt
import numpy as np


ACTIONS = [
    0, # hit
    1, # stay
]

class BlackjackAgent:
    epsilon = None
    qtable = {}
    history = []

    def __init__(
        self,
        epsilon,
    ):
        self.epsilon = epsilon

    def get_action(self, obs: tuple[int, int]) -> int:
        if random.random() > self.epsilon:
            return random.choice(ACTIONS)
        else:
            values = self.qtable.get(obs, [0, 0])
            max_value = max(values)
            best_choice = values.index(max_value)
            return best_choice

    def calc_discounted_rewards(self, reward):
        rewards = []
        for index, step in enumerate(reversed(self.history)):
            discount_step = 1 / len(self.history)
            rewards.append((1 - (index * discount_step)) * reward)

        return rewards

    def update(
        self,
        reward
    ):
        discounted_rewards = self.calc_discounted_rewards(reward)
        for index, step in enumerate(reversed(self.history)):
            if step['state'] not in self.qtable:
                self.qtable[step['state']] = [0] * len(ACTIONS)

            self.qtable[step['state']][step['action']] += discounted_rewards[index]
        self.history = []

    def decay_epsilon(self):
        pass

def take_turn(player, state, agent):
    # for given turn
    # player decides whether to hit or stay
    if player['type'] == 'dealer':
        if player['score'] < 15:
            player['score'] += random.randint(1, 10)
        else:
            player['did_stay'] = True
    else:
        action = agent.get_action(state)
        agent.history.append({'state': state, 'action': action})
        if action:
            player['score'] += random.randint(1, 10)
        else:
            player['did_stay'] = True

def make_confusion_matrix():
    matrix = np.zeros((21, 21))
    for state, values in agent.qtable.items():
        matrix[state[0]][state[1]] = 1 if values[0] > values[1] else 0

    plt.imshow(matrix, cmap='Blues', label="Test")
    plt.xlabel("agent score")
    plt.ylabel("dealer score")
    note_text = "blue = stay, white = hit"
    x_coord = 8  # X-coordinate of the textbox
    y_coord = 0  # Y-coordinate of the textbox

    plt.text(x_coord, y_coord, note_text, fontsize=12, color='black',
            bbox=dict(alpha=0.7))
    # plt.legend()

    # if hit, increase score accordingly
        # if busted, other player wins
    # if stay, update player status
    
    # if both players have stayed, calc winner
        # update agent

# repeat games over and over to train agent
def run_experiment():
    agent = BlackjackAgent(epsilon=0.2)
    game_count = 200000
    step_size = int(game_count / 20)
    winner_indices = []
    for game_index in range(game_count):
        players = [
            {'type': 'dealer', 'score': 0, 'did_stay': False},
            {'type': 'agent', 'score': 0, 'did_stay': False},
        ]
        game_is_over = False
        winner_index = None
        active_player_index = 0
        while winner_index is None:
            player = players[active_player_index]
            take_turn(player, (players[0]['score'], players[1]['score']), agent)
            if player['score'] == 21:
                winner_index = active_player_index
            elif player['score'] > 21:
                winner_index = 1 if active_player_index == 0 else 0
            elif players[0]['did_stay'] and players[1]['did_stay']:
                if players[0]['score'] >= players[1]['score']:
                    winner_index = 0
                else:
                    winner_index = 1
            
            if winner_index == 0:
                agent.update(-10)
            elif winner_index == 1:
                agent.update(10)

            active_player_index = 0 if active_player_index == 1 else 1
        winner_indices.append(winner_index)

        if game_index % step_size == 0:
            make_confusion_matrix()
            plt.savefig(f"confusion_matrix_game{game_index}.png")

    # given a list of winners
    # create a graph that shows on the x axis the number games played
    # and on the y axis the percent of the last 100 games that were won by the agent
    # convert list of winners into list of win percents by reducing down
    # step through list with step size equal to x axis tick interval
    # win_counts = []
    # window_size = 1
    # for game_index in range(step_size, game_count, step_size):
    # # get last 100 games
    #     prev_game_window = winner_indices[game_index - window_size: game_index]
    # # calc win perc
    #     agent_wins = len(list(filter(lambda index: index == 1, prev_game_window)))
    # # store it
    #     win_counts.append(agent_wins)

    # print(win_counts)
    # print(list(range(step_size, game_count, step_size)))
    # plt.plot(list(range(step_size, game_count, step_size)), win_counts)
    # plt.xlabel("number of games played")
    # plt.ylabel(f"number of agent wins in previous {window_size} games")
    # plt.show()
    # from pprint import pprint
    # pprint(agent.qtable)
    # # pprint({k: ('HIT' if v[0] > v[1] else 'STAY') + str(v) for k, v in agent.qtable.items()})
    # pprint({k: 0 if v[0] > v[1] else 1 for k, v in agent.qtable.items()})

    make_confusion_matrix()
    plt.show()