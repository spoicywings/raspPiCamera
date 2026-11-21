from INA219 import INA219


class Battery:
    def __init__(self):
        # Waveshare UPS HAT (C) uses I2C address 0x43
        self.sensor = INA219(addr=0x43)

    def get_status(self):
        voltage = self.sensor.getBusVoltage_V()
        current = self.sensor.getCurrent_mA() / 1000
        power = self.sensor.getPower_W()

        # Waveshare's voltage-based battery percentage estimate
        percent = (voltage - 3.0) / 1.2 * 100
        percent = max(0, min(100, percent))

        return {
            "voltage": voltage,
            "current": current,
            "power": power,
            "percent": percent
        }