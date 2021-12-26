# Tamsin Rogers
# November 13, 2019
# Updated December 8, 2019
# CS 152 
# Project 11: Something Interactive

import graphicsPlus as gr
import random
import math
from graphicsPlus import *

#the parent class for simulated objects
class Thing:
	"""This function initializes the attributes of objects in the Thing class.	Win and the_type are the required parameters."""
	def __init__(self, win, the_type):
		self.win = win				#the GraphWin window for drawing
		self.the_type = "type"		#the type of thing being created
		self.mass = 0				#A scalar value indicating the mass of the object.
		self.position = [0,0]		#A 2-element list indicating the current position of the object.
		self.velocity = [0,0]		#A 2-element list indicating the current velocity of the object.
		self.acceleration = [0,0]	#A 2-element list indicating acceleration acting on the object.
		self.elasticity = .5		#The amount of energy retained after a collision.
		self.scale = 10				#The scale factor between the simulation space and pixels. Default to 10.
		self.vis = []				#An empty list that will hold Zelle graphics.
		self.color = (0,0,0)		#An (r, g, b) tuple. A good default value is black (0, 0, 0).
		self.drawn = False			#A boolean indicating if the shape has been drawn, initially False.
	#GET METHODS
	"""This function takes the argument self and returns the type of the object as a string."""
	def getType(self):
		return "thing"
	"""This function takes the argument self and returns the mass of the object."""
	def getMass(self):
		return self.mass
	"""This function takes the argument self and returns a 2 element tuple with the x,y position of the ball object."""
	def getPosition(self):			
		return self.position[:]
	"""This function takes the argument self and returns a 2 element tuple with the x and y velocities."""
	def getVelocity(self):			
		return self.velocity[:]
	"""This function takes the argument self and returns a 2 element tuple with the x and y accelerations.""" 
	def getAcceleration(self):		
		return self.acceleration[:]
	"""This function takes the argument self and returns the elasticity value, or the amount of energy retained after a collision, of the object."""
	def getElasticity(self):
		return self.elasticity
	"""This function takes the argument self and returns the scale factor between the simulation space and pixels."""
	def getScale(self):
		return self.scale
	"""This function takes the argument self and returns an (r, g, b) tuple that sets the color of the object."""
	def getColor(self):
		return self.color
	"""This function takes the argument self and returns a boolean indicating if the referenced shape has been drawn."""
	def getDrawn(self):
		return self.drawn
	#DRAW/UNDRAW METHODS
	"""This function takes the argument self and loops through the vis list to draw the object in the window."""
	def draw(self):
		for i in self.vis:
			i.draw(self.win)
		self.drawn = True
	"""This function takes the argument self and loops through the vis list to undraw the object in the window."""
	def undraw(self):
		for i in self.vis:
			i.undraw()
		self.drawn = False
	#SET METHODS
	"""This function takes self and m as arguments and sets the mass of the object."""
	def setMass(self, m):
		self.mass = m
	"""This function sets the x,y velocity of the thing object.	  The vx and vy variables 
	are the new x,y values.	 The x coordinate of v is assigned to the x coordinate in self.velocity, 
	and the y coordinate of v is assigned to the y coordinate in self.velocity."""	   
	def setVelocity(self, vx, vy):		# vx and vy are the new x and y velocities
		self.velocity[0] = vx
		self.velocity[1] = vy
	"""This function sets the x,y acceleration of the thing object.	  The ax and ay variables 
	are the new x,y values.	 The x coordinate of a is assigned to the x coordinate in self.acceleration, 
	and the y coordinate of a is assigned to the y coordinate in self.acceleration."""	
	def setAcceleration(self, ax, ay):	# ax and ay are new x and y accelerations.
		self.acceleration[0] = ax
		self.acceleration[1] = ay
	"""This function sets the amount of energy retained by an object after a collision 
	(elasticity) to the variable e."""
	def setElasticity(self, e):
		self.elasticity = e
	"""This function sets the x,y position of the Thing object.	 This is done by calculating 
	the difference between the new position (px, py) and the current position (self.position[0], self.position[1]).	 
	These values are then set into dx, dy, and the ball's position fields are updated with 
	the new positions.	The setPosition function is finalized by multiplying dx by self.scale 
	and dy by -self.scale, and moving the vis list items by dx and dy within a for loop.'"""	   
	def setPosition(self, px, py):
		# BAM updated to be simpler
		dx = px - self.position[0]
		dy = py - self.position[1]
		self.position[0] = px			# assign to the x coordinate in self.pos the x coordinate of p
		self.position[1] = py			# assign to the y coordinate in self.pos the y coordinate of p

		dx = dx * self.scale
		dy = -dy * self.scale
		# c = self.vis[0].getCenter()
		# dx = (self.scale*px)-(c.getX())
		# dy = (self.win.getHeight()-(self.scale*py)-(c.getY()))
		for i in self.vis:
			i.move(dx, dy)
	"""This function sets the color field of the shape to c.  If c is not None, the function 
	loops over the self.vis list and sets the fill color of the referenced shape object to 
	the appropriate color using rgb values."""
	def setColor(self, c):
		self.color = c
		if c != None:
			for i in self.vis:
				thecolor = gr.color_rgb(self.color[0], self.color[1], self.color[2])
				i.setFill(thecolor)
	"""This function adjusts the position, velocity, and vis values of the thing object through 
	dependence on its current acceleration and force values.  It takes one argument (dt), 
	which is the time step that indicates how much time to run the simulation for."""
	def update(self, dt):
		# update the x position using x_new = x_old + x_vel*dt + 0.5*x_acc * dt*dt
		self.position[0] = self.position[0] + self.velocity[0]*dt + 0.5*self.acceleration[0] * dt*dt
		# update the y position using y_new = y_old + y_vel*dt + 0.5*y_acc * dt*dt 
		self.position[1] = self.position[1] + self.velocity[1]*dt + 0.5*self.acceleration[1] * dt*dt
		# assign to dx the change in the x position times the scale factor (self.scale)
		dx = (self.velocity[0]*dt + 0.5 * self.acceleration[0] * dt * dt)*self.scale
	   # assign to dy the negative of the change in the y position times the scale factor (self.scale)
		dy = -(self.velocity[1]*dt + 0.5 * self.acceleration[1] * dt * dt)*self.scale
		# for each item in self.vis
		for i in self.vis:
			# call the move method of the graphics object with dx and dy as arguments.
			i.move(dx, dy)
		# update the x velocity by adding the acceleration times dt to its old value
		self.velocity[0] = self.velocity[0]+(self.acceleration[0]*dt)
		# update the y velocity by adding the acceleration times dt to its old value
		self.velocity[1] = self.velocity[1]+(self.acceleration[1]*dt)
	
class Ball(Thing):
	"""This function initializes the attributes of objects in the Ball class, which are inherited from the Thing class."""
	def __init__(self, win, x0=0, y0=0, radius=2, color=(0,0,0), type = "ball"):
		Thing.__init__(self, win, "ball")
		self.win = win
		self.radius = radius
		self.position = [x0, y0]
		self.color = color
		self.refresh()
		self.setColor(self.color)
	def getType(self):
		return "ball"
	"""This function assigns drawn to the value of self.drawn.	Then, if the shape is draw, 
	it undraws it using self.undraw.  The function then defines the self.vis list of graphics 
	objects using the current position, radius, and window values, and if the object is drawn, 
	draws it."""
	def refresh(self):
		drawn = self.drawn
		if drawn:
			self.undraw()
		self.vis = [ gr.Circle( gr.Point(self.position[0]*self.scale, self.win.getHeight()-self.position[1]*self.scale), self.radius * self.scale ) ]
		self.setColor(self.color)
		if drawn:
			self.draw()
	"""This function returns the radius of the ball object."""
	def getRadius(self):
		return self.radius
	"""This function assigns r to the radius field and then calls self.refresh()."""
	def setRadius(self,r):
		self.radius = r
		self.refresh()
		
class Block(Thing):
	"""This function initializes the attributes of objects in the Block class, which are inherited from the Thing class."""
	def __init__ (self, win, x0=5, y0=5, width=150, height=2, color=(0,0,0), type = "block"):
		Thing.__init__(self, win, "block")
		self.win = win
		self.position = [x0,y0]		   
		self.color = color
		self.width = width
		self.height = height
		self.reshape()				#set up the vis list
		self.setColor((0,0,0))		#set the color
	def getType(self):
		return "block"
	"""This function undraws the block's graphics objects if they are drawn and defines the 
	self.vis list of graphics objects using the appropriate fields.	 It then draws the graphics 
	objects for block if they are drawn."""
	def reshape(self):
		# BAM need to use a local variable for this because self.undraw modifies self.drawn to False
		drawn = self.drawn
		if drawn:
			self.undraw()
		# BAM adjusted the Y value so the orientation is inverted
		self.vis = [gr.Rectangle(gr.Point((self.position[0]-self.width/2)*self.scale, self.win.getHeight() - (self.position[1]-self.height/2)*self.scale), gr.Point((self.position[0]+self.width/2)*self.scale, self.win.getHeight() - (self.position[1]+self.height/2)*self.scale))]
		if drawn:
			self.draw()
	def getPosition(self):
		return self.position[:] # BAM return a copy to avoid aliasing
	"""This function returns the width of the block object."""
	def getWidth(self):
		return self.width
	"""This function returns the height of the block object."""
	def getHeight(self):
		return self.height
	"""This function resets the width of the block object using the dx variable and the reshape function."""
	def setWidth(self, dx):
		self.width = dx
		self.reshape()
	"""This function resets the height of the block object using the dy variable and the reshape function."""
	def setHeight(self, dy):
		self.height = dy
		self.reshape()
	"""This function moves the block object in the left x direction."""		  
	def moveLeft(self):
		self.setPosition(self.position[0]-5, self.position[1])
	"""This function moves the block object in the right x direction."""
	def moveRight(self):
		self.setPosition(self.position[0]+5, self.position[1])
	"""This function moves the block object down in the y direction."""		  
	def moveDown(self):
		self.setPosition(self.position[0], self.position[1]-5)
	"""This function moves the block object up in the y direction."""		
	def moveUp(self):
		self.setPosition(self.position[0], self.position[1]+5)
			
class RotatingBlock(Thing):
	def __init__(self, win, x0=5, y0=5, width=1.5, height=1.5, Ax = None, Ay = None, color=(255,255,255)):
		Thing.__init__(self, win, "rotatingblock")
		self.win = win
		self.position = [x0,y0]			#The x0 and y0 values as a 2-element list. # BAM edited to be position
		self.anchor = [Ax, Ay]			#the Ax and Ay values as a 2-element list, if both are given, otherwise x0, y0
		if Ax != None and Ay != None:
			self.anchor = [Ax, Ay]
		else:
			self.anchor = [x0,y0]
		self.width = width
		self.height = height
		self.points = [ (-width/2, -height/2), (width/2, -height/2), (width/2, height/2), (-width/2, height/2)]
		self.angle = 0.0				#The current orientation of the line
		self.rvel = 0.0					#Rotational velocity (in degrees/s)
		self.drawn	= False				#A Boolean variable to indicate if the Line has been drawn
		self.setColor((255,255,255))
		self.refresh()
	def getType(self):
		return "rotatingblock"
	def refresh(self):
		drawn = self.drawn
		if drawn:
			self.undraw()
		self.render()
		if drawn:
			self.draw()
			self.setColor((255,255,255))
	"""This function returns the width of the block object."""
	def getWidth(self):
		return self.width
	"""This function returns the height of the block object."""
	def getHeight(self):
		return self.height
	"""This function resets the width of the block object using the dx variable and the reshape function."""
	def setWidth(self, dx):
		self.width = dx
		self.refresh()
	"""This function resets the height of the block object using the dy variable and the reshape function."""
	def setHeight(self, dy):
		self.height = dy
		self.refresh()
	def render(self):
		# assign to theta the result of converting self.angle from degrees to radians
		theta = self.angle*((math.pi)/180)
		# assign to cth the cosine of theta
		cth = math.cos(theta)
		# assign to sth the sine of theta
		sth = math.sin(theta)
		# assign to pts the empty list
		pts = []
		# for each vertex in self.points
		for v in self.points:
		  # (2 lines of code): assign to x and y the result of adding the vertex to self.pos and subtracting self.anchor
		  x = self.position[0] + v[0] - self.anchor[0] # BAM edited to be position
		  y = self.position[1] + v[1] - self.anchor[1] # BAM edited to be position
		  # assign to xt the calculation x * cos(Theta) - y * sin(Theta) using your precomputed cos/sin values above
		  xt = (x*cth - y*sth)
		  # assign to yt the calculation x * sin(Theta) + y * cos(Theta)
		  yt = (x*sth + y*cth)
		  # (2 lines of code): assign to x and y the result of adding xt and yt to self.anchor
		  x = (xt)+self.anchor[0]
		  y = (yt)+self.anchor[1]
		  # append to pts a Point object with coordinates (self.scale * x, self.win.getHeight() - self.scale*y)
		  pts.append(gr.Point(self.scale*x, self.win.getHeight() - self.scale*y))
		# assign to self.vis a list with a Zelle graphics Line object using the Point objects in pts
		self.vis = [gr.Polygon(pts[0], pts[1], pts[2], pts[3])]
	def getAngle(self):
		return self.angle
	def setAngle(self, a):
		self.angle = a
		self.refresh()
	def getAnchor(self):
		return self.anchor
	def setAnchor(self, x0, y0):
		self.anchor[0] = x0
		self.anchor[1] = y0
	def getRotVelocity(self):
		return self.rvel
	def setRotVelocity(self, r):
		self.rvel = r
	def rotate(self, r):
		self.angle = self.angle + r
		if self.drawn:
			self.vis[0].undraw()
			self.vis[0].draw(self.win)
		self.refresh()
	def update(self,dt):
		da = self.rvel*dt
		if da != 0:
			self.rotate(da)
		Thing.update(self, dt) # BAM this should always occur
	"""This function sets the color field of the shape to c.  If c is not None, the function 
	loops over the self.vis list and sets the fill color of the referenced shape object to 
	the appropriate color using rgb values."""
	def setColor(self, c):
		self.color = c
		if c != None:
			for i in self.vis:
				thecolor = gr.color_rgb(self.color[0], self.color[1], self.color[2])
				i.setFill(thecolor)
		
class Snowman(Thing):
	"""This function initializes the attributes of objects in the Newshape class, which are inherited from the Thing class."""
	def __init__(self, win, x0=4, y0=2, dx=4, dy=2, radius=2, color=((255,255,255)), type = "snowman"):
		Thing.__init__(self, win, "snowman")
		self.win = win
		self.radius = radius
		self.position = [x0, y0]
		self.color = color
		self.width = dx
		self.height = dy
		self.refresh()
		self.setColor(self.color)
	def getType(self):
		return "snowman"
	"""This function assigns drawn to the value of self.drawn.	Then, if the shape is draw, 
	it undraws it using self.undraw.  The function then defines the self.vis list of graphics 
	objects using the current position, radius, and window values, and if the object is drawn, 
	draws it."""
	def refresh(self):
		drawn = self.drawn
		if drawn:
			self.undraw()
		top = gr.Circle( gr.Point(self.position[0]*self.scale, self.win.getHeight()-self.position[1]*self.scale), self.radius * self.scale )
		middle = gr.Circle( gr.Point(self.position[0]*self.scale, self.win.getHeight()-(self.position[1]-2.6)*self.scale), (self.radius * self.scale)*1.5 )
		bottom = gr.Circle( gr.Point(self.position[0]*self.scale, self.win.getHeight()-(self.position[1]-5.414)*self.scale), (self.radius * self.scale)*2 )
		self.vis = [bottom, middle, top]
		if drawn:
			self.draw()
	"""This function returns the radius of the ball object."""
	def getRadius(self):
		return self.radius
	"""This function assigns r to the radius field and then calls self.refresh()."""
	def setRadius(self,r):
		self.radius = r
		self.refresh()
	"""This function takes the argument self and loops through the vis list to undraw the object in the window."""
	def undraw(self):
		for i in self.vis:
			i.undraw()
		self.drawn = False
		
class Hotchocolate(Thing):
	"""This function initializes the attributes of objects in the Hotchocolate class, which are inherited from the Thing class."""
	def __init__ (self, win, x0=5, y0=5, width=150, height=2, type = "block"):
		Thing.__init__(self, win, "hotchocolate")
		self.win = win
		self.position = [x0,y0]		   
		self.width = width
		self.height = height
		self.reshape()				#set up the vis list
	def getType(self):
		return "hotchocolate"
	"""This function undraws the block's graphics objects if they are drawn and defines the 
	self.vis list of graphics objects using the appropriate fields.	 It then draws the graphics 
	objects for block if they are drawn."""
	def reshape(self):
		# BAM need to use a local variable for this because self.undraw modifies self.drawn to False
		drawn = self.drawn
		if drawn:
			self.undraw()
		# BAM adjusted the Y value so the orientation is inverted
		self.vis = [Image(Point(230,245), "hc.png")]
		if drawn:
			self.draw()
	def getPosition(self):
		return self.position[:] # BAM return a copy to avoid aliasing
	"""This function returns the width of the block object."""
	def getWidth(self):
		return self.width
	"""This function returns the height of the block object."""
	def getHeight(self):
		return self.height
	"""This function resets the width of the block object using the dx variable and the reshape function."""
	def setWidth(self, dx):
		self.width = dx
		self.reshape()
	"""This function resets the height of the block object using the dy variable and the reshape function."""
	def setHeight(self, dy):
		self.height = dy
		self.reshape()