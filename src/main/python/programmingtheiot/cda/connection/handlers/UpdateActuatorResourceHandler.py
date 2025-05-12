#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData

import aiocoap

from aiocoap import Code
from aiocoap.resource import Resource

class UpdateActuatorResourceHandler():
	"""
	Standard resource that will handle an incoming actuation command,
	and return the command response.
	
	NOTE: Your implementation will likely need to extend from the selected
	CoAP library's resource base class.
	
	"""

	def __init__(self, dataMsgListener: IDataMessageListener = None):
		super().__init__()
		self.dataMsgListener = dataMsgListener
		self.dataUtil = DataUtil()

	async def render_put(self, request):
		try:
			logging.info("Received PUT request: %s", request.payload.decode('utf-8'))

			if not request.payload:
				logging.warning("PUT request payload is empty.")
				return aiocoap.Message(code=Code.BAD_REQUEST)

		
			actuatorCmdData = self.dataUtil.jsonToActuatorData(request.payload)

			return self._createResponse(actuatorCmdData)

		except Exception as e:
			logging.warning("Failed to validate and convert actuation command: %s", str(e))

		return aiocoap.Message(code=Code.NOT_ACCEPTABLE)
	
	def _createResponse(self, data: ActuatorData = None):
		responseCode = Code.CHANGED

		actuatorResponseData = self.dataMsgListener.handleActuatorCommandMessage(data)

		if not actuatorResponseData:
			logging.warning("No response from actuator handler. Creating default response.")
			actuatorResponseData = ActuatorData()
			actuatorResponseData.updateData(data)
			actuatorResponseData.setAsResponse()
			actuatorResponseData.setStatusCode(-1)

		jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
		return aiocoap.Message(code=responseCode, payload=jsonData.encode('ascii'))