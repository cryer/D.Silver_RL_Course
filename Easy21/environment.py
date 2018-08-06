import numpy as np
import random


class Easy21(object):
    def __init__(self):
        self.playersum = random.randint(1,10)
        self.dealerfirst = random.randint(1,10)
        self.dealersum = self.dealerfirst
        self.game_end = False
        self.winner = 'none'
    
    def reset(self):
        return Easy21()
        
    def State(self):
        playersum = self.playersum
        dealerfirst = self.dealerfirst
        return [playersum,dealerfirst]
        
    def is_game_end(self):
        return self.game_end
        
    def draw_a_card(self):
        if random.randint(1,3) < 3:
            return int(random.randint(1,10))
        else:
            return -int(random.randint(1,10))
    
    # action {hit,stick}
    def step(self,action):
        if action == 0:
            self.playersum += self.draw_a_card()
            if self.playersum < 1 or self.playersum > 21:
                self.game_end = True
                self.winner = 'dealer'
                return self.State(), -1.0
            else:
                self.game_end = False
                self.winner = 'none'
                return self.State(), 0
        elif action == 1:
            while(self.dealersum < 17):
                self.dealersum = self.dealersum + self.draw_a_card()
                # print("curr dealer sum:",self.dealersum)
                if self.dealersum < 1 or self.dealersum > 21:
                    self.game_end = True
                    self.winner = 'player'
                    return self.State(), 1.0
            if self.dealersum > self.playersum:
                self.game_end = True
                self.winner = 'dealer'
                return self.State(), -1.0
            elif self.dealersum < self.playersum:
                self.game_end = True
                self.winner = 'player'
                return self.State(), 1.0
            else:
                self.game_end = True
                self.winner = 'none'
                return self.State(), 0.0
    
    def start_game(self):
        while not (self.is_game_end()):
            print('___你的手牌点数___:',self.playersum)
            print('___庄家手牌点数___:',self.dealersum)
            print("抓牌0或者放弃1：")
            a = input()
            state,win = self.step(int(a))
        if self.winner == "player":
            print('You Win!!')
        elif self.winner == "dealer":
            print('YOU Lose!')
        else:
            print('Tie!')
        
if __name__ == '__main__':
    game = Easy21()
    game.start_game()
        
        
