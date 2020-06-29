from pyfcm import FCMNotification


class FCMSender():
    def __init__(self, api_key):
        self.fcm_service = FCMNotification(api_key=api_key)
        self.device_tokens = list()
    
    def add_device(self, device_token):
        self.device_tokens.append(device_token)

    def send(self, title, body):
        result = self.fcm_service.notify_multiple_devices(registration_ids=self.device_tokens,
                                                        message_title=title,
                                                        message_body=body)

        print(result)
        return result