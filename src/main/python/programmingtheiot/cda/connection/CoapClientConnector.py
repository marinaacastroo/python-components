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
        logging.info("sendDiscoveryRequest called")
        return False

    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendDeleteRequest called")
        return False

    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendGetRequest called")
        return False

    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendPostRequest called")
        return False

    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("sendPutRequest called")
        return False

    def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        logging.info("startObserver called")
        return False

    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("stopObserver called")
        return False
