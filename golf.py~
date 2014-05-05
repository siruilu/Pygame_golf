#!/usr/bin/python

import os, sys
import pygame
import math
from pygame.locals import *
from pygame.color import THECOLORS
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
import ball, course


class GameSpace:
	#initiate player with number and variables
	def __init__(self, num, connection):
		self.player = num
		self.connection = connection
		
		pygame.font.init()
		self.clock = pygame.time.Clock()
		
		self.myfont = pygame.font.SysFont("monospace", 15)

   		self.size = self.width, self.height = 640, 480
		self.color = 0, 255, 0

		#whose turn it is
		self.turn = 1

		#hole number
		self.hole_num = 4

		#initiate first hole
		self.next_hole()

		#temporary variables for receiving data over connection		
		self.xpos = 100
		self.ypos = 100
		self.other_score = 0
		self.tohit = False
		self.moving = False
		self.inhole = False

		self.player1score = 0  #Will be used to keep track of player totals across courses
		self.player2score = 0

		self.finished = False
		
    		self.screen = pygame.display.set_mode(self.size)

	#on to next hole
	def next_hole(self):
		self.course = course.Course(self, str(self.hole_num))
		self.ball1 = ball.Ball(self, self.course.ball_location[0], self.course.ball_location[1])
		self.ball2 = ball.Ball(self, self.course.ball_location[0], self.course.ball_location[1])

		#Gives each player their own color ball
		self.ball1.image = pygame.image.load("/afs/nd.edu/user2/dhaberme/Public/red_golfball.fw.png")
		self.ball2.image = pygame.image.load("/afs/nd.edu/user2/dhaberme/Public/blue_golfball.fw.png")

		#set background
		self.background = pygame.image.load("/afs/nd.edu/user2/dhaberme/Public/background3.png")
        	self.backgroundRect = self.background.get_rect()

		#reset turn and flags
		self.turn = 1

		self.ball1.tohit = False
		self.ball1.moving = False
		self.ball1.inHole = False
		
		self.ball2.tohit = False
		self.ball2.moving = False
		self.ball2.inHole = False



	#receive data sent from other player
	def set_data(self, xpos, ypos, other_score, tohit, moving, inhole):
		self.xpos = int(xpos)
		self.ypos = int(ypos)
		self.other_score = int(other_score)

		if tohit == "True":
			self.tohit = True
		else:
			self.tohit = False

		if moving == "True":
			self.moving = True
		else:
			self.moving = False

		if inhole == "True":
			self.inhole = True
		else:
			self.inhole = False
		


	#main loop
	def main(self):
		#send data over connection
		if self.player == 1:
			self.connection.transport.write(str(self.ball1.rect.centerx) + "," + str(self.ball1.rect.centery) + "," + str(self.ball1.strokes) + "," + str(self.ball1.tohit) + "," + str(self.ball1.moving) + "," + str(self.ball1.inHole) )
		if self.player == 2:
			self.connection.transport.write(str(self.ball2.rect.centerx) + "," + str(self.ball2.rect.centery) + "," + str(self.ball2.strokes) + "," + str(self.ball2.tohit) + "," + str(self.ball2.moving) + "," + str(self.ball2.inHole) )

			
		#set information from data received
		if self.player == 1:
			self.ball2.rect.center = (self.xpos, self.ypos)
			self.ball2.strokes = self.other_score
			self.ball2.tohit = self.tohit
			self.ball2.moving = self.moving
			self.ball2.inHole = self.inhole
		if self.player == 2:
			self.ball1.rect.center = (self.xpos, self.ypos)		
			self.ball1.strokes = self.other_score
			self.ball1.tohit = self.tohit
			self.ball1.moving = self.moving
			self.ball1.inHole = self.inhole
		

		#if both balls are not in hole, continue gameplay
		if self.ball1.inHole == False or self.ball2.inHole == False:

			#set turn
			if self.ball1.inHole == True:
				self.turn == 2
			elif self.ball2.inHole == True:
				self.turn == 1
			elif self.ball2.strokes < self.ball1.strokes:
				self.turn = 2
			elif self.ball1.inHole == False:	
				self.turn = 1			

			#get the mouse x and y position on the screen
			self.mx, self.my = pygame.mouse.get_pos()

			#user inputs
      			for event in pygame.event.get():
      				if event.type == QUIT:
      			        	pygame.quit()
					reactor.stop()
      				elif event.type == KEYDOWN and event.key == K_ESCAPE:
      			    		pygame.quit()
					reactor.stop()
				#putt
				elif event.type == MOUSEBUTTONDOWN and event.button == 1:
					#determine if it is your turn
					if self.turn == 1 and self.player == 1:					
						#only start putting process if ball is not moving
						if self.ball2.moving == False and self.ball1.inHole == False and self.ball1.moving == False:
							self.ball1.tohit = True
					elif self.turn == 2 and self.player == 2:
						if self.ball1.moving == False and self.ball2.inHole == False and self.ball2.moving == False:
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
							#after putt, switch turn and tell other player 
							if self.ball1.inHole == False:
								self.turn = 1
				#for testing only
