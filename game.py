# Tamsin Rogers
# December 9, 2019
# CS 152 
# Project 11: Something Interactive
# run this program from the Terminal by entering "python3 game.py"
# this program is an interactive game in which the user scores points by bouncing a ball off the block and colliding with the snowmen objects and loses points by colliding with the hot chocolate objects

#import necessary packages and files
import physics_objects as pho
import collision																			
import graphicsPlus as gr
import random
import time
import math
from graphicsPlus import *
import playsound
from playsound import playsound

answer = input("Enter your name here:")														#command line entry
playsound('bg.mp3', False)																	#play the background music
print("Game Loading ...")																	#let the user know the game is loading

"""creates the wall around the window and puts the block objects in the returned list thewall."""
def buildWall(win):
	rightwall = pho.Block(win)
	rightwall = pho.Block(win)
	rightwall.setPosition(70,0)
	rightwall.setHeight(150)
	rightwall.setWidth(1.5)
	rightwall.setColor((255,255,255))
	rightwall.setElasticity(.3)
	leftwall = pho.Block(win)
	leftwall.setPosition(0,50)
	leftwall.setHeight(150)
	leftwall.setWidth(1.5)
	leftwall.setColor((255,255,255))
	leftwall.setElasticity(.3)
	topwall = pho.Block(win)
	topwall.setPosition(0,70)
	topwall.setElasticity(.3)
	topwall.setColor((255,255,255))
	bottomwall = pho.Block(win)
	bottomwall.setPosition(10,0)
	bottomwall.setElasticity(.3)
	bottomwall.setColor((255,255,255))
	thewall = [topwall, bottomwall, leftwall, rightwall]
	return thewall

"""creates the startscreen window - seen by user at the start of the game"""	
def startscreen():
	win = gr.GraphWin( 'startscreen', 700, 700, False )										#create a GraphWin
	background = Image(Point(350,350), "start.png")											#set the background image to the snow scene
	background.draw(win)
	shapes = buildWall(win)																	#call buildWall, storing the return list in a variable
	
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()
	
	rotate = pho.RotatingBlock(win, 45, 45, 13, 13)											#draw a rotating block behind the "click here" textbox
	rotate.setColor((255,255,255))
	rotate.draw()
	rotate.setRotVelocity(20)
	
	click = gr.Text( gr.Point( 445, 250 ), ("click here \n to start") )						#create a textbox
	click.setSize(20)
	click.setTextColor("blue")
	click.setStyle('bold')
	click.draw(win)
	
	space = gr.Text(gr.Point(155, 680), ("press Space for instructions"))					#create a textbox
	space.setSize(20)
	space.setTextColor("black")
	space.setStyle('bold')
	space.draw(win)
	dt = 0.02	  
	
	while True:	   
		key = win.checkKey()													  
		for i in range(10000):																#update the rotating block
			rotate.update(dt)
			click.undraw()
			click.draw(win)
			if i % 10:
				win.update()
				time.sleep(0.01)
			key = win.checkKey()
			if key == "space":																#if the user presses the space key (wants to see instructions)
				playsound("click.mp3", False)												#play the click sound effect
				win.close()																	#close the startscreen window
				instructions()																#call the instructions function
			elif win.checkMouse() != None:													#if the user clicks the mouse (wants to play the game)
				playsound("click.mp3", False)												#play the click sound effect
				win.close()																	#close the startscreen window
				main()																		#call the main function - user plays the game
	return answer																			#set the user's command line answer to their player name
	
