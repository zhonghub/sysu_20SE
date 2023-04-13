### MDP Value Iteration and Policy Iteration
import argparse
import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

parser = argparse.ArgumentParser(description='A program to run assignment 1 implementations.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--env",
                    help="The name of the environment to run your algorithm on.",
                    choices=["Deterministic-4x4-FrozenLake-v0", "Stochastic-4x4-FrozenLake-v0"],
                    default="Deterministic-4x4-FrozenLake-v0")

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a (P,S',r,goal)
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float	概率
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int	下一个状态
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int		奖励值
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool	终止
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int		# 状态数
		number of states in the environment
	nA: int		# 策略数
		number of actions in the environment
	gamma: float	# y , V(s) = r + y *V(s')*p(s')
		Discount factor. Number in range [0, 1)
"""


def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
    """Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
	"""
    #  P[state][action] =  (P,S',r,goal)
    #
    value_function = np.zeros(nS)
    ############################
    # YOUR IMPLEMENTATION HERE #
    # value_function[nS-1] = 0
    while True:
        delta = 0.0
        prev_v = np.copy(value_function)
        for s in range(nS):  # action = policy[t]
            v = value_function[s]
            V_s = 0
            a = policy[s]
            for j in P[s][a]:
                V_s += j[0] * (j[2] + gamma * prev_v[j[1]])  # V(s) = (r + y *V(s')) *p(s')
            value_function[s] = V_s
            delta += abs(V_s - v)
        if delta < tol:
            # print("Value function converged.")
            break
    ############################
    # return value_function
    return value_function


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
    """Given the value function from policy improve the policy.
	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

    new_policy = np.zeros(nS, dtype='int')

    ############################
    # YOUR IMPLEMENTATION HERE #
    for s in range(nS):
        q_sa = np.zeros(nA)
        # 评估当前状态下，每个动作的收益
        for a in range(nA):
            # 计算动作值函数q
            q_sa[a] = sum([p * (r + gamma * value_from_policy[s_]) for p, s_, r, _ in P[s][a]])
        # 更新后的策略是相对于q的贪婪策略，所以使用max操作
        new_policy[s] = np.random.choice(np.argwhere(q_sa == np.max(q_sa)).flatten())

    ############################
    return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3):
    """Runs policy iteration.

	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)

    ############################

    # YOUR IMPLEMENTATION HERE #
    policy_stable = False
    while not policy_stable:
        policy_stable = True
        value_from_policy = policy_evaluation(P, nS, nA, policy, gamma, tol)
        new_policy = policy_improvement(P, nS, nA, value_from_policy, policy, gamma)
        for i in range(nS):
            if new_policy[i] != policy[i]:
                policy_stable = False
                break
        policy = new_policy

    ############################
    return value_function, policy


def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3):
    """
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)
    ############################

    # YOUR IMPLEMENTATION HERE #
    while True:
        delta = 0.0
        for s in range(nS):
            a0 = policy[s]
            v1 = P[s][a0][0][2] + gamma * P[s][a0][0][1]
            t = -1
            for a in range(nA):
                t += 1
                p, s_, r, g = P[s][a][0]
                if g and s_ != 15:
                    continue
                if v1 < r + gamma * s_:
                    a0 = t
                    v1 = r + gamma * s_
            delta += abs(v1 - value_function[s])
            policy[s] = a0
            value_function[s] = v1
        if delta < tol:  # delta < tol
            break

    ############################

    return value_function, policy


def render_single(env, policy, max_steps=100):
    """
	This function does not need to be modified
	Renders policy once on environment. Watch your agent play!

	Parameters
	----------
	env: gym.core.Environment
		Environment to play on. Must have nS, nA, and P as attributes.
	Policy: np.array of shape [env.nS]
		The action to take at a given state
	"""
    episode_reward = 0
    ob = env.reset()
    done = False
    for t in range(max_steps):
        env.render()
        time.sleep(0.25)
        a = policy[ob]
        ob, rew, done, _ = env.step(a)
        episode_reward += rew
        if done:
            break
    env.render()
    if not done:
        print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
    else:
        print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":
    # read in script argument
    args = parser.parse_args()

    # Make gym environment
    env = gym.make(args.env)

    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)

    V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    render_single(env, p_pi, 100)

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)

    V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
    render_single(env, p_vi, 100)
