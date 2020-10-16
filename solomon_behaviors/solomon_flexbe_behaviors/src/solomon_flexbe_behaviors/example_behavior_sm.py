#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_state import LogState
from flexbe_states.wait_state import WaitState
from solomon_flexbe_states.get_2D_image_state import Get2DImageState
from solomon_flexbe_states.clear_octomap import ClearOctomapState
from solomon_flexbe_states.get_detected_object_state import GetDetectedObjectState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Aug 21 2015
@author: Philipp Schillinger
'''
class ExampleBehaviorSM(Behavior):
	'''
	This is a simple example for a behavior.
	'''


	def __init__(self):
		super(ExampleBehaviorSM, self).__init__()
		self.name = 'Example Behavior'

		# parameters of this behavior
		self.add_parameter('waiting_time', 3)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		log_msg = "Hello World Solomon!"
		# x:786 y:398
		_state_machine = OperatableStateMachine(outcomes=['finished'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:52 y:78
			OperatableStateMachine.add('Print_Message',
										LogState(text=log_msg, severity=Logger.REPORT_HINT),
										transitions={'done': 'Capture 2D Image'},
										autonomy={'done': Autonomy.Off})

			# x:56 y:193
			OperatableStateMachine.add('Wait_After_Logging',
										WaitState(wait_time=self.waiting_time),
										transitions={'done': 'Clear Octomap'},
										autonomy={'done': Autonomy.Off})

			# x:237 y:144
			OperatableStateMachine.add('Capture 2D Image',
										Get2DImageState(),
										transitions={'done': 'Wait_After_Logging'},
										autonomy={'done': Autonomy.Off},
										remapping={'camera_img': 'camera_img'})

			# x:244 y:239
			OperatableStateMachine.add('Clear Octomap',
										ClearOctomapState(),
										transitions={'done': 'Wait_2s', 'failed': 'Wait_2s'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:72 y:279
			OperatableStateMachine.add('Wait_2s',
										WaitState(wait_time=2),
										transitions={'done': 'detect'},
										autonomy={'done': Autonomy.Off})

			# x:252 y:361
			OperatableStateMachine.add('detect',
										GetDetectedObjectState(),
										transitions={'done': 'finished', 'failed': 'finished'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'detected_objects': 'detected_objects'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