"""creates the instructions window - seen by user if they press the space key"""	
def instructions():
	win = gr.GraphWin( 'instructions', 700, 700, False )									#create a GraphWin
	background = Image(Point(350,350), "instructions.png")									#set the background image to the instructions
	background.draw(win)
	shapes = buildWall(win)																	#call buildWall, storing the return list in a variable
	
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()
	
	rotate = pho.RotatingBlock(win, 60, 62, 7.5, 7.5)										#draw a rotating block behind the "click here" textbox
	rotate.setColor((255,255,255))
	rotate.draw()
	rotate.setRotVelocity(20)
	
	click = gr.Text( gr.Point( 600, 85 ), ("click here \n to practice") )					#create a textbox
	click.setSize(13)
	click.setTextColor("blue")
	click.setStyle('bold')
	click.draw(win)
	dt = 0.02
							
	for i in range(10000):																	#update the rotating block
		rotate.update(dt)
		click.undraw()
		click.draw(win)
		if i % 10:
			win.update()
			time.sleep(0.01)
		if win.checkMouse() != None:														#if the user clicks the mouse (wants to practice)
			playsound("click.mp3", False)													#play the click sound effect
			win.close()																		#close the instructions window
			practice()																		#call the practice function
	return answer

"""creates the practice window - seen by user if they select that they want to practice before playing"""
def practice():
	win = gr.GraphWin( 'instructions', 700, 700, False )									#create a GraphWin
	background = Image(Point(230,245), "main.png")											#set the background image to the snow scene
	background.draw(win)
	shapes = buildWall(win)	
	
	block = pho.Block(win)																	#draw a block behind the "click here" textbox
	block.setWidth(10)
	block.setHeight(7)
	block.setPosition(60,61)
	block.setColor((255,255,255))
	block.draw()																			#call buildWall, storing the return list in a variable
	
	click = gr.Text( gr.Point( 600, 90 ), ("click here \n when you're \n ready to play!") )	#create a textbox
	click.setSize(13)
	click.setTextColor("blue")
	click.setStyle('bold')
	click.draw(win)
	
	dt = 0.02																
	frame = 0
	if frame%10 == 0:
			win.update()
	
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()	
	
	ball = pho.Ball(win)																	#create the main ball
	ball.setPosition( 50, 50 )
	ball.setVelocity( 15, -40 )
	ball.setAcceleration( 0,1 )
	ball.setElasticity(2)
	ball.setColor((255,255,255))
	ball.setMass(20)
	ball.draw()
	
	sled = pho.Block(win)																	#create the user-controlled block for the ball to bounce off
	sled.setHeight(1.5)
	sled.setWidth(20)
	sled.setPosition(50,10)
	sled.setColor((0,0,250))
	sled.setElasticity(1)
	sled.draw()
	
	while True:
		collided = False
		time.sleep( 0.033 )											
		key = win.checkKey()
		
		if win.checkMouse():																#if the user clicks the mouse (wants to play the game)
			playsound("click.mp3", False)													#play the click sound effect
			win.close()																		#close the practice window
			main()																			#run the main game function
		
		#USER KEY CONTROLS
		if key == 'Left':																	#if the user clicked the left arrow button
			sled.moveLeft()																	#move the sled to the left
		if key == 'Right':																	#if the user clicked the right arrow button
			sled.moveRight()				   												#move the sled to the right
		if key == 'Up':																		#if the user clicked the up arrow button
			sled.moveUp()																	#move the sled up
		if key == 'Down':																	#if the user clicked the down arrow button
			sled.moveDown()																	#move the sled down
		
		collided = False																	#the ball has not collided with anything
		
		for i in shapes:																	
			if collision.collision(ball, i, .01) == True:									#if the ball collides with a wall
				collided = True																#bounce off the wall
		if collision.collision(ball, sled, .01) == True:									#if the ball collides with the sled
			playsound("bounce.mp3", False)													#play the bounce sound effect
			collided = True																	#bounce off the sled
		if collided == False:
			ball.update(dt)
		frame = frame + 1
		win.update()

