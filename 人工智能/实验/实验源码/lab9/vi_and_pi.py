### MDP Value Iteration and Policy Iteration
import argparse
import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

parser = argparse.ArgumentParser(description='A program to run assignment 1 implementations.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--env", 
					help="The name of the environment to run your algorithm on.", 
					choices=["Deterministic-4x4-FrozenLake-v0","Stochastic-4x4-FrozenLake-v0"],
					default="Deterministic-4x4-FrozenLake-v0")

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float 用 "行动 "从 "状态 "过渡到 "下一状态 "的概率。
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int 表示我们过渡到的状态（范围是[0, nS - 1]）。
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int 
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action" 0或1，表示用 "行动 "从 "状态 "过渡到 "下一个状态 "的奖励。
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
			  当 "下一个状态 "是一个终端状态（洞或目标）时为真，否则为假。
	nS: int 状态的数量
		number of states in the environment
	nA: int 行动的数量
		number of actions in the environment
	gamma: float 折扣因子γ
		Discount factor. Number in range [0, 1)
"""

"""
策略评估
"""
def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.评估的策略 将状态映射到行动。初始都为0
	tol: float
		Terminate policy evaluation when终止政策评估，当
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS] 值函数
		The value function of the given policy, where value_function[s] is 给定策略的值函数，其中value_function[s]为
		the value of state s状态s的值
	"""

	value_function = np.zeros(nS)

	############################
	while(True):
		delta = 0.0
		for i in range(nS):
			j = policy[i]
			#if P[i][j][0][3]:
			#	continue
			v = value_function[i]
			value_function[i] = P[i][j][0][2] + gamma * value_function[P[i][j][0][1]]
			delta += abs(v - value_function[i])
		if delta < tol:
			break
	############################
	return value_function

"""
策略改进
"""
def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy 由策略计算出的值函数
	policy: np.array
		The previous policy. 之前的策略

	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

	new_policy = np.zeros(nS, dtype='int')

	############################
	#先计算状态行动值函数，然后找最优
	for i in range(nS):
		#if P[i][policy[i]][0][3]:
		#	continue
		a1 = policy[i]
		v1 = P[i][a1][0][2] + gamma * value_from_policy[P[i][a1][0][1]]
		for j in range(nA):
			if v1 < (P[i][j][0][2] + gamma * value_from_policy[P[i][j][0][1]]):
				a1 = j
				v1 = P[i][j][0][2] + gamma * value_from_policy[P[i][j][0][1]]
		new_policy[i] = a1
	############################
	return new_policy

"""
策略迭代
"""
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
	while(True):
		policy_stable = True
		value_from_policy = policy_evaluation(P, nS, nA, policy, gamma, tol)
		new_policy = policy_improvement(P, nS, nA, value_from_policy, policy, gamma)
		for i in range(nS):
			if new_policy[i] != policy[i]:
				policy_stable = False
		policy = new_policy
		if(policy_stable):
			break
	############################
	return value_function, policy

"""
值迭代
"""
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
	while (True):
		delta = 0.0
		for i in range(nS):
			a1 = policy[i]
			v1 = P[i][a1][0][2] + gamma * P[i][a1][0][1]
			for j in range(nA):
				if P[i][j][0][3] and P[i][j][0][1]!= 15:
					continue
				if v1 < P[i][j][0][2] + gamma * P[i][j][0][1]:
					a1 = j
					v1 = P[i][j][0][2] + gamma * P[i][j][0][1]
			delta += abs(v1 - value_function[i])
			policy[i] = a1
			value_function[i] = v1
		if delta < tol:
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
# 编辑以下内容，在不同的环境中运行策略和值迭代，并
# 可视化所产生的策略的作用!
# 你可以改变下面函数中的参数
if __name__ == "__main__":
	# read in script argument
	args = parser.parse_args()
	
	# Make gym environment
	env = gym.make(args.env)

	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_pi, 100)

	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)

	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_vi, 100)


