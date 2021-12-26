# Template by Bruce A Maxwell
# Fall 2018
# CS 152 Project 11
#
# Make an Asteroids-like ship move around
#
# slightly modified by Eric Aaron, Fall 2018, Spring 2019
#
# import useful packages
import math
import time
import graphicsPlus as gr
import physics_objects as pho

# make a ship object, treat it as a ball
# but it needs to be able to rotate
# should probably have a parent rotator class that does most of this for you
class Ship(pho.Thing):
    def __init__(self, win, x0=0, y0=0, mass=1, radius=3):
        pho.Thing.__init__(self, win, "ball")
        # could use pho.Thing.__init__(self, win, "ball", mass=mass, radius=radius) instead,
        # if Thing.__init__ has those defaults
        self.setMass(mass)
        self.radius = radius
        self.setPosition(x0, y0)

        # anchor point is by default the center of the ship/circle so we don't need it
        self.angle = 0.
        self.dangle = 0.

        # visualization properties
        # This is a two-part visualization
        # the ship is a triangle
        self.bodypts = [ (radius, 0),
                         (- radius*0.5,   1.732*radius*0.5),
                         (- radius*0.5, - 1.732*radius*0.5) ]
        # the exhaust is another triangle
        self.flamepts = [ (- radius*0.5,   0.5*radius),
                          (- radius*0.5, - 0.5*radius),
                          (- radius*1.732, 0) ]

        self.scale = 10.
        self.vis = []
        self.drawn = False
        self.refresh() # call refresh to set up the vis list properly

        # these are for handling the flicker of the exhaust
        self.flickertime = 6
        self.flicker = False
        self.countdown = 0

    #########
    # these functions are identical to the rotating block
    # a smart coder would make a parent rotator class

    # draw the object into the window
    def refresh(self):
        drawn = self.drawn
        if drawn:
            self.undraw()
            
        self.render()
        
        if drawn:
            self.draw()

    # get and set the angle of the object
    # these are unique to rotators
    def getAngle(self):
        return self.angle

    # setAngle has to update the visualization
    def setAngle(self, a):
        self.angle = a
        self.refresh()

    # get and set rotational velocity
    def setRotVelocity(self, rv):
        self.dangle = rv # degrees per second

    def getRotVelocity(self):
        return self.dangle

    def getRadius(self):
        return self.radius

    def setRadius(self, r):
        self.radius = r
        self.refresh()

    # incrementally rotate by da (in degrees)
    # has to update the visualization
    def rotate(self, da):
        self.angle += da
        self.refresh()

    # special ship methods
    def setFlickerOn(self, countdown = 50):
        self.flicker = True
        self.countdown = countdown

    def setFlickerOff(self):
        self.countdown = 0
        self.flicker = False
        
    # simplified render function since the ship always rotates around its center
    def render(self):

        # get the cos and sin of the current orientation
        theta = math.pi * self.angle / 180.
        cth = math.cos(theta)
        sth = math.sin(theta)

        # rotate each point around the object's center
        pts = []
        for vertex in self.bodypts + self.flamepts:
            # move the object's center to 0, 0, which it is already in model coordinates
            xt = vertex[0]
            yt = vertex[1]

            # rotate the vertex by theta around the Z axis
            xtt = cth*xt - sth*yt
            ytt = sth*xt + cth*yt

            # move the object's center back to its original location
            pos = self.getPosition()
            xf = xtt + pos[0]
            yf = ytt + pos[1]

            # create a point with the screen space coordinates
            pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

        # make the two objects
        self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
        self.vis[0].setFill("dark blue")
        self.vis[0].setOutline("dark red")
        self.vis[1].setOutline("yellow")

    # update the various state variables
    # add a unique flicker touch
    def update(self, dt):
        # update the angle based on rotational velocity
        da = self.dangle * dt
        if da != 0.0: # don't bother updating if we don't have to
            self.rotate( da )

        # flicker the flames
        # this should be a field of the object
        if self.flicker and self.countdown > 0:
            if self.countdown % self.flickertime < self.flickertime/2:
                self.vis[1].setFill( 'yellow' )
            else:
                self.vis[1].setFill( 'orange' )
            self.countdown -= 1
        else:
            self.vis[1].setFill( 'white' )

        # call the parent update for the rest of it
        pho.Thing.update(self, dt)

def main():
    # make a window
    win = gr.GraphWin('Ship', 500, 500, False)

    # make ship, draw it, wait for a mouse click
    ship = Ship(win, 25, 25)
    ship.draw()
    
    dt = 0.01
    frame = 0
    ship.setRotVelocity(20)
    
    gamma = 10
    delta = 1
    
    winWidth = 50
    winHeight = 50
    
    while True:
        key = win.checkKey()
        if key == "q":
            break
            
        # assign to moveit the value False
        moveit = False
        # assign to p the ship's current position.  You might want to cast it to a list.
        p = ship.getPosition()[:]

        # if the x coordinate is less than 0
        if p[0] < 0:
            # add winWidth to the x coordinate
            p[0] = p[0] + winWidth
            # assign to moveit the value True
            moveit = True
        # elif the x coordinate is greater than winWidth
        elif p[0] > winWidth:
            # subtract winWidth from the x coordinate
            p[0] = p[0] - winWidth
            # assign to moveit the value True
            moveit = True
        # if the y coordinate is less than 0
        if p[1] < 0:
            # add winHeight to the y coordinate
            p[1] = p[1] + winHeight
            # assign to moveit the value True
            moveit = True
        # elif the y coordinate is greater than winHeight
        elif p[1] > winHeight:
            # subtract winHeight from the y coordinate
            p[1] = p[1] - winHeight
            # assign to moveit the value True
            moveit = True
    
        # if moveit:
        if moveit:
            # set the ship's position to p
            ship.setPosition(p[0], p[1])
    
        ship.update(dt)
        frame = frame + 1
        
        if frame%10 == 0:
            win.update()
        
        # if the user hits the 'Left' key
        if key == "Left":
            # set the rotational velocity to the old rotational velocity plus gamma
            ship.setRotVelocity(ship.dangle+gamma)
            # call the ship's setFlickerOn method with no arguments
            ship.setFlickerOn()
        # elif the user hits the 'Right' key
        elif key == "Right":
            # set the rotational velocity to the old rotational veloity minus gamma
            ship.setRotVelocity(ship.dangle-gamma)
            # call the ship's setFlickerOn method with no arguments
            ship.setFlickerOn()
            
        # elif the user types 'space'
        elif key == "space":
            # assign to a the ship's current angle (getAngle)
            a = ship.getAngle()
            # assign to theta the result of multiplying a by math.pi and dividing by 180
            theta = (a*math.pi)/180
            # assign to v the ship's current velocity (getVelocity)
            v = ship.getVelocity()
            vx = ship.getVelocity()[0]
            vy = ship.getVelocity()[1]
            vnewx = vx + math.cos(theta) * delta
            vnewy = vy + math.sin(theta) * delta
            # set the ship's velocity to it's new values
            ship.setVelocity(vnewx, vnewy)
            #   The new X velocity is v_new_x = v_old_x + cos(theta) * delta
            #   The new Y velocity is v_new_y = v_old_y + sin(theta) * delta
            # call the ship's setFlickerOn method with no arguments
            ship.setFlickerOn()

    # all done
    win.close()

if __name__ == "__main__":
    main()