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
		self.vx = 0     #velocity
		self.vy = 0
		self.strokes = 0
		self.justCollided=0#using this variable really helps with balls getting stuck on walls from what I saw. Doesn't completely stop it though

		#determines the loss of velocity
		self.friction = .96

		self.initialx = x
		self.initialy = y
		
		#flags to indicate state of ball
		self.tohit = False
		self.moving = False
		self.inHole = False

	def tick(self):
		if self.tohit == True:
			#calculate distance from mouse to player
      			self.dx = self.gs.mx - self.rect.centerx
      			self.dy = self.gs.my - self.rect.centery   
			self.distance = math.sqrt(math.pow(self.dx, 2) + math.pow(self.dy, 2))	#pythagorean theorem
	
			#if distance is more than maximum power
			if self.distance > 100:
				#calculate angle and where line should be
      				self.angle = math.atan2(self.dy, self.dx)
				
				self.powerx = 100*math.cos(self.angle)
				self.powery = 100*math.sin(self.angle)
				self.linex = self.rect.centerx + self.powerx
				self.liney = self.rect.centery + self.powery

			#otherwise just use mouse coordinates
			else:
				self.linex = self.gs.mx
				self.liney = self.gs.my
				self.powerx = self.linex - self.rect.centerx
				self.powery = self.liney - self.rect.centery

		#if not preparing to hit, move ball
		elif self.moving == True:
			self.detect_collision()
			newpos = self.rect.move((self.vx, self.vy))
      			self.rect = newpos
			self.vx *= self.friction
			self.vy *= self.friction		

			if self.vx < 0.1 and self.vx > -0.1 and self.vy > -0.1 and self.vy < 0.1:
				self.vx = 0
				self.vy = 0
				self.moving = False

		#if ball is in hole
		elif self.inHole == True:
			self.rect.center = (self.gs.course.hole_location[0], self.gs.course.hole_location[1])


	#adjust velocity if ball interacts with some environment object 
	def detect_collision(self):

		#Collision detection based entirely on sprite collision
		if (self.justCollided == 0):
			if pygame.sprite.spritecollideany(self, self.gs.course.vertwalls):
				self.vx *= -1

			if pygame.sprite.spritecollideany(self, self.gs.course.horizwalls):
				self.vy *= -1

			#check if ball is in hole
			if self.rect.collidepoint(self.gs.course.hole_location[0], self.gs.course.hole_location[1]):
				self.vy = 0
				self.vx = 0
				self.inHole = True
			justCollided = 1
		else:
			justCollided = 0

		
		#if ball is in sand trap, adjust velocity accordingly
		if self.gs.course.sandRect.collidepoint(self.rect.center):
			self.friction = .65
		else:
			self.friction = .96

		#if ball falls into water, put back into initial place and add one penalty stroke
		if self.gs.course.sandRect.collidepoint(self.rect.center):
			self.vx = 0
			self.vy = 0
			self.rect.center = (self.initialx, self.initialy)
			self.strokes+=1
		

	#hit ball
	def putt(self):
		self.moving = True
		#initiate movement
		self.vx = -self.powerx/5
		self.vy = -self.powery/5
		self.strokes+=1
		#save initial point in case ball goes into water trap
		self.initialx = self.rect.centerx
		self.initialy = self.rect.centery
		
		
		
