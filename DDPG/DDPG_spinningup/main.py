from DDPGModel import *
import gym
import matplotlib.pyplot as plt
from PPO.draw import Painter


if __name__ == '__main__':
    env = gym.make('Pendulum-v0')
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]
    act_bound = [-env.action_space.high[0], env.action_space.high[0]]

    ddpg = DDPG(obs_dim, act_dim, act_bound)

    MAX_EPISODE = 100
    MAX_STEP = 500
    update_every = 50
    batch_size = 100
    rewardList = []
    for episode in range(MAX_EPISODE):
        o = env.reset()
        ep_reward = 0
        for j in range(MAX_STEP):
            if episode > 5:
                a = ddpg.get_action(o, ddpg.act_noise)
            else:
                a = env.action_space.sample()
            o2, r, d, _ = env.step(a)
            ddpg.replay_buffer.store(o, a, r, o2, d)

            if episode >= 5 and j % update_every == 0:
                for _ in range(update_every):
                    batch = ddpg.replay_buffer.sample_batch(batch_size)
                    ddpg.update(data=batch)

            o = o2
            ep_reward += r

            if d:
                break
        print('Episode:', episode, 'Reward:%i' % int(ep_reward))
        rewardList.append(ep_reward)

    painter = Painter(load_csv=True,load_dir='../DDPG_spinningup_PER/compare.csv')
    painter.addData(rewardList,'DDPG')
    painter.saveData(save_dir='../DDPG_spinningup_PER/compare.csv')
    painter.drawFigure()





