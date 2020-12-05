import enum
import subprocess
import os


FCM_API_KEY = "AAAAMhLA7II:APA91bEOUdF8RdDSmaX2U52xJRHnYzlRWwHg8B5FgTw5eQD9zotxrmy6-_iJccBtzsLQKxAg8yRM8nt_CyKuMnEpiz5lWCpfwLttWXehZqZQwP7HVkHvvAjQiNoto3UGKtvoxyFW3sfN"
DEVICE_TOKEN = "fNPHIdmDO1o:APA91bGIBfb7nJ3n7qtMLCM1gLZT7c2M-Wt64QOQRW55hPkkfhGe1aS27hJKIwSko8nKfHful4MNT-yEvlHmXUFi1mc9VM41a6-vYo1UiApPnZjKS5h4EVHIxPp102zCZhu4ALLU7iVy"

class CameraMode(enum.Enum):
    WEBCAM = 0
    REALSENSE = 1
    KVS = 2
    ZMQ = 3

camera_mode = CameraMode.ZMQ
