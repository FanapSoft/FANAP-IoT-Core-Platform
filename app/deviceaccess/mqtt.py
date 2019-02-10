import paho.mqtt.client


class DAMqtt:

    D2P_TOPIC = 'd2p'
    P2D_TOPIC = 'p2d'

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
        self.use_shared_sub = self.cfg.get('MQTT_EMQ_SHARED_SUB', False)

        if user:
            self.client.username_pw_set(user, password)

        self.client.connect(host, port, 60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        topic = '/+/' + DAMqtt.D2P_TOPIC
        if self.use_shared_sub:
            # Using emqttd as broker. Check https://emqttd-docs.readthedocs.io/en/latest/advanced.html
            topic = '$queue/' + topic

        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        # ToDo: Create log when received packet is not correct
        deviceid = DAMqtt.get_deviceid_from_topic(msg.topic)
        if not deviceid:
            return

        msg = DAMqtt.decode_message(msg.payload)

        if not msg:
            return

        self.ds.get_device_message(msg, deviceid)

    def send_to_device(self, msg, deviceid):
        self.client.publish(
            DAMqtt._get_platform_to_device_topic(deviceid),
            payload=msg)

    @staticmethod
    def _get_platform_to_device_topic(deviceid):
        return '/{}/{}'.format(deviceid, DAMqtt.P2D_TOPIC)

    @staticmethod
    def get_deviceid_from_topic(topic):
        return topic.split('/')[-2]

    @staticmethod
    def decode_message(message):

        if not isinstance(message, str):
            try:
                message = message.decode('utf-8')
            except UnicodeDecodeError:
                # ToDo: how to packets with encoding issue
                return False
        return message
