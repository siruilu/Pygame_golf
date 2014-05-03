import os, sys
import pygame
import math
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
	def __init__(self,gs=None,x=100,y=100):
		pygame.sprite.Sprite.__init__(self)
		
		self.gs = gs
		self.image = pygame.image.load("/afs/nd.edu/user2/dhaberme/Public/golfball.png")

		self.rect = self.image.get_rect(center = (x,y))

		#flag to see whether player is putting
		self.tohit = False

	def tick(self):
		if self.tohit == True:
			#calculate distance from mouse to player
      			self.dx = self.gs.mx - self.rect.centerx
      			self.dy = self.gs.my - self.rect.centery   
			self.distance = math.sqrt(math.pow(self.dx, 2) + math.pow(self.dy, 2))	#pythagorean theorem
	
			#if distance is more than maximum power
			if self.distance > 100:
				#calculate angle
      				self.angle = math.atan2(self.dy, self.dx)
				
				self.powerx = self.rect.centerx + 100*math.cos(self.angle)
				self.powery = self.rect.centery + 100*math.sin(self.angle)

			#otherwise just use mouse coordinates
			else:
				self.powerx = self.gs.mx
				self.powery = self.gs.my
