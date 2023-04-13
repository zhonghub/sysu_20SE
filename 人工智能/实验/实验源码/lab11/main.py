import argparse
import gym
from argument import dqn_arguments, pg_arguments

if __name__ == '__main__':
    from agent_dir.agent_dqn import AgentDQN
    env = gym.make('CartPole-v0')
    env.seed(0)
    agent = AgentDQN(env, 128)
    agent.run()
