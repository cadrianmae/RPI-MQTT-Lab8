"""
RP2040 Temperature Sensor Module
Reads temperature from the built-in ADC temperature sensor

Author: Mae Capacite (C21348423)
Date: 2025-11-14
"""

import machine
import micropython as mp


class TempSensor:
    """
    RP2040 Temperature Sensor Interface.

    Uses the built-in ADC temperature sensor with calibration constants
    from the RP2040 datasheet.

    Reference: https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
    """

    # Constants for ADC and temperature conversion
    U16_MAX = mp.const(2 ** 16)
    ADC_AVDD = mp.const(3.3)  # ADC reference voltage
    ADC_PIN = mp.const(4)  # ADC pin for temperature sensor

    # Temperature calibration constants from datasheet
    TEMP_REFERENCE = mp.const(27)  # Reference temperature (°C)
    VOLTAGE_AT_REFERENCE = mp.const(0.706)  # Voltage at reference temp (V)
    TEMP_COEFFICIENT = mp.const(0.001721)  # Temperature coefficient (V/°C)

    def __init__(self):
        """Initialize the temperature sensor ADC."""
        self.sensor = machine.ADC(self.ADC_PIN)

    def read_temp(self) -> float:
        """
        Read temperature in degrees Celsius.

        Returns:
            Temperature in °C as a float
        """
        # Read raw 16-bit ADC value
        raw_value = self.sensor.read_u16()

        # Convert ADC reading to voltage
        adc_voltage = raw_value * (self.ADC_AVDD / self.U16_MAX)

        # Calculate temperature using calibration formula
        # T = T_ref - (V_adc - V_ref) / T_coeff
        temperature = (
            self.TEMP_REFERENCE -
            (adc_voltage - self.VOLTAGE_AT_REFERENCE) / self.TEMP_COEFFICIENT
        )

        return temperature

    def __str__(self) -> str:
        """String representation showing current temperature reading."""
        return f"TempSensor: {self.read_temp():.2f}°C"
