###########################
# Sample Node for RACECAR #
# Brian Plancher          #
# 7/12/17                 #
###########################

#!/usr/bin/python

# all of your imports go here
import rospy
#from std_msgs.msg import Bool
#from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped

###########################
# this class is your node #
###########################
class DepthNode:
   
   # constructor of the class to create it and set up all global things and subscribers and publishers
   def __init__(self):
    
      # subscribe to the laser data, teleop commands and whatever else you want here
      #rospy.Subscriber("/scan", LaserScan, self.callback)
      rospy.Subscriber("/vesc/low_level/ackermann_cmd_mux/input/teleop", AckermannDriveStamped, self.callback)
      
      # advertise that we'll publish on the TBD topic for notifications
      self.pubHandle = rospy.Publisher("TBD", AckermannDriveStamped, queue_size = 1)
      # and all other puublishers
        
      # global variables / parameters
      #self.global_var = 0.5
      
      # example ackermann msg
      msg = AckermannDriveStamped()
      msg.drive.speed = 1.2
      msg.drive.steering_angle = 0.2
      msg.header.stamp = rospy.Time.now()
      self.pub_msg = msg
	
   # Callback for laser message
   
   def callback(self, drive_msg):
      drive_msg.speed = 1.0
      drive_msg.steering_angle = 0.2
      self.pubHandle.publish(drive_msg)
      '''
      # DO STUFF HERE
      foo = bar * LaserScan_msg.ranges[0] # how to get a value out of LaserScan_msg and use it
      baz = self.global_var # how to use a global variable
      self.pub_msg.speed = baz # how to use a global variable part 2
      self.method_a() # how to call method_a
   
   # example helper method
   def method_a(self)
      #DO STUFF HERE
      self.pubHandle.publish(self.pub_msg) # how to publish
      
   # other methods here until done
   '''

# incude this to make sure the file connects to the roscore
if __name__ == '__main__':
    rospy.init_node("NodeName")
    node = DepthNode()
    rospy.spin()

