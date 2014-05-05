Pygame Mini Golf Game
=====================
Programmed by Sirui Lu and Darin Habermel for CSE 30332 Final Project


Getting Started
===============
First, make sure that Player 1 is logged into student03.cse.nd.edu, since that is where the server must be run from. Then, once both players are in the correct directory in the terminal, Player 1 should start the server by running "python2.6 golf.py 1" in the command line. Then, Player 2 should run "python2.6 golf.py 2" and the game windows should pop up for both players.

The Basics
==========
Once the game is running, each player will take turns trying to hit the ball into the hole, with Player 1 going first. To hit the ball, click and hold the mouse button down somewhere on the game screen, and a line should appear. While holding the mouse down, the player can the line around. This line simulates the angle and power with which the player is hitting the ball. Keep in mind that the further back the line goes, the faster the ball will move in the opposite direction. 
The players will take turns hitting the ball until both players have made the ball into the hole. Then, the game will move on to the next hole in the course, keeping track of both player's scores relative to the "par" score. After the 9th and final hole, the game will end, declaring a winner and showing the scores of both players.

Environmental Features
======================
Each hole in the course is designed as a sort of maze, with walls that the ball cannot go through. If you are having trouble with the ball getting stuck on the walls, please see the Troubleshooting section below. Also, some holes will have extra environmental features, such as sand traps and water. Watch out for these! If a ball is hit into a sand trap, its speed will slow down dramatically, and if a ball is hit into the water, the ball will return to the place it was hit from, and the player will still be given a stroke.

Troubleshooting
===============
The walls will occasionally have a problem with the ball getting stuck on them. This is due to the ball trying not moving far enough after colliding with the wall to be completely outside of the wall's rectangle. The ball's velocity will then oscillate between positive and negative. We attempted to put checks in there to prevent this, but it will still happen occasionally, especially when walls are close together. If this happens, hit the ball directly at the wall and the velocity should be great enough that you will escape this issue.























