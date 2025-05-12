#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData

import aiocoap
from aiocoap import Code
from aiocoap.resource import ObservableResource

class GetTelemetryResourceHandler(ObservableResource, ITelemetryDataListener):
	def __init__(self):
		super().__init__()

		self.pollCycles = \
			ConfigUtil().getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, \
				key = ConfigConst.POLL_CYCLES_KEY, \
				defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)

		self.dataUtil = DataUtil()
		self.sensorData = None

		# for testing
		self.payload = "GetSensorData"

	async def render_get(self, request):
		responseCode = Code.CONTENT # TODO: change to appropriate value

		if not self.sensorData:
			self.sensorData = SensorData()

		jsonData = self.dataUtil.sensorDataToJson(self.sensorData)

		return aiocoap.Message(code = responseCode, payload = jsonData.encode('ascii'))
	
	def onSensorDataUpdate(self, data: SensorData = None) -> bool:
		pass
	