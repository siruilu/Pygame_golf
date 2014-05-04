import os, sys
import pygame
import math
from pygame.locals import *
from pygame.color import THECOLORS
import ball

class GameSpace:
	def main(self):
		self.ball1 = ball.Ball(self)
		self.ball2 = ball.Ball(self)

		pygame.font.init()
		self.clock = pygame.time.Clock()
		
		self.myfont = pygame.font.SysFont("monospace", 15)

   		self.size = self.width, self.height = 640, 480
		self.color = 0, 255, 0

		#position of hole
		self.holex = 400
		self.holey = 300
		
		
    		self.screen = pygame.display.set_mode(self.size)

		self.ball1.image.convert_alpha()
		self.ball1.image.set_colorkey(THECOLORS['white'])


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
					if self.ball1.moving == False and self.ball1.inHole == False:
						self.ball1.tohit = True
				elif event.type == MOUSEBUTTONUP and event.button == 1:
					#only hit if line is drawn
					if self.ball1.moving == False and self.ball1.tohit == True and self.ball1.inHole == False:					
						self.ball1.tohit = False
						self.ball1.putt()

			
			self.ball1.tick()			
			self.clock.tick(60)
			
			self.screen.fill(self.color)
			#draw hole and ball
			pygame.draw.circle(self.screen, (0,0,0), (self.holex, self.holey), 8)
			self.screen.blit(self.ball1.image, self.ball1.rect)

			#draw line for putting
			if self.ball1.tohit == True:
				pygame.draw.line(self.screen, (0,0,0),(self.ball1.linex, self.ball1.liney), (self.ball1.rect.centerx, self.ball1.rect.centery))


			pygame.display.flip()


if __name__ == "__main__":
    gs = GameSpace()
    gs.main()


