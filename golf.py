#!/usr/bin/python

import os, sys
import pygame
import math
from pygame.locals import *
from pygame.color import THECOLORS
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
import ball


class GameSpace:
	#initiate player with number
	def __init__(self, num, connection):
		self.player = num
		self.connection = connection


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

		#whose turn it is
		self.turn = 1
		
		
    		self.screen = pygame.display.set_mode(self.size)

		#make image backgrounds transparent
		self.ball1.image.convert_alpha()
		self.ball1.image.set_colorkey(THECOLORS['white'])
		self.ball2.image.convert_alpha()
		self.ball2.image.set_colorkey(THECOLORS['white'])


		while 1:
			#send data over connection
			if self.player == 1:
				self.connection.transport.write(str(self.ball1.rect.centerx) + "," + str(self.ball1.rect.centery))
			if self.player == 2:
				self.connection.transport.write(str(self.ball2.rect.centerx) + "," + str(self.ball2.rect.centery))


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
					#determine if it is your turn
					if self.turn == 1 and self.player == 1:					
						#only start putting process if ball is not moving
						if self.ball2.moving == False and self.ball1.inHole == False:
							self.ball1.tohit = True
					elif self.turn == 2 and self.player == 2:
						if self.ball1.moving == False and self.ball2.inHole == False:
							self.ball2.tohit = True
				elif event.type == MOUSEBUTTONUP and event.button == 1:
					if self.turn == 1 and self.player == 1:
						#only hit if line is drawn
						if self.ball2.moving == False and self.ball1.tohit == True and self.ball1.inHole == False:					
							self.ball1.tohit = False
							self.ball1.putt()
							#switch turn to next player if not done
							if self.ball2.inHole == False:
								self.turn = 2
							
					elif self.turn == 2 and self.player == 2: 					
						if self.ball1.moving == False and self.ball2.tohit == True and self.ball2.inHole == False:					
							self.ball2.tohit = False
							self.ball2.putt()
							if self.ball1.inHole == False:
								self.turn = 1

			#update all objects
			self.ball1.tick()
			self.ball2.tick()			
			self.clock.tick(60)
			
			self.screen.fill(self.color)
			#draw hole and balls
			pygame.draw.circle(self.screen, (0,0,0), (self.holex, self.holey), 8)
			self.screen.blit(self.ball1.image, self.ball1.rect)
			self.screen.blit(self.ball2.image, self.ball2.rect)

			#draw line for putting
			if self.ball1.tohit == True:
				pygame.draw.line(self.screen, (0,0,0),(self.ball1.linex, self.ball1.liney), (self.ball1.rect.centerx, self.ball1.rect.centery))
		
			if self.ball2.tohit == True:
				pygame.draw.line(self.screen, (0,0,0),(self.ball2.linex, self.ball2.liney), (self.ball2.rect.centerx, self.ball2.rect.centery))

			#display turn and strokes
     			self.turn_label = self.myfont.render("Player " + str(self.turn) + "'s Turn", 1, THECOLORS['black'])
			self.strokes1 = self.myfont.render("Player 1 Strokes: " + str(self.ball1.strokes), 1, THECOLORS['blue'])
			self.strokes2 = self.myfont.render("Player 2 Strokes: " + str(self.ball2.strokes), 1, THECOLORS['red'])
      			self.screen.blit(self.turn_label, (495, 0) )
			self.screen.blit(self.strokes1, (457, 15) )
			self.screen.blit(self.strokes2, (457, 30) )
			

			pygame.display.flip()


#networking classes
class Connection(Protocol):
	def dataReceived(self, data):
		print 'Receive'
		#data contains positions

		#parse data
		data.partition(',')
			
		#change other player's ball position
		if int(sys.argv[1]) == 1:							
			gs.ball2.rect.center = (data[0], data[2])				
		if int(sys.argv[1]) == 2:							
			gs.ball1.rect.center = (data[0], data[2])	
			
		
  	def connectionMade(self):
		print 'Connected to other player'
		gs = GameSpace(int(sys.argv[1]), self)   #initate game and pass self
		gs.main()

		
class ConnectionFactory(ClientFactory):
 	def buildProtocol(self, addr):
	  	return Connection()



if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print 'Incorrect number of arguments'
		print 'usage: python2.6 golf.py <player number (1 or 2)>'
		sys.exit(2)
	elif int(sys.argv[1]) != 1 and int(sys.argv[1]) != 2:
		print 'Player number must be 1 or 2'
		sys.exit(2)
	else:	
		#if argument correct, run program
		if int(sys.argv[1]) == 1:
			reactor.listenTCP(40034, ConnectionFactory())
			reactor.run()
		elif int(sys.argv[1]) == 2:
			reactor.connectTCP("student03.cse.nd.edu", 40034, ConnectionFactory())
			reactor.run() 	
	

		


