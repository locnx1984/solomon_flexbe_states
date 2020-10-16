#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger

from flexbe_core.proxy.proxy_service_caller import ProxyServiceCaller

from sensor_msgs.msg import Image
from vision_msgs.msg import Detection3D, Detection3DArray, ObjectHypothesisWithPose
from solomon_msgs.srv import VisionDetect,VisionDetectRequest
from std_msgs.msg import Empty as Empty_msg
from std_srvs.srv import Empty
'''
Created on 10/15/2020

@author: Loc Nguyen
'''
class GetDetectedObjectState(EventState):
	'''
	Get detected objects from vision system.

	#> camera_img 	Image 	The current color image of the left camera.

	<= done 				Image data is available.

	'''

	def __init__(self):
		'''Constructor'''
		super(GetDetectedObjectState, self).__init__(outcomes = ['done','failed'],
														output_keys = ['detected_objects'])
		rospy.wait_for_service('/detect_object')
		self.detect_proxy = rospy.ServiceProxy('/detect_object', VisionDetect)
	 	self._service_topic = '/detect_object'
		#self._srv = ProxyServiceCaller({self._service_topic: VisionDetect})

		self._srv_result = None
		self._failed = False
		self._done = False

	def execute(self, userdata): 

		

		Logger.loginfo("execute: detect objects!")
		if self._failed or self._srv_result is None:
			return 'failed'
		return 'done' 

	def on_enter(self, userdata):
		
		self._failed = False
		self._done = False

		try:
			Logger.loginfo("on_enter: detect objects!")

			self._srv_result = self.detect_proxy()
			rospy.sleep(0.01)
			Logger.loginfo('result=%s'%self._srv_result)
			current_objects = self._srv_result.result.detections  
			userdata.detected_objects = current_objects 
			self._done = True

			#PROXY CALLER
			# srv_request =VisionDetectRequest() 
			
			# _srv_result = self._srv.call( self._service_topic,srv_request)

			# current_objects = _srv_result.result.detections  
			# Logger.loginfo('Total detected objects:%d' %len(current_objects))
			# for i in range(len(current_objects)):
			# 	x=current_objects[i].results[0].pose.pose.position.x  
			# 	y=current_objects[i].results[0].pose.pose.position.y 
			# 	z=current_objects[i].results[0].pose.pose.position.z 
			# 	Logger.loginfo('object %d is at XYZ(%f,%f,%f)'%(i+1,x,y,z))

			# userdata.detected_objects = current_objects 
			# self._done = True
		except Exception as e:
			Logger.logwarn('Failed to send service call:\n%s' % str(e))
			self._failed = True
		
 
		