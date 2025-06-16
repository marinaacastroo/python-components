import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener

class MqttClientControlPacketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Ejecutando MqttClientControlPacketTest...")
        cls.cfg = ConfigUtil()
        # Asegúrate de usar un clientID único para estos tests
        cls.mcc = MqttClientConnector(clientID="MyTestMqttControlClient")
        cls.mcc.setDataMessageListener(DefaultDataMessageListener())

    def setUp(self):
        pass

    def tearDown(self):
        # Desconecta si no estuviera ya desconectado
        try:
            self.mcc.disconnectClient()
        except Exception:
            pass

    def testConnectAndDisconnect(self):
        """
        Test para verificar los paquetes CONNECT, CONNACK y DISCONNECT.
        """
        self.mcc.connectClient()
        sleep(2)  # Espera breve para que se establezca la conexión y se reciba CONNACK
        self.mcc.disconnectClient()
        # Aquí se podrían hacer asserts si tu implementación expone estados o callbacks

    def testServerPing(self):
        """
        Test para verificar que el keep-alive envía PINGREQ y se recibe PINGRESP.
        Configurar un keep-alive corto en la configuración ayudará.
        """
        self.mcc.connectClient()
        # Espera suficiente para que venza el intervalo keep-alive (usando la configuración)
        keepAliveInterval = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
        sleep(keepAliveInterval + 2)
        self.mcc.disconnectClient()
        # Aquí se debería validar a través de logs o un callback que se envió PINGREQ/recibió PINGRESP

    def testPubSubWithQoS1(self):
        """
        Test para generar los paquetes de publicación/suscripción usando QoS 1.
        Debe generar PUB, PUBACK, SUB, SUBACK, UNSUB, UNSUBACK.
        """
        qos = 1
        self.mcc.connectClient()
        sleep(2)
        self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=qos)
        sleep(1)
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="Test message QoS 1", qos=qos)
        sleep(3)
        self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
        sleep(1)
        self.mcc.disconnectClient()

    def testPubSubWithQoS2(self):
        """
        Test para generar la secuencia de control para QoS 2:
        Esto incluirá la secuencia PUBREC, PUBREL y PUBCOMP.
        """
        qos = 2
        self.mcc.connectClient()
        sleep(2)
        self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=qos)
        sleep(1)
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="Test message QoS 2", qos=qos)
        sleep(3)
        self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
        sleep(1)
        self.mcc.disconnectClient()

if __name__ == "__main__":
    unittest.main()