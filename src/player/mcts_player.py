import random
import time
import copy
import math
import numpy as np
from game_core.board import piece_id_to_owner
from player.policy_value_net import PolicyValueNet


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class Node:
    def __init__(self, parent, prior):
        self.parent = parent
        self.children = {}  # a lookup of legal child nodes
        self.n_visits = 0  # num of time this node was visited during MCTS. "good" are visited more often than "bad"
        self.Q = 0
        self.P = prior  # the prior probablity of selecting this state from its parent
        # self.player_id = player_id  # the player whose turn it is (-1 or 1)

    def is_leaf(self):
        return len(self.children) == 0
    
    def ucb_score(self, c):
        """
        Calculate and return the value (UCB score) for this node.
        It is a combination of leaf evaluations Q, and this node's prior adjusted for its visit count, u.
        c: a number in (0, inf) controlling the relative impact of value Q, and prior probability P, on this node's score.
        """
        u = c * self.P * math.sqrt(self.parent.n_visits) / (1 + self.n_visits)
        return u + self.Q
    
    def expand(self, action_probs):
        """
        Expand tree by creating new children.
        """
        for action, prob in action_probs:
            if action not in self.children.keys():
                self.children[action] = Node(self, prob)

    def select_child(self, c):
        """
        Select children with maximum UCB score.
        Return: A tuple of (action, node)
        """
        return max(self.children.items(), key=lambda action_node: action_node[1].ucb_score(c))
    
    def backpropagate(self, leaf_value):
        if self.parent:
            self.parent.backpropagate(-leaf_value)
        self.n_visits += 1
        self.Q = ((self.n_visits - 1) * self.Q + leaf_value) / self.n_visits


class MCTS:
    def __init__(self, policy_value_fn, c=5, n_simulations=400):
        """
        policy_value_fn: a function that takes in a board state and player's id, outputs
                         a list of (action, probability) tuples and also a score in [-1, 1]
                         (i.e. the expected value of the end game score from the current
                         player's perspective) for the current player.
        """
        self.root = Node(None, 1.)
        self.policy_value_fn = policy_value_fn
        self.c = c
        self.n_simulations = n_simulations
    
    def get_move_probs(self, board, player_id, temp=1e-3):
        node = self.root
        # expand the root node
        action_probs, leaf_value = self.policy_value_fn(board, player_id)
        node.expand(action_probs)

        # perform playouts {n_simulations} times
        for i in range(self.n_simulations):
            board_copy = copy.deepcopy(board)

            # select the first leaf node
            node = self.root
            while not node.is_leaf():
                action, node = node.select_child(self.c)
                piece_id, coord = board_copy.decode_move(action, player_id)
                board_copy.move_piece(piece_id, coord)
        
            # Evaluate the leaf using a network which outputs a list of action, probability) tuples p 
            # and also a score v in [-1, 1] for the current player.
            action_probs, leaf_value = self.policy_value_fn(board_copy, player_id)
            # check game finished
            finished, winner = board_copy.game_finished()
            if not finished:
                # expand the leaf node
                node.expand(action_probs)
            else:
                if winner == -1:
                    leaf_value = 0.
                else:
                    leaf_value = 1. if winner == player_id else -1.

            # update value and visit count of nodes in this traversal
            node.backpropagate(-leaf_value)

        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node_.n_visits) for act, node_ in self.root.children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))
        return acts, act_probs
    
    def update_with_move(self, last_move):
        """
        Step forward in the tree, keeping everything we already know about the subtree.
        """
        if last_move in self.root.children.keys():
            # make the child node of the select move the new root
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            # reset the tree
            self.root = Node(None, 1.)


class MCTSPlayer:
    def __init__(self, player_id, name, c=5, n_simulations=400):
        self.player_id = player_id
        self.name = name
        policy_value_net = PolicyValueNet(10, 9, 9, 192)
        self.mcts = MCTS(policy_value_net.policy_value_fn, c, n_simulations)

    def get_action(self, board):
        acts, act_probs = self.mcts.get_move_probs(board, self.player_id)
        move = np.random.choice(acts, p=act_probs)
        self.mcts.update_with_move(-1)

        return board.decode_move(move, self.player_id)