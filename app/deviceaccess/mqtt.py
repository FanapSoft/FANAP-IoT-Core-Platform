import paho.mqtt.client
import json


class DAMqtt:

    D2P_TOPIC = 'd2p'

    def __init__(self, app, datastore):
        self.cfg = app.config
        self.ds = datastore

    def start(self):
        self.client = paho.mqtt.client.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        host = self.cfg.get('MQTT_HOST', 'localhost')
        port = self.cfg.get('MQTT_PORT',  1883)
        user = self.cfg.get('MQTT_USR', '')
        password = self.cfg.get('MQTT_PASSWORD', '')

        if user:
            self.client.username_pw_set(user, password)

        self.client.connect(host, port, 60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe('+/' + DAMqtt.D2P_TOPIC)

    def on_message(self, client, userdata, msg):
        # ToDo: Create log when received packet is not correct

        deviceid = DAMqtt.get_deviceid_from_topic(msg.topic)
        if not deviceid:
            return

        msg_dict = DAMqtt.decode_message(msg.payload)

        if not msg_dict:
            return

        self.ds.get_device_message(msg_dict, deviceid)

    @staticmethod
    def get_deviceid_from_topic(topic):
        return topic.split('/')[-2]

    @staticmethod
    def decode_message(message):
        try:
            msg = message
            # Message from MQTT is in byte-array format
            if not isinstance(message, str):
                msg = message.decode('utf-8')

            msg_data = json.loads(msg)
        except json.decoder.JSONDecodeError:
            # ToDo: Log missed packets here
            return None

        return msg_data
