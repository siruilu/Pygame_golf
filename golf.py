import os, sys
import pygame
import math
from pygame.locals import *
import ball

class GameSpace:
	def main(self):
		self.ball = ball.Ball(self)
	#	self.player1 = Player(self)
	#	self.player2 = Player(self)
		pygame.font.init()
		
		self.myfont = pygame.font.SysFont("monospace", 15)

   		self.size = self.width, self.height = 640, 480
		self.color = 0, 255, 0
		
		
    		self.screen = pygame.display.set_mode(self.size)

		while 1:		
			self.screen.fill(self.color)
			self.screen.blit(self.ball.image, self.ball.rect)

			pygame.draw.circle(self.screen, (0,0,0), (300, 300), 8)

			pygame.display.flip()


if __name__ == "__main__":
    gs = GameSpace()
    gs.main()