"""creates the winscreen window - seen by user once they score 10 points in the game"""
def winscreen():
	win = gr.GraphWin( 'win', 700, 700, False )												#create a GraphWin
	background = Image(Point(350,350), "win.png")								   			#set the background image to the win image
	background.draw(win)
	shapes = buildWall(win)																	#call buildWall, storing the return list in a variable
	
	playsound("gamewin.mp3", False)															#play the win sound effect
	
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()
	
	textbox1 = gr.Text( gr.Point( 350, 50 ), ("You won!  Final score: 10") )				#create a textbox
	textbox1.setSize(30)
	textbox1.setTextColor("green")
	textbox1.setStyle('bold')
	textbox1.draw(win)
	
	click = gr.Text( gr.Point( 400, 200 ), ("Click here \n to play again") )				#create a textbox
	click.setSize(20)
	click.setTextColor("blue")
	click.setStyle('bold')
	click.draw(win)
	
	rotate = pho.RotatingBlock(win, 40, 50, 12.5, 12.5)										#draw a rotating block behind the "click here" textbox
	rotate.setColor((255,255,255))
	rotate.draw()
	rotate.setRotVelocity(20)
	dt = 0.02
	
	for i in range(1000):																	#update the rotating block
		rotate.update(dt)
		click.undraw()																		#update the textbox
		click.draw(win)
		if i % 10:
			win.update()
			time.sleep(0.01)
		if win.checkMouse() != None:														#if the user clicks the mouse (wants to play the game again)
			playsound("click.mp3", False)													#play the click sound effect
			win.close()																		#close the winscreen window
			startscreen()																	#call the start screen function - bring the user back to the start screen

"""creates the losescreen window - seen by user if they reach 0 points"""			
def losescreen():
	win = gr.GraphWin( 'lose', 700, 700, False )											#create a GraphWin
	background = Image(Point(350,350), "lose.png")
	background.draw(win)
	shapes = buildWall(win)																	#call buildWall, storing the return list in a variable
	
	playsound("gamelose.mp3", False)														#play the lose sound effect
	
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()
	
	textbox1 = gr.Text( gr.Point( 250, 50 ), ("You lost - the snowman melted.") )			#create a textbox
	textbox1.setSize(30)
	textbox1.setTextColor("red")
	textbox1.setStyle('bold')
	textbox1.draw(win)
	
	click = gr.Text( gr.Point( 497, 200 ), ("Click here \n to try again") )					#create a textbox
	click.setSize(20)
	click.setTextColor("blue")
	click.setStyle('bold')
	click.draw(win)
	
	rotate = pho.RotatingBlock(win, 50, 50, 13, 13)									  		#draw a rotating block behind the "click here" textbox
	rotate.setColor((255,255,255))
	rotate.draw()
	rotate.setRotVelocity(20)
	dt = 0.02
	
	for i in range(1000):																	#update the rotating block
		rotate.update(dt)
		click.undraw()																		#update the textbox
		click.draw(win)
		if i % 10:
			win.update()
			time.sleep(0.01)
		if win.checkMouse() != None:														#if the user clicks the mouse (wants to try again)
			playsound("click.mp3", False)													#play the click sound effect
			win.close()																		#close the losescreen window
			startscreen()																	#call the start screen function - bring the user back to the start screen

"""the main game function - user scores points by bouncing the ball off the block and colliding with the snowmen objects and loses points by colliding with the hot chocolate objects"""
def main():
	win = gr.GraphWin( 'game', 700, 700, False )											#create a GraphWin
	background = Image(Point(230,245), "main.png")											#set the background image to the snow scene
	background.draw(win)
	score = 0		
	dt = 0.02
	frame = 0
	if frame%10 == 0:
			win.update()																	#initialize the score to 0
	
	scoretext = gr.Text( gr.Point( 50, 30 ), ("score:",score) )								#create the score textbox
	scoretext.setSize(20)
	scoretext.setTextColor("blue")
	scoretext.setStyle('bold')
	scoretext.draw(win)
	
	nametext = gr.Text(gr.Point(350,30), ("Player:",answer))								#create the player name textbox using the command line answer
	nametext.setSize(20)
	nametext.setTextColor("blue")
	nametext.setStyle('bold')
	nametext.draw(win)

	shapes = buildWall(win)																	#call buildWall, storing the return list in a variable
	for i in shapes:																		#loop over the shapes list and have each Thing call its draw method
		i.draw()	
	
	ball = pho.Ball(win)																	#create the main ball
	ball.setPosition( 50, 50 )
	ball.setVelocity( 15, -40 )
	ball.setAcceleration( 0,1 )
	ball.setElasticity(2)
	ball.setColor((255,255,255))
	ball.setMass(40)
	ball.draw()
	
	sled = pho.Block(win)																	#create the user-controlled sled for the ball to bounce off
	sled.setHeight(1.5)
	sled.setWidth(20)
	sled.setPosition(50,10)
	sled.setColor((0,0,250))
	sled.setElasticity(1)
	sled.draw()
	
	snowman1 = pho.Snowman(win)																#create the snowman objects
	snowman1.setPosition(18, 90)										
	snowman1.setVelocity(0,-20)
	snowman1.setAcceleration(0,-1)				
	snowman1.update(.01)							
	snowman1.draw()													
	snowman2 = pho.Snowman(win)						
	snowman2.setPosition(27,100)				
	snowman2.setVelocity(0,-20)
	snowman2.setAcceleration(0,-1)								
	snowman2.update(.01)											
	snowman2.draw()
	snowman3 = pho.Snowman(win)											
	snowman3.setPosition(36, 110)											
	snowman3.setVelocity(0,-20)
	snowman3.setAcceleration(0,-1)				
	snowman3.update(.01)							
	snowman3.draw()													
	snowman4 = pho.Snowman(win)						
	snowman4.setPosition(45,130)					
	snowman4.setVelocity(0,-20)
	snowman4.setAcceleration(0,-1)								
	snowman4.update(.01)											
	snowman4.draw()
	snowman5 = pho.Snowman(win)									
	snowman5.setPosition(54, 150)								
	snowman5.setVelocity(0,-20)
	snowman5.setAcceleration(0,-1)				
	snowman5.update(.01)							
	snowman5.draw()													
	
	hc1 = pho.Hotchocolate(win)																	#create the hot chocolate objects
	hc1.setPosition(10, 300)				
	hc1.setVelocity(0,-20)
	hc1.setAcceleration(0,-1)	
	hc1.setWidth(1)
	hc1.setHeight(1)		
	hc1.update(.01)					
	hc1.draw()
	hc2 = pho.Hotchocolate(win)														
	hc2.setPosition(50,320)	
	hc2.setVelocity(0,-20)
	hc2.setAcceleration(0,-1)
	hc2.setWidth(1)
	hc2.setHeight(1)						
	hc2.update(.01)					
	hc2.draw()
	hc3 = pho.Hotchocolate(win)														
	hc3.setPosition(100, 350)					
	hc3.setVelocity(0,-20)
	hc3.setAcceleration(0,-1)	
	hc3.setWidth(1)
	hc3.setHeight(1)					
	hc3.update(.01)					
	hc3.draw()
	
	snowmen = [snowman1, snowman2, snowman3, snowman4, snowman5]							#put the snowman objects into a list
	hotchocolate = [hc1, hc2, hc3]															#put the hot chocolate objects into a list
	
	while True:
		collided = False
		time.sleep( 0.033 )											
		key = win.checkKey()
		if win.checkMouse():																#if the user clicked the mouse, exit the window
			playsound("click.mp3", False)													#play the click sound effect
			break	
		
		#USER KEY CONTROLS
		if key == 'Left':																	#if the user clicked the left arrow button
			sled.moveLeft()																	#move the sled to the left
		if key == 'Right':																	#if the user clicked the right arrow button
			sled.moveRight()				   												#move the sled to the right
		if key == 'Up':																		#if the user clicked the up arrow button
			sled.moveUp()																	#move the sled up
		if key == 'Down':																	#if the user clicked the down arrow button
			sled.moveDown()																	#move the sled down
		for i in snowmen:
			i.update(0.033)		
		for i in hotchocolate:
			i.update(0.033) 																		
		
		sx = [5,14,22,30,38,46,54.5,65]														#a list of possible x coordinates for the snowmen
		hx = [20,40,60,80,100,120]															#a list of possible x coordinates for the hot chocolates
		
		for i in snowmen:
			if i.getPosition()[1] < 0:														#if a snowman is outside the window
				i.setPosition(random.choice(sx), random.choice(range(90,150)))				#reposition the snowman
				i.update(.01)
				if not i.getDrawn():
					i.draw()
		
		for i in hotchocolate:
			if i.getPosition()[1] < -50:													#if a hot chocolate is outside the window
				i.undraw()
				i.setPosition(random.choice(hx),random.randint(300,350))					#reposition the hot chocolate
				i.draw()
				i.setWidth(1)
				i.setHeight(1)	
				i.update(.01)	
		
		if ball.getPosition()[0] > win.getWidth() or ball.getPosition()[1] < 0:				#if the ball is outside the window
			ball.setPosition(25, 25)														#reposition the ball to the center of the window
			ball.setVelocity(20,20)
			ball.setAcceleration(0,0)
			ball.update(.01)
		
		collided = False																	#the ball has not collided with anything
		
		for i in shapes:																	#if the ball collides with a wall
			if collision.collision(ball, i, .01) == True:									#bounce off the wall
				collided = True
		if collision.collision(ball, sled, .01) == True:									#if the ball collides with the sled
			collided = True																	#bounce off the sled
			playsound("bounce.mp3", False)													#play the bounce sound effect
		
		collided = False																	#the ball has not collided with anything
		collidedS = False																	#the ball has not collided with a snowman
		
		for i in snowmen:																	
			if collision.collision(ball, i, .01) == True:									#if the ball collides with a snowman
				collidedS = True															#the ball has collided with a snowman
				score = score+1																#update the score and score textbox
				scoretext.undraw()
				scoretext = gr.Text( gr.Point( 50, 30 ), ("score:",score) )
				scoretext.setSize(15)
				scoretext.setTextColor("blue")
				scoretext.setStyle('bold')
				scoretext.draw(win)
				if collidedS == True:														#if the ball/snowman collision happened
					print("*snowman* +1")													#print the score update in the terminal
					i.undraw()
					playsound("gain.mp3", False)											#play the gain point sound effect
					ball.setRadius(ball.radius+.5)											#increase the ball's radius by .5
					ball.setMass(ball.mass+10)
					time.sleep(0.5)
					i.setPosition(random.choice(sx),90)										#reposition the snowman
					i.update(.01)
					if not i.getDrawn():
						i.draw()															#redraw the snowman
						i.setVelocity(0,-20)												#reset the snowman's speed
		
		collided = False																	#the ball has not collided with anything
		collidedH = False																	#the ball has not collided with a hot chocolate
		
		for h in hotchocolate:																
			if collision.collision(ball, h, .01) == True:									#if the ball collides with a hot chocolate
				collidedH = True
				score = score-1																#update the score and score textbox
				scoretext.undraw()
				scoretext = gr.Text( gr.Point( 50, 30 ), ("score:",score) )
				scoretext.setSize(15)
				scoretext.setTextColor("blue")
				scoretext.setStyle('bold')
				scoretext.draw(win)		
				print("*hot chocolate* -1")													#print the score update in the terminal
				if collidedH == True:
					h.undraw()
					playsound("lose.mp3", False)											#play the lose point sound effect
					ball.setRadius(ball.radius-.5)											#decrease the ball's radius by .5
					time.sleep(0.05)
					h.setPosition(random.choice(hx),random.randint(300,350))				#reposition the hot chocolate
					h.setWidth(1)
					h.setHeight(1)		
					h.update(.01)
					if not h.getDrawn():
						h.draw()															#redraw the hot chocolate
						h.setVelocity(0,-20)												#reset the hot chocolate's speed
		
		if (ball.radius == 0 ) or (score < 0):												#if the radius of the ball reaches 0 (snowball melts) or the score is less than 0
			time.sleep(0.05)
			win.close()																		#close the current game window
			losescreen()																	#display the lose screen
		
		if score>9:																			#if the user scores 10 points
			time.sleep(0.05)
			win.close()																		#close the current game window
			winscreen()																		#display the winscreen
			
		if collided == False:
			ball.update(dt)
			
		frame = frame + 1
		win.update()

if __name__ == "__main__":
	startscreen()
