import gym
from collections import deque
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

env = gym.make('CartPole-v0')
n_episodes = 2000
gamma = 0.99
print_every = 20
update_target = 100
capacity = 10000
eps = 100
env.seed(0)
print('observation space:', env.observation_space)
print('action space:', env.action_space)


class Net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.Tensor(x)
        x = F.relu(self.fc1(x))
        action_v = self.out(x)
        return action_v


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity

    def len(self):
        return len(self.buffer)

    def push(self, *transition):
        if len(self.buffer) == self.capacity:
            self.buffer.pop(0)
        self.buffer.append(transition)

    def sample(self, n):
        index = np.random.choice(len(self.buffer), n)
        batch = [self.buffer[i] for i in index]
        return zip(*batch)

    def clean(self):
        self.buffer.clear()


class DQN:
    def __init__(self, env, input_size, hidden_size, output_size):
        self.env = env
        # 两个网具有相同的结构
        self.eval_net = Net(input_size, hidden_size, output_size)
        # eval_net:实时更新的Q的network
        self.target_net = Net(input_size, hidden_size, output_size)
        # target_net:每TARGET_REPLACE_ITER轮更新一次的target network
        self.optim = optim.Adam(self.eval_net.parameters(), lr=1e-3)
        self.eps = eps
        self.buffer = ReplayBuffer(capacity)
        # relay buffer 计数器
        self.loss_fn = nn.MSELoss()
        self.learn_step = 0

    def choose_action(self, obs):
        if np.random.uniform() <= self.eps:
            # 贪婪策略
            action = np.random.randint(0, self.env.action_space.n)
        else:
            action_value = self.eval_net(obs)
            # actions_value 是每个action的Q值 (即Q(s,a))
            action = torch.max(action_value, dim=-1)[1].numpy()
            # 表示Q值最大的action的index
        return int(action)

    def store_transition(self, *transition):
        self.buffer.push(*transition)

    def learn(self):
        if self.eps > 0.05:
            self.eps *= 0.999

        if self.learn_step % update_target == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step += 1
        batch_size = 128
        obs, actions, rewards, next_obs, dones = self.buffer.sample(batch_size)
        # 从replay buffer中提取出这一个batch的记录
        actions = torch.LongTensor(actions)  # LongTensor to use gather latter
        dones = torch.IntTensor(dones)
        rewards = torch.FloatTensor(rewards)
        # 分别对应了这一个batch中的原始状态，该状态采取的动作，该状态的reward

        q_eval = self.eval_net(obs).gather(-1, actions.unsqueeze(-1)).squeeze(-1)
        # 这里gather的操作是根据squeeze是0还是1选择每一行的0还是1，也就是选择maxQ(s,a)
        q_next = self.target_net(next_obs).detach()
        # detach的作用就是不反向传播去更新
        q_target = rewards + gamma * (1 - dones) * torch.max(q_next, dim=-1)[0]
        # Q_target = r + gamma * q_next
        loss = self.loss_fn(q_eval, q_target)
        # pytorch深度学习
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()


def main():
    o_dim = env.observation_space.shape[0]
    a_dim = env.action_space.n
    agent = DQN(env, o_dim, 64, a_dim)
    scores_deque = deque(maxlen=100)
    scores = []

    for i_episode in range(n_episodes):
        obs = env.reset()
        # 重置当前环境状态
        episode_reward = 0
        # 每个episode中的reward
        done = False
        while not done:
            # env.render()
            # 渲染环境
            action = agent.choose_action(obs)
            # 根据当前的状态s，选择当前回合合适的action
            next_obs, reward, done, info = env.step(action)
            agent.store_transition(obs, action, reward, next_obs, done)
            # 状态，该状态使用的a，该状态用a之后的r，之后的状态这些信息存储起来，放入replay buffer中
            episode_reward += reward
            obs = next_obs
            if agent.buffer.len() >= capacity:
                agent.learn()
        scores_deque.append(episode_reward)
        # 维护可视化得分变化队列
        scores.append(episode_reward)
        if i_episode % print_every == 0:
            print('Episode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)))
        if np.mean(scores_deque) >= 195.0:
            print(
                'Environment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)))
            break
    ax = plt.figure().add_subplot(111)
    plt.plot(np.arange(1, len(scores) + 1), scores)
    plt.ylabel('Score')
    plt.xlabel('Episode')
    plt.show()


if __name__ == "__main__":
    main()
