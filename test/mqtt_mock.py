class MockMqtt:

    def __init__(self, app, datastore):
        self.cfg = app.config
        self.ds = datastore
        self.started = False
        self.tx_messages = []

    def start(self):
        self.started = True

    def send_to_device(self, msg, deviceid):
        self.tx_messages.append(
            dict(msg=msg, deviceid=deviceid)
        )

    def receive_from_device(self, msg, deviceid):
        self.ds.get_device_message(msg, deviceid)

    def _get_last_tx_message(self):
        return self.tx_messages[-1]

    def _get_tx_message_cnt(self):
        return len(self.tx_messages)
