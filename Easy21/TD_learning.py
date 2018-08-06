import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from environment import Easy21
from monte_carlo_control import monte_carlo

def epsilon_greedy(N0, N, Q, x, y):
    # epsilon-greedy exploration
    e = N0 / (N0 + np.sum(N[x - 1, y - 1, :]))
    if np.random.uniform(0, 1) > e:
        action = np.argmax(Q[x - 1, y - 1, :])
    else:
        action = np.random.randint(0, 2)
    return action

def sarsa_lambda(max_episode, gamma, lbd, N0, optimal_Q=None):
    # sarsa(lambda)
    Q = np.zeros([21, 10, 2])
    N = np.zeros([21, 10, 2])
    mse = []
    for i in range(max_episode):
        # initial eligibility traces
        E = np.zeros([21, 10, 2])
        # initial a new episode
        episode = Easy21()
        x, y = episode.State()
        action = epsilon_greedy(N0, N, Q, x, y)
        # sample until terminal
        while not episode.is_game_end():
            N[x - 1, y - 1, action] += 1
            E[x - 1, y - 1, action] += 1
            # run one step
            ([xp, yp], reward) = episode.step(action)
            if episode.is_game_end():
                # if the episode is in terminal state, Q[s', a'] is 0
                delta = reward - Q[x - 1, y - 1, action]
                actionp = 0
            else:
                actionp = epsilon_greedy(N0, N, Q, xp, yp)
                delta = reward + gamma * Q[xp - 1, yp - 1, actionp] - Q[x - 1, y - 1, action]
            alpha = 1.0 / N[x - 1, y - 1, action]
            Q += (alpha * delta * E)
            E *= (gamma * lbd)
            x, y, action = xp, yp, actionp
        if (i% 1000 == 0) and (optimal_Q is not None):
            mse.append(np.sum((Q - optimal_Q)**2))
    return (Q, mse)

def main():
    N0 = 200
    gamma = 1
    lbd = 0
    max_episode = 50001
    mse_list = []
    mc_Q = monte_carlo(10**6, gamma, N0)
    for lbd in np.arange(0, 1.1, 0.1):
        sarsa_Q, mse = sarsa_lambda(max_episode, gamma, lbd, N0, mc_Q)
        mse_list.append(mse[-1])
        Vm = np.amax(sarsa_Q, axis=2)
        if lbd == 0.0 or lbd == 1.0:
            # plot MSE against episode number
            plt.figure()
            plt.plot(np.arange(0, max_episode, 1000), mse)
            plt.xlabel("episode")
            plt.ylabel("MSE")
            plt.title("lambda = {}".format(lbd))
            plt.draw()
            # plot value function
            x = np.arange(1, 22)
            y = np.arange(1, 11)
            xs, ys = np.meshgrid(x, y)
            fig = plt.figure()
            ax = Axes3D(fig)
            ax.plot_wireframe(xs, ys, Vm.T, rstride=1, cstride=1)
            plt.title("Value function when lambda = {}".format(lbd))
            plt.draw()
            
    # plot mse against lambda      
    plt.figure()
    plt.plot(np.arange(0, 1.1, 0.1), mse_list)
    plt.xlabel(r"$\lambda$")
    plt.ylabel("MSE")
    plt.draw()

    plt.show()

if __name__ == "__main__":
    main()
