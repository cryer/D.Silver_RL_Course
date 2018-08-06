import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from environment import Easy21

def epsilon_greedy(N0, N, Q, x, y):
    # epsilon-greedy exploration
    e = N0 / (N0 + np.sum(N[x - 1, y - 1, :]))
    if np.random.uniform(0, 1) > e:
        action = np.argmax(Q[x - 1, y - 1, :])
    else:
        action = np.random.randint(0, 2)
    return action

def monte_carlo(max_episode, gamma, N0):
    # monte carlo
    Q = np.zeros([21, 10, 2])
    N = np.zeros([21, 10, 2])
    for i in range(max_episode):
        # initial a new episode
        episode = Easy21()
        # the initial state of the episode
        x, y = episode.State()
        # sample until terminal
        history = []
        while not episode.is_game_end():
            # decide action
            action = epsilon_greedy(N0, N, Q, x, y)
            N[x - 1, y - 1, action] += 1
            # run one step
            state, reward = episode.step(action)
            history.append(([x, y], action, reward))
            [x, y] = state
        # calculate return Gt for each state in this episode
        Gt = 0
        for j, (state, action, reward) in enumerate(reversed(history)):
            [x, y] = state
            alpha = 1.0 / N[x - 1, y - 1, action]
            Gt = gamma * Gt + reward
            Q[x - 1, y - 1, action] += alpha * (Gt - Q[x - 1, y - 1, action])
    return Q


def main():
    N0 = 200
    gamma = 1
    max_episode = 1000000
    mc_Q = monte_carlo(max_episode, gamma, N0)
    # optimal value function
    Vm = np.amax(mc_Q, axis=2)
    # plot value function
    x = np.arange(1, 22)
    y = np.arange(1, 11)
    xs, ys = np.meshgrid(x, y)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(xs, ys, Vm.T, rstride=1, cstride=1)
    plt.show()

if __name__ == "__main__":
    main()
