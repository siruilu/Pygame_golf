import os, sys
import pygame
import math
from pygame import locals

class Ball(pygame.sprite.Sprite):
	def __init__:
		pygame.sprite.Sprite.__init__(self)
		
		self.gs = gs
		self.image = pygame.image.load("/afs/nd.edu/user2/dhaberme/Public/golfball.png")

		self.rect = self.image.get_rect()

		self.orig_image = self.image
