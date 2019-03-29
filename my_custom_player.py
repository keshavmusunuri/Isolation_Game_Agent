
from sample_players import DataPlayer
import random

class CustomPlayer(DataPlayer):
    """ Implement customized agent to play knight's Isolation """

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least
        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.
        See RandomPlayer and GreedyPlayer in sample_players for more examples.
        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        depth_limit = 20

        if state.ply_count < 4 and self.data is not None:
            if state in self.data:
                self.queue.put(self.data[state])
            else:
                self.queue.put(random.choice(state.actions()))
        else:
            for depth in range(1, depth_limit+1):
                best_move = self.alpha_beta_search(state, depth)
                if best_move is not None:
                   self.queue.put(best_move)
        
    def alpha_beta_search(self, state, depth):    

        def min_value(state, depth, alpha, beta):

            val = float("inf")

            if state.terminal_test():
               return state.utility(self.player_id)

            if depth <= 0 : 
              return self.score(state)
            
            for action in state.actions():
                val = min(val, max_value(state.result(action), depth - 1, alpha, beta))
                if val <= alpha:
                   return val
                beta = min(beta, val)
            return val 

        def max_value(state, depth, alpha, beta):
            val = float("-inf")

            if state.terminal_test(): 
              return state.utility(self.player_id)

            if depth <= 0 : 
              return self.score(state)
              
            for action in state.actions():
                val = max(val, min_value(state.result(action), depth - 1, alpha, beta))
                if val >= beta:
                   return val
                alpha = max(alpha, val)
            return val
        
        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1, float('-inf'), float('inf')))       
        
    def score(self, state):
        width = 11
        height = 9
        borders = [
            [(0, widths) for widths in range(width)],
            [(heights, 0) for heights in range(height)],
            [(height - 1, widths) for widths in range(width)],
            [(width - 1, heights) for heights in range(height)]
        ]
        player_loc = state.locs[self.player_id]
        opponent_loc = state.locs[1 - self.player_id]
        player_liberties = state.liberties(player_loc)     
        opponent_liberties = state.liberties(opponent_loc)
        if self.at_border(player_loc, borders):
          next_opponent_liberties = [len(state.liberties(next_move)) for next_move in opponent_liberties]
          return len(player_liberties) - 3 * (len(opponent_liberties) + sum(next_opponent_liberties))  
        else:
          return len(player_liberties) - 3 * (len(opponent_liberties))

    def at_border(self, locs, borders):
        for border in borders:
          return locs in border