#				elif event.type == KEYDOWN and event.key == K_UP:
#					self.ball2.inHole = True
#					self.ball1.inHole = True

			#update all objects
			self.ball1.tick()
			self.ball2.tick()			
			self.clock.tick(60)
			
			self.screen.fill(self.color)
			
			#draw hole and balls
 			self.screen.blit(self.background, self.backgroundRect)
			if self.course.sandimage != None:
				self.screen.blit(self.course.sandimage, self.course.imageRect)
			self.screen.blit(self.course.image, self.course.rect)
			self.screen.blit(self.ball1.image, self.ball2.rect)
			self.screen.blit(self.ball2.image, self.ball1.rect)
			self.course.tick()


			#draw line for putting
			if self.ball1.tohit == True and self.player == 1:
				pygame.draw.line(self.screen, (0,0,0),(self.ball1.linex, self.ball1.liney), (self.ball1.rect.centerx, self.ball1.rect.centery))
		
			if self.ball2.tohit == True and self.player == 2:
				pygame.draw.line(self.screen, (0,0,0),(self.ball2.linex, self.ball2.liney), (self.ball2.rect.centerx, self.ball2.rect.centery))


			#display turn and strokes
     			self.turn_label = self.myfont.render("Player " + str(self.turn) + "'s Turn", 1, THECOLORS['black'])
			self.strokes1 = self.myfont.render("Player 1 Strokes: " + str(self.ball1.strokes), 1, THECOLORS['blue'])
			self.strokes2 = self.myfont.render("Player 2 Strokes: " + str(self.ball2.strokes), 1, THECOLORS['red'])
      			self.screen.blit(self.turn_label, (495, 0) )
			self.screen.blit(self.strokes1, (457, 15) )
			self.screen.blit(self.strokes2, (457, 30) )

			#display total score for each player
   			self.player1total = self.myfont.render("Player 1 Total: " + str(self.player1score), 1, THECOLORS['blue'])
        		self.player2total = self.myfont.render("Player 2 Total: " + str(self.player2score), 1, THECOLORS['red'])
            		self.screen.blit(self.player1total, (5, 15))
            		self.screen.blit(self.player2total, (5,30))
			

			pygame.display.flip()

		#if both players are done with hole and not to end of course yet
		elif self.hole_num < 9:
			self.player1score = self.player1score + (int(self.ball1.strokes) - int(self.course.par) + 1)
			self.player2score = self.player2score + (int(self.ball2.strokes) - int(self.course.par) + 1)
			self.hole_num += 1
			self.next_hole()

		#this means done with course, calculate score one last time
		elif self.finished == False:
			
			self.player1score = self.player1score + (int(self.ball1.strokes) - int(self.course.par) + 1)
			self.player2score = self.player2score + (int(self.ball2.strokes) - int(self.course.par) + 1)
			self.finished = True

		else:
		
			if self.player1score < self.player2score:
				self.end_label = self.myfont.render("Player 1 Wins!!", 1, THECOLORS['black'])
			elif self.player2score < self.player1score:
				self.end_label = self.myfont.render("Player 2 Wins!!", 1, THECOLORS['black'])
			else:
				self.end_label = self.myfont.render("It is a tie!", 1, THECOLORS['black'])

			self.end1 = self.myfont.render("Player 1 Final Strokes: " + str(self.player1score), 1, THECOLORS['blue'])
			self.end2 = self.myfont.render("Player 2 Final Strokes: " + str(self.player2score), 1, THECOLORS['red'])

			self.screen.fill(self.color)
	      		self.screen.blit(self.end_label, (240, 215) )
			self.screen.blit(self.end1, (240, 230) )
			self.screen.blit(self.end2, (240, 245) )

			pygame.display.flip()

			#allow user to exit game
			for event in pygame.event.get():
      				if event.type == QUIT:
      			        	pygame.quit()
					reactor.stop()
      				elif event.type == KEYDOWN and event.key == K_ESCAPE:
      			    		pygame.quit()
					reactor.stop()


#networking classes
class Connection(Protocol):
	def dataReceived(self, data):

		#parse data
		parsed = data.split(',')
			
		#call function that handles data
		self.gs.set_data(parsed[0], parsed[1], parsed[2], parsed[3], parsed[4], parsed[5])			
		
		#run main loop
		self.gs.main()

					
  	def connectionMade(self):
		print 'Connected as Player ' + str(sys.argv[1])
		#when connected, make game and run main loop once
		self.gs = GameSpace(int(sys.argv[1]), self)
		self.gs.main()
		

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
	

		


		


