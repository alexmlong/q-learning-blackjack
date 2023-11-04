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

    def __init__(self,epsilon):
        self.epsilon = epsilon

    def get_action(self, obs: tuple[int, int]) -> int:
        """
        Either chooses an action at random, with probability 1 - epsilon,
        or chooses the action that has the highest known value so far.

        This is used at each point in the game where the agent gets to
        make a decision.
        """
        if random.random() > self.epsilon:
            return random.choice(ACTIONS)
        else:
            values = self.qtable.get(obs, [0, 0])
            max_value = max(values)
            best_choice = values.index(max_value)
            return best_choice

    def calc_discounted_rewards(self, reward):
        """
        Calculates rewards for every action in the agent's history and
        by taking the base reward provided and discounting it (i.e.
        setting it closer to 0) progressively for each step in history,
        such that older steps are given a more heavily discounted reward.

        This is used when a game completes and a reward is given
        depending on whether or not the agent won, which is then used to
        update the agent's mapping of value for actions in various states.
        """
        rewards = []
        for index, step in enumerate(reversed(self.history)):
            discount_step = 1 / len(self.history)
            rewards.append((1 - (index * discount_step)) * reward)

        return rewards

    def update(
        self,
        reward
    ):
        """
        This updates the agent's mapping of values for specific actions
        in specific states based on the provided reward. This is used when
        a game completes.
        """
        discounted_rewards = self.calc_discounted_rewards(reward)
        for index, step in enumerate(reversed(self.history)):
            if step['state'] not in self.qtable:
                self.qtable[step['state']] = [0] * len(ACTIONS)

            self.qtable[step['state']][step['action']] += discounted_rewards[index]
        self.history = []

    def decay_epsilon(self):
        pass

def take_turn(player, state, agent):
    """ Executes a single turn of Black Jack. """
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
    """ Creates a plot showing the agent's preferred action. """
    matrix = np.zeros((21, 21))
    for state, values in agent.qtable.items():
        matrix[state[0]][state[1]] = 1 if values[0] > values[1] else 0

    plt.imshow(matrix, cmap='Blues', label="Test")
    plt.xlabel("agent score")
    plt.ylabel("dealer score")
    note_text = "blue = stay, white = hit"
    x_coord = 8
    y_coord = 0

    plt.text(x_coord, y_coord, note_text, fontsize=12, color='black',
            bbox=dict(alpha=0.7))

def run_experiment():
    """ Runs the entire experiment, training and evaluating the agent. """
    agent = BlackjackAgent(epsilon=0.2)
    game_count = 200000
    step_size = int(game_count / 20)
    winner_indices = []
    for game_index in range(game_count):
        players = [
            {'type': 'dealer', 'score': 0, 'did_stay': False},
            {'type': 'agent', 'score': 0, 'did_stay': False},
        ]
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

    make_confusion_matrix()
    plt.show()