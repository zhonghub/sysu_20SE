import gym
import torch
import torch.nn.functional as F
import numpy as np
from torch import nn, optim
import matplotlib.pyplot as plt
import time
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
env = gym.make("CartPole-v0")
lr = 1e-3
n_episodes = 500
alpha = 0.99  # 学习速率
capacity = 5000
eps = 1.0
eps_min = 0.05
hidden = 128
sample_size = 64  # 取样学习大小
eps_decay = 0.99
update_target = 100
lossf = nn.MSELoss()
allloss = []
allreward = []


def printfig(tlist, title):
    plt.plot(tlist)
    plt.title(title)
    # plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


class Net(nn.Module):  # 神经网络
    def __init__(self, input_size, output_size):
        # 初始化神经网络
        super(Net, self).__init__()
        self.func1 = nn.Linear(input_size, hidden)
        self.func2 = nn.Linear(hidden, output_size)

    def forward(self, x):
        x = torch.Tensor(x)
        hide = F.relu(self.func1(x))
        out = self.func2(hide)
        return out


def sample(memory, n):  # 取样
    index = np.random.choice(len(memory), n)
    sample_set = []
    for i in index:
        sample_set.append(memory[i])
    return zip(*sample_set)


def next_action(obs, eval_net):
    global eps
    if np.random.uniform() > eps:
        value = eval_net(obs)
        action = torch.max(value, dim=-1)[1].numpy()
    else:
        action = np.random.randint(0, env.action_space.n)
    return int(action)


def learn(learn_step, target_net, eval_net, memory, optimer):
    global eps
    if learn_step % update_target == 0:
        target_net.load_state_dict(eval_net.state_dict())  # 将评估网络复制到目标网络中
    learn_step += 1
    if eps > eps_min:
        eps *= eps_decay
    # 取样
    obs, actions, rewards, next_obs, dones = sample(memory,sample_size)
    actions = torch.LongTensor(actions)
    dones = torch.IntTensor(dones)
    rewards = torch.FloatTensor(rewards)
    # 更新两个神经网络
    q_eval = eval_net(obs).gather(-1, actions.unsqueeze(-1)).squeeze(-1)
    q_next = target_net(next_obs).detach()
    q_target = rewards + alpha * (1 - dones) * torch.max(q_next, dim=-1)[0]  # Q_target = r + alpha * q_next
    loss = lossf(q_eval, q_target)
    allloss.append(loss.item())
    optimer.zero_grad()
    loss.backward()
    optimer.step()
    return learn_step, target_net, eval_net, eps, optimer, memory

def push(memory, *transition):
    if len(memory) == capacity:
        memory.pop(0)
    memory.append(transition)

def DQN():
    # env.reset()
    start_time = time.process_time()
    memory=[]
    o_dim = env.observation_space.shape[0]
    a_dim = env.action_space.n
    eval_net = Net(o_dim, a_dim)  # 评估网络
    target_net = Net(o_dim, a_dim)  # 目标网络
    optimer = optim.Adam(eval_net.parameters(), lr=lr)  # 优化器
    learn_step = 0
    for i_episode in range(n_episodes):
        # env.render()
        obs = env.reset()
        episode_reward = 0
        done = False
        while not done:
            action = next_action(obs, eval_net)
            next_obs, reward, done, info = env.step(action)
            # 保存进行状态
            push(memory,obs, action, reward, next_obs, done)
            episode_reward += reward
            obs = next_obs
            if len(memory) >= capacity:
                learn_step, target_net, eval_net, eps, optimer, memory = learn(learn_step, target_net, eval_net, memory,
                                                                              optimer)
        print(f"Episode: {i_episode}, Reward: {episode_reward}")
        allreward.append(episode_reward)
    end_time = time.process_time()
    print(f'耗时:{end_time - start_time}s')
    printfig(allloss, "loss")
    printfig(allreward, "reward")


if __name__ == "__main__":
    DQN()
