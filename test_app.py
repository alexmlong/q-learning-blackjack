from app import BlackjackAgent


def test_get_action():
    agent = BlackjackAgent(epsilon=1)
    agent.qtable = {
        (0, 2, True): [1, 0]
    }
    action = agent.get_action((0, 2, True))
    assert action == 0, action

def test_calc_discounted_rewards():
    agent = BlackjackAgent(epsilon=1)

    agent.history = [
        {'state': (10, 0, True), 'action': 0},
        {'state': (16, 5, True), 'action': 0},
        {'state': (16, 15, True), 'action': 0},
        {'state': (16, 25, True), 'action': 0},
    ]

    discounted_rewards = agent.calc_discounted_rewards(-10)
    assert discounted_rewards == [-10, -7.5, -5, -2.5], discounted_rewards

def test_update():
    agent = BlackjackAgent(epsilon=1)
    agent.history = [
        {'state': (10, 0, True), 'action': 0},
        {'state': (16, 5, True), 'action': 0},
        {'state': (16, 15, True), 'action': 0},
        {'state': (16, 25, True), 'action': 0},
    ]
    agent.update(-10)
    assert agent.qtable == {
        (10, 0, True): [-2.5, 0],
        (16, 5, True): [-5, 0],
        (16, 15, True): [-7.5, 0],
        (16, 25, True): [-10, 0],
    }, agent.qtable