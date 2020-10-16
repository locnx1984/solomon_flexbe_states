#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

from flexbe_core.proxy import ProxySubscriberCached

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
'''
Created on 10/15/2020

@author: Loc Nguyen
'''
class Get2DImageState(EventState):
	'''
	Grabs the most recent camera image.

	#> camera_img 	Image 	The current color image of the left camera.

	<= done 				Image data is available.

	'''

	def __init__(self):
		'''Constructor'''
		super(Get2DImageState, self).__init__(outcomes = ['done'],
														output_keys = ['camera_img'])
		#self.bridge = CvBridge()
		self._img_topic = "/camera/color/image_raw"
		self._sub = ProxySubscriberCached({self._img_topic: Image})


	def execute(self, userdata):
		Logger.loginfo("excexute!")
		if self._sub.has_msg(self._img_topic):
			img2D = self._sub.get_last_msg(self._img_topic)

			# try: 
			# 	image_buff = CvBridge().imgmsg_to_cv2(img2D, "bgr8") 
			# 	cv2.namedWindow("window")
      		# 	cv2.imshow("window", image_buff) 
			 

			Logger.loginfo("Get 2D image! width %d height %d" %(img2D.width,img2D.height))			
			userdata.camera_img=img2D
			return 'done'


	def on_enter(self, userdata):
		Logger.loginfo("enter!")
		pass