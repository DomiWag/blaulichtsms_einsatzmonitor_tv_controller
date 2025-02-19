import requests
import abc


ips = ["10.3.141.10", "10.3.141.20"]
duration = 10 * 60 * 1000 # in milliseconds
for ip in ips:
    r = requests.get(f"http://{ip}/cm?cmnd=TimedPower%20{duration}")

class LightController(abc.ABC):
    @abc.abstractmethod
    def turn_on(self):
        pass

    @abc.abstractmethod
    def turn_off(self):
        pass

    @abc.abstractmethod
    def set_alarm(self):
        pass

class TasmotaLightController(LightController):
    def __init__(self, ip: str, alarm_duration: int):
        self.ip = ip
        self.alarm_duration = alarm_duration

    def turn_on(self):
        requests.get(f"http://{self.ip}/cm?cmnd=Power%20On")

    def turn_off(self):
        requests.get(f"http://{self.ip}/cm?cmnd=Power%20Off")

    def set_alarm(self):
        requests.get(f"http://{self.ip}/cm?cmnd=TimedPower%20{str(self.alarm_duration)}")