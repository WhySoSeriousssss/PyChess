import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable


class ChessNet(nn.Module):
    def __init__(self, height, width, channel, n_actions):
        super().__init__()

        self.board_height = height
        self.board_width = width
        self.channel = channel

        # common layers
        self.conv1 = nn.Conv2d(self.channel, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        # policy net
        self.policy_conv1 = nn.Conv2d(128, 32, kernel_size=3, padding=1)
        self.policy_conv2 = nn.Conv2d(32, 4, kernel_size=3, padding=1)
        self.policy_fc1 = nn.Linear(4 * self.board_height * self.board_width, n_actions)

        # value net
        self.value_conv1 = nn.Conv2d(128, 16, kernel_size=3, padding=1)
        self.value_conv2 = nn.Conv2d(16, 2, kernel_size=3, padding=1)
        self.value_fc1 = nn.Linear(2 * self.board_height * self.board_width, 64)
        self.value_fc2 = nn.Linear(64, 1)

    def forward(self, input):
        # common layers
        x = F.relu(self.conv1(input))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # policy net
        x_policy = F.relu(self.policy_conv1(x))
        x_policy = F.relu(self.policy_conv2(x_policy))
        x_policy = x_policy.view(-1, 4 * self.board_height * self.board_width)
        x_policy = F.log_softmax(self.policy_fc1(x_policy), dim=1)

        # value net
        x_value = F.relu(self.value_conv1(x))
        x_value = F.relu(self.value_conv2(x_value))
        x_value = x_value.view(-1, 2 * self.board_height * self.board_width)
        x_value = F.relu(self.value_fc1(x_value))
        x_value = F.tanh(self.value_fc2(x_value))

        return x_policy, x_value


class PolicyValueNet():
    def __init__(self, board_height, board_width, n_state_channels, n_actions):
        self.board_height = board_height
        self.board_width = board_width
        self.n_state_channels = n_state_channels
        self.n_actions = n_actions
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.model = ChessNet(board_height, board_width, n_state_channels, n_actions).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), weight_decay=1e-4)

    def policy_value_fn(self, board, player_id):
        """
        input: board, player_id
        output: a list of (action, probability) tuples for each available action and the score of the board state
        """
        # evaluate the current state of the board
        eval_state = board.get_eval_state(player_id)
        eval_state = np.ascontiguousarray(eval_state.reshape(-1, self.n_state_channels, self.board_height, self.board_width))
        log_act_probs, value = self.model(Variable(torch.from_numpy(eval_state)).to(self.device).float())
        act_probs = np.exp(log_act_probs.data.cpu().numpy().flatten())
        value = value.data[0][0]
        # filter out the unavailable actions, normalize the new act_probs
        legal_moves = board.get_player_encoded_availables(player_id)
        act_probs[np.array(legal_moves) == 0] = 0.
        act_probs /= np.sum(act_probs)
        act_probs = zip(np.nonzero(legal_moves)[0], act_probs)
        return act_probs, value
    