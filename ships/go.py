#! /usr/bin/env python

import rospy
import pyfirmata as pf
from geometry_msgs.msg import Twist

ard = pf.Arduino('/dev/ttyACM0')
motorL = ard.get_pin('d:10:s')
motorR = ard.get_pin('d:9:s')

ard.pass_time(1)
motorL.write(1500)
motorR.write(1500)
print("ready")

def callback(msg):
    rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
    
    if msg.linear.x == 0:
        if msg.angular.z == 0:
            print("stop")
            motorL.write(1500)
            motorR.write(1500)

        elif msg.angular.z > 0:
            print("turn left")
            motorL.write(1400)
            motorR.write(1400)

        elif msg.angular.z < 0:
            print("turn right")
            motorL.write(1600)
            motorR.write(1600)

    elif msg.linear.x < 0:
        if msg.angular.z == 0:
            print("go back")
            motorL.write(1350)
            motorR.write(1650)

        elif msg.angular.z > 0:
            print("back left")
            motorL.write(1450)
            motorR.write(1650)

        elif msg.angular.z < 0:
            print("back right")
            motorL.write(1350)
            motorR.write(1550)

    elif msg.linear.x > 0:
        if msg.angular.z < 0.1 and msg.angular.z > -0.1 :
            print("go straight")
            motorL.write(1530)
            motorR.write(1470)

        elif msg.angular.z > 0.1 and msg.angular.z < 0.5 :
            print("go left")
            motorL.write(1450)
            motorR.write(1350)

        elif msg.angular.z > 0.5 :
            print("go left")
            motorL.write(1350)
            motorR.write(1300)

        elif msg.angular.z < -0.1 and msg.angular.z > -0.5 :
            print("go right")
            motorL.write(1650)
            motorR.write(1550)
            
        elif msg.angular.z < -0.5 :
            print("go right")
            motorL.write(1700)
            motorR.write(1650)

    else:
        print("Error. Can not moving.")
        motorL.write(1500)
        motorR.write(1500)

def listener():
    print("Initialize ROS node.")
    rospy.init_node('myship_go')
    rospy.Subscriber('/cmd_vel', Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()