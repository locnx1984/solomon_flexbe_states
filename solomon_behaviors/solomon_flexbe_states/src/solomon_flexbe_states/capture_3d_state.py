#!/usr/bin/env python

import rospy
from flexbe_core import EventState, Logger 
from flexbe_core.proxy.proxy_service_caller import ProxyServiceCaller
from std_srvs.srv import Empty 

'''
Created on 10/15/2020

@author: Loc Nguyen
'''
class Capture3DState(EventState):
	'''
	Clear Octomap of planning scene.

	#> input 				Nothing

	<= done 				Octomap is cleared.

	'''

	def __init__(self):
		'''Constructor'''
		super(Capture3DState, self).__init__(outcomes = ['done','failed']) 
		self._srv_topic = '/clear_octomap'
		self.clear_octomap = rospy.ServiceProxy('/clear_octomap', Empty)  

	def execute(self, userdata):
		return 'done'

	def on_enter(self, userdata):  
		try:
			self.clear_octomap()
			Logger.loginfo("Capture 3D data...")
			# for i in range(3):
			# 	self.clear_octomap() 
			# 	Logger.loginfo("clear octomap %d" %(i+1))
		except rospy.ServiceException, e:
			Logger.loginfo("Service call failed: %s"%e)
		except:
			Logger.loginfo("service not available...")
			return 'failed' 