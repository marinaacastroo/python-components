
#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class HumidifierEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(HumidifierEmulatorTask, self).__init__(
			name = ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
			typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE,
			simpleName = "HUMIDIFIER"
		)

		enableEmulation = ConfigUtil().getBoolean(
			ConfigConst.CONSTRAINED_DEVICE,
			ConfigConst.ENABLE_EMULATOR_KEY
		)

		self.sh = SenseHAT(emulate = enableEmulation)
		self._simpleName = self.getSimpleName() if self.getSimpleName() else "UNKNOWN"

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		if val is None:  # Evita que sea None
			val = ConfigConst.DEFAULT_VAL
		
		if self.sh.screen:
			msg = f"{self.getSimpleName()} ON: {val}C"
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1

		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		name = self.getSimpleName()
		if name is None:
			name = "HumidifierEmulatorTask"

		msg = f"{name} OFF"
		
		if self.sh.screen:
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1
