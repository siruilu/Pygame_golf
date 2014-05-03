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
		self.clock = pygame.time.Clock()
		
		self.myfont = pygame.font.SysFont("monospace", 15)

   		self.size = self.width, self.height = 640, 480
		self.color = 0, 255, 0
		
		
    		self.screen = pygame.display.set_mode(self.size)

		while 1:
			#get the mouse x and y position on the screen
			self.mx, self.my = pygame.mouse.get_pos()
			
			#user inputs
      			for event in pygame.event.get():
      				if event.type == QUIT:
      			        	pygame.quit()
      				elif event.type == KEYDOWN and event.key == K_ESCAPE:
      			    		pygame.quit()
				#putt
				elif event.type == MOUSEBUTTONDOWN and event.button == 1:
					#only start putting process if ball is not moving
					if self.ball.moving == False:
						self.ball.tohit = True
				elif event.type == MOUSEBUTTONUP and event.button == 1:
					#only hit if line is drawn
					if self.ball.moving == False and self.ball.tohit == True:					
						self.ball.tohit = False
						self.ball.putt()

			
			self.ball.tick()			
			self.clock.tick(60)
			
			self.screen.fill(self.color)
			self.screen.blit(self.ball.image, self.ball.rect)

			pygame.draw.circle(self.screen, (0,0,0), (300, 300), 8)
			if self.ball.tohit == True:
				pygame.draw.line(self.screen, (0,0,0),(self.ball.linex, self.ball.liney), (self.ball.rect.centerx, self.ball.rect.centery))


			pygame.display.flip()


if __name__ == "__main__":
    gs = GameSpace()
    gs.main()


