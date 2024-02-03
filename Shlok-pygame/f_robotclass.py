class Robot:
    def __init__(self, x, y): # constructor 
        
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    #def currPosition(self):
      # print(f"Robot's position (x,y): ({self.x}, {self.y})")

# Create an instance of the Robot class
my_robot = Robot(0, 0)

# Move the robot
my_robot.move(2, 3)
#my_robot.move(8, 9)
#my_robot.currPosition()

# Print the robot's current position
print(f"Robot's position (x,y): ({my_robot.x}, {my_robot.y})")
