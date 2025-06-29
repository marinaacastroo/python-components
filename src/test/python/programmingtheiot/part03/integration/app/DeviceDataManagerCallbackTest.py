#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import unittest

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.ActuatorData import ActuatorData

class DeviceDataManagerCallbackTest(unittest.TestCase):
	"""
	Test DeviceDataManager.handleActuatorCommandMessage callback logic.
	"""
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing DeviceDataManager ActuatorData callback...")

	def setUp(self):
		self.ddMgr = DeviceDataManager()

	def tearDown(self):
		self.ddMgr = None

	def testActuatorDataCallback(self):
		ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setStateData("This is a test.")
		ad.setValue(52)
		logging.info(f"Sending ActuatorData command: {ad}")
		response = self.ddMgr.handleActuatorCommandMessage(ad)
		logging.info(f"Received response: {response}")
		self.assertTrue(response is None or isinstance(response, ActuatorData))

if __name__ == "__main__":
	unittest.main()
