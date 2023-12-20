import random
import numpy as np
from collections import defaultdict, deque
from player.mcts_player import MCTSPlayer
from player.policy_value_net import PolicyValueNet
from game_core.board import *


class SelfPlayGame:
    def __init__(self):
        pass

    def start_self_play(self, player, temp):
        board = Board()
        board.init_board(0)
        states, mcts_probs, current_players = [], [], []
        current_player_id = 0

        while True:
            (piece_id, coord), move_probs = player.get_action(board, current_player_id, temp=temp, return_probs=True)
            # store the data
            states.append(board.get_eval_state(current_player_id))
            mcts_probs.append(move_probs)
            current_players.append(current_player_id)
            # perform the move
            board.move_piece(piece_id, coord)
            # print(f"Player{current_player_id} moved {piece_id_to_chinese_name[piece_id-1]}({piece_id}) to {coord}")
            current_player_id = 1- current_player_id
            # check game finished
            game_finished, winner = board.game_finished()
            if game_finished:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if winner != -1:
                    print("Game end. Winner is player:", winner)
                else:
                    print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)
    
    def start_eval_play(self, players):
        board = Board()
        board.init_board(0)
        current_player_id = 0

        while True:
            player_in_turn = players[current_player_id]
            piece_id, coord = player_in_turn.get_action(board, current_player_id)  # player take action
            board.move_piece(piece_id, coord)  # update board state
            game_finished, winner = board.game_finished()  # check game finished
            if game_finished:
                players[0].reset_player()
                players[1].reset_player()
                break
            current_player_id = 1 - current_player_id  # switch the player
            

class TrainPipeline():
    def __init__(self):
        # params of the board and the game
        self.board_width = 9
        self.board_height = 10
        self.n_state_channels = 9
        self.n_actions = 192
        self.self_play_game = SelfPlayGame()
        # training params
        self.learn_rate = 2e-3
        self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.temp = 1.0  # the temperature param
        self.n_simulations = 200  # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 512  # mini-batch size for training
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.play_batch_size = 1
        self.epochs = 5  # num of train_steps for each update
        self.kl_targ = 0.02
        self.check_freq = 30
        self.game_batch_num = 100
        self.best_win_ratio = 0.0
        self.policy_value_net = PolicyValueNet(self.board_width, self.board_height, 
                                               self.n_state_channels, self.n_actions)
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      player_id=0, name="bot1", c=self.c_puct,
                                      n_simulations=self.n_simulations, is_training=True)

    def collect_selfplay_data(self, n_games=1):
        """
        collect self-play data for training
        """
        for i in range(n_games):
            winner, play_data = self.self_play_game.start_self_play(self.mcts_player, self.temp)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            self.data_buffer.extend(play_data)

    def policy_update(self):
        """
        update the policy-value net
        """
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = np.array([data[0] for data in mini_batch])
        mcts_probs_batch = np.array([data[1] for data in mini_batch])
        winner_batch = np.array([data[2] for data in mini_batch])
        old_probs, old_v = self.policy_value_net.policy_value(state_batch)
        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(
                    state_batch,
                    mcts_probs_batch,
                    winner_batch,
                    self.learn_rate*self.lr_multiplier)
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)), axis=1))
            if kl > self.kl_targ * 4:  # early stopping if D_KL diverges badly
                break
        # adaptively adjust the learning rate
        if kl > self.kl_targ * 2 and self.lr_multiplier > 0.1:
            self.lr_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.lr_multiplier < 10:
            self.lr_multiplier *= 1.5

        explained_var_old = (1 - np.var(np.array(winner_batch) - old_v.flatten()) / np.var(np.array(winner_batch)))
        explained_var_new = (1 - np.var(np.array(winner_batch) - new_v.flatten()) / np.var(np.array(winner_batch)))
        print(f"kl:{kl:.5f}\n"
              f"lr_multiplier:{self.lr_multiplier:.3f}\n"
              f"loss:{loss}\n"
              f"entropy:{entropy}\n"
              f"explained_var_old:{explained_var_old:.3f}\n"
              f"explained_var_new:{explained_var_new:.3f}\n")
        return loss, entropy

    def policy_evaluate(self, n_games=10):
        """
        Evaluate the trained policy by playing against the pure MCTS player
        Note: this is only for monitoring the progress of training
        """
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                         player_id=0, name="bot1", c=self.c_puct,
                                         n_simulations=self.n_simulations)
        
        dumb_net = PolicyValueNet(self.board_width, self.board_height, self.n_state_channels, self.n_actions)
        dumb_player = MCTSPlayer(dumb_net.policy_value_fn, player_id=1, name="bot2", n_simulations=10)
        
        win_cnt = defaultdict(int)
        for i in range(n_games):
            winner = self.self_play_game.start_eval_play([current_mcts_player, dumb_player])
            win_cnt[winner] += 1
        win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[-1]) / n_games
        print(f"win: {win_cnt[1]}, lose: {win_cnt[2]}, tie:{win_cnt[-1]}")
        return win_ratio

    def run(self):
        """
        run the training pipeline
        """
        try:
            for i in range(self.game_batch_num):
                print(f"========== Batch {i} ==========")
                print("start self-playing...")
                self.collect_selfplay_data(self.play_batch_size)
                print(f"batch i:{i+1}, episode_len:{self.episode_len}\n")
                if len(self.data_buffer) > self.batch_size:
                    print("start training step...")
                    loss, entropy = self.policy_update()
                # check the performance of the current model, and save the model params
                if (i + 1) % self.check_freq == 0:
                    print(f"current self-play batch: {i+1}")
                    win_ratio = self.policy_evaluate()
                    self.policy_value_net.save_model('models/current_policy.model')
                    if win_ratio > self.best_win_ratio:
                        print("New best policy!!!!!!!!")
                        self.best_win_ratio = win_ratio
                        # update the best_policy
                        self.policy_value_net.save_model('models/best_policy.model')
                        if (self.best_win_ratio == 1.0 and self.pure_mcts_playout_num < 5000):
                            self.pure_mcts_playout_num += 1000
                            self.best_win_ratio = 0.0
        except KeyboardInterrupt:
            print('\n\rquit')


if __name__ == '__main__':
    training_pipeline = TrainPipeline()
    training_pipeline.run()
