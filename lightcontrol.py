import requests
import abc
import configparser
import logging


class BaseAlarmLight(abc.ABC):
    @abc.abstractmethod
    def turn_on(self):
        pass

    @abc.abstractmethod
    def turn_off(self):
        pass

    @abc.abstractmethod
    def set_alarm(self):
        pass

class TasmotaAlarmLight(BaseAlarmLight):
    def __init__(self, ip: str, alarm_duration_seconds: int):
        self.logger = logging.getLogger(__name__)
        self.ip = ip
        self.alarm_duration = alarm_duration_seconds * 1000 # Convert to milliseconds

    def turn_on(self):
        self.logger.info(f"Turning on light at {self.ip}")
        requests.get(f"http://{self.ip}/cm?cmnd=Power%20On")

    def turn_off(self):
        self.logger.info(f"Turning off light at {self.ip}")
        requests.get(f"http://{self.ip}/cm?cmnd=Power%20Off")

    def set_alarm(self):
        try:
            self.logger.info(f"Setting alarm on light at {self.ip} for {str(self.alarm_duration)} ms")
            requests.get(f"http://{self.ip}/cm?cmnd=TimedPower%20{str(self.alarm_duration)}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to set alarm on light at {self.ip}: {e}")

class AlarmLightController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.lights = []

        # Read lights from config
        config = configparser.ConfigParser()
        config.read("config.ini")
        light_count = int(config["alarm_lights"]["count"])
        for i in range(light_count):
            light_section = f"alarm_light_{i}"
            address = config[light_section]["address"]
            username = config[light_section]["username"]
            password = config[light_section]["password"]
            on_time = int(config[light_section]["on_time"])
            self.lights.append(TasmotaAlarmLight(address, on_time))

    def set_alarm(self):
        self.logger.info("Setting alarm on all lights")
        for light in self.lights:
            light.set_alarm()