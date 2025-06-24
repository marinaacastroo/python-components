#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import socket
import traceback

from coapthon import defines
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon.utils import generate_random_token

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

class CoapClientConnector(IRequestResponseClient):
    """
    Shell representation of class for student implementation.
    
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.config = ConfigUtil()
        self.dataMsgListener = dataMsgListener
        self.enableConfirmedMsgs = False
        self.coapClient = None
        self.observeRequests = {}
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.HOST_KEY,
            ConfigConst.DEFAULT_HOST
        )
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.PORT_KEY,
            ConfigConst.DEFAULT_COAP_PORT
        )
        self.uriPath = "coap://" + self.host + ":" + str(self.port) + "/"
        logging.info('\tHost:Port: %s:%s', self.host, str(self.port))
        self.includeDebugLogDetail = True
        try:
            tmpHost = socket.gethostbyname(self.host)
            if tmpHost:
                self.host = tmpHost
                self._initClient()
            else:
                logging.error("Can't resolve host: " + self.host)
        except socket.gaierror:
            logging.info("Failed to resolve host: " + self.host)

    def _initClient(self):
        try:
            self.coapClient = HelperClient(server=(self.host, self.port))
            logging.info('Client created. Will invoke resources at: ' + self.uriPath)
        except Exception as e:
            logging.error("Failed to create CoAP client to URI path: " + self.uriPath)
            traceback.print_exception(type(e), e, e.__traceback__)

    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        self.dataMsgListener = listener
        logging.info("DataMessageListener set.")
        return True

    def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None):
        resourcePath = ""
        hasResource = False
        if resource:
            resourcePath = resourcePath + resource.value
            hasResource = True
        if name:
            if hasResource:
                resourcePath = resourcePath + '/'
            resourcePath = resourcePath + name
        return resourcePath

    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("Discovering remote resources...")

        return self.sendGetRequest(
            resource=None,
            name='.well-known/core',
            enableCON=False,
            timeout=timeout
        )

    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendDeleteRequest called")
        return False

    def sendGetRequest(
        self,
        resource: ResourceNameEnum = None,
        name: str = None,
        enableCON: bool = False,
        timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT
    ) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing GET with path: " + resourcePath)

            request = self.coapClient.mk_request(defines.Codes.GET, path=resourcePath)
            request.token = generate_random_token(2)

            if not enableCON:
                request.type = defines.Types["NON"]

            response = self.coapClient.send_request(request=request, timeout=timeout)

            self._onGetResponse(response=response, resourcePath=resourcePath)
            return True
        else:
            logging.warning("Can't test GET - no path or path list provided.")
            return False

    def _onGetResponse(self, response, resourcePath: str = None):
        if not response:
            logging.warning('GET response invalid. Ignoring.')
            return

        logging.info('GET response received.')

        jsonData = response.payload
        locationPath = resourcePath.split('/') if resourcePath else []

        if len(locationPath) > 2:
            dataType = locationPath[2]

            if dataType == ConfigConst.ACTUATOR_CMD:
                # TODO: convert payload to ActuatorData and verify!
                logging.info("ActuatorData received: %s", jsonData)

                try:
                    from programmingtheiot.data.DataUtil import DataUtil
                    ad = DataUtil().jsonToActuatorData(jsonData)

                    if self.dataMsgListener:
                        self.dataMsgListener.handleActuatorCommandMessage(ad)
                except:
                    logging.warning("Failed to decode actuator data. Ignoring: %s", jsonData)
                    return
            else:
                logging.info("Response data received. Payload: %s", jsonData)
        else:
            logging.info("Response data received. Payload: %s", jsonData)
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendPostRequest called")
        return False

    def sendPutRequest(
        self,
        resource: ResourceNameEnum = None,
        name: str = None,
        enableCON: bool = False,
        payload: str = None,
        timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT
    ) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing PUT with path: " + resourcePath)

            request = self.coapClient.mk_request(defines.Codes.PUT, path=resourcePath)
            request.token = generate_random_token(2)
            request.payload = payload

            if not enableCON:
                request.type = defines.Types["NON"]

            self.coapClient.send_request(
                request=request,
                callback=self._onPutResponse,
                timeout=timeout
            )
            return True
        else:
            logging.warning("Can't test PUT - no path or path list provided.")
            return False

    def _onPutResponse(self, response):
        if not response:
            logging.warning('PUT response invalid. Ignoring.')
            return

        logging.info('PUT response received: %s', response.payload)

    def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        logging.info("startObserver called")
        return False

    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("stopObserver called")
        return False
