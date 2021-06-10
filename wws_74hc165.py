# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 John Woolsey for Woolsey Workshop
#
# SPDX-License-Identifier: MIT

"""
`wws_74hc165`
================================================================================

CircuitPython driver for 74HC165 shift register.

* Author(s): John Woolsey

Implementation Notes
--------------------

Based on Adafruit_CircuitPython_74HC595 driver library.

**Hardware:**

* 74HC165 Shift Register

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""


# Imports
import digitalio
import adafruit_bus_device.spi_device as spi_device

__version__ = "0.0.0-auto.0"
__repo__ = (
    "https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165.git"
)


class DigitalInOut:
    """Digital input/output of the 74HC165.  The interface is exactly the same
    as the ``digitalio.DigitalInOut`` class, however note that by design this
    device is INPUT ONLY!  Attempting to write outputs or set direction as
    output will raise an exception.
    """

    def __init__(self, pin_number, shift_register_74hc165):
        """Specify the pin number of the shift register (0...7) and the
        ShiftRegister74HC165 instance.
        """
        self._pin = pin_number
        self._byte_pos = self._pin // 8
        self._byte_pin = self._pin % 8
        self._shift_register = shift_register_74hc165

    # kwargs in switch functions below are _necessary_ for compatibility
    # with DigitalInout class (which allows specifying pull, etc. which
    # is unused by this class).  Do not remove them, instead turn off pylint
    # in this case.
    # pylint: disable=unused-argument
    def switch_to_output(self, value=False, **kwargs):  # pylint: disable=no-self-use
        """``switch_to_output`` is not supported."""
        raise RuntimeError("Digital output is not supported.")

    def switch_to_input(self, **kwargs):
        """``DigitalInOut switch_to_input``"""
        self.direction = digitalio.Direction.INPUT

    # pylint: enable=unused-argument

    @property
    def value(self):
        """The value of the pin, either True for high or False for low."""
        return self._shift_register.gpio[self._byte_pos] & (1 << self._byte_pin) == (
            1 << self._byte_pin
        )

    @value.setter
    def value(self, val):  # pylint: disable=no-self-use
        """``value`` setting is not supported."""
        raise RuntimeError("Setting value is not supported.")

    @property
    def direction(self):
        """``Direction`` can only be set to ``INPUT``."""
        return digitalio.Direction.INPUT

    @direction.setter
    def direction(self, val):  # pylint: disable=no-self-use
        """``Direction`` can only be set to ``INPUT``."""
        if val != digitalio.Direction.INPUT:
            raise RuntimeError("Digital output is not supported.")

    @property
    def pull(self):
        """Pull-up/down is not supported, return None for no pull-up/down."""
        return None

    @pull.setter
    def pull(self, val):  # pylint: disable=no-self-use
        """Only supports null/no pull state."""
        if val is not None:
            raise RuntimeError("Pull-up and pull-down is not supported.")


class ShiftRegister74HC165:
    """Initialize the 74HC165 on the specified SPI bus and indicate the number
    of shift registers being used.
    """

    def __init__(self, spi, latch, number_of_shift_registers=1):
        self._device = spi_device.SPIDevice(spi, baudrate=1000000)
        self._latch = latch
        self._latch.direction = digitalio.Direction.OUTPUT
        self._number_of_shift_registers = number_of_shift_registers
        self._gpio = bytearray(self._number_of_shift_registers)

    @property
    def number_of_shift_registers(self):
        """The number of shift register chips."""
        return self._number_of_shift_registers

    @property
    def gpio(self):
        """The raw GPIO input register.  Each bit represents the input value of
        the associated pin (0 = low, 1 = high).
        """
        # Manage latch (chip select) separately since it's values needs to be
        # set in reverse.
        self._latch.value = True
        with self._device as spi:
            # pylint: disable=no-member
            spi.readinto(self._gpio)
        self._latch.value = False
        return self._gpio

    @gpio.setter
    def gpio(self, val):  # pylint: disable=no-self-use
        """``gpio`` setting is not supported."""
        raise RuntimeError("Setting gpio is not supported.")

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this 74HC165 device.
        """
        assert 0 <= pin <= (self._number_of_shift_registers * 8) - 1
        return DigitalInOut(pin, self)
