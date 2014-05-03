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


			
