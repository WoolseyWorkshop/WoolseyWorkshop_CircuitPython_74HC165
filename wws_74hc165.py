# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: 2021 John Woolsey for Woolsey Workshop
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


import digitalio
from adafruit_bus_device import spi_device

try:
    import typing  # pylint: disable=unused-import
    from microcontroller import Pin
    import busio
    from circuitpython_typing import ReadableBuffer
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = (
    "https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165.git"
)


class DigitalInOut:
    """Digital input/output of the 74HC165.  The interface is exactly the same
    as the ``digitalio.DigitalInOut`` class, however note that by design this
    device is INPUT ONLY!  Attempting to write outputs or set direction as
    output will raise an exception.
    """

    _pin: Pin
    _byte_pos: int
    _byte_pin: int
    _shift_register: "ShiftRegister74HC165"

    def __init__(
        self, pin_number: Pin, shift_register_74hc165: "ShiftRegister74HC165"
    ) -> None:
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
    def switch_to_output(  # pylint: disable=no-self-use
        self, value: bool = False, **kwargs
    ) -> None:
        """``switch_to_output`` is not supported."""
        raise RuntimeError("Digital output is not supported.")

    def switch_to_input(self, **kwargs) -> None:
        """``DigitalInOut switch_to_input``"""
        self.direction = digitalio.Direction.INPUT

    # pylint: enable=unused-argument

    @property
    def value(self) -> bool:
        """The value of the pin, either True for high or False for low."""
        return self._shift_register.gpio[self._byte_pos] & (1 << self._byte_pin) == (
            1 << self._byte_pin
        )

    @value.setter
    def value(self, val: bool) -> None:  # pylint: disable=no-self-use
        """``value`` setting is not supported."""
        raise RuntimeError("Setting value is not supported.")

    @property
    def direction(self) -> digitalio.Direction.INPUT:
        """``Direction`` can only be set to ``INPUT``."""
        return digitalio.Direction.INPUT

    @direction.setter
    def direction(  # pylint: disable=no-self-use
        self, val: digitalio.Direction.INPUT
    ) -> None:
        """``Direction`` can only be set to ``INPUT``."""
        if val != digitalio.Direction.INPUT:
            raise RuntimeError("Digital output is not supported.")

    @property
    def pull(self) -> None:
        """Pull-up/down is not supported, return None for no pull-up/down."""
        return None

    @pull.setter
    def pull(self, val: None) -> None:  # pylint: disable=no-self-use
        """Only supports null/no pull state."""
        if val is not None:
            raise RuntimeError("Pull-up and pull-down are not supported.")


class ShiftRegister74HC165:
    """Initialize the 74HC165 on the specified SPI bus, indicate the
    number of shift registers being used, and the optional baudrate.
    """

    _device: spi_device.SPIDevice
    _number_of_shift_registers: int
    _gpio: ReadableBuffer

    def __init__(
        self,
        spi: busio.SPI,
        latch: digitalio.DigitalInOut,
        number_of_shift_registers: int = 1,
        baudrate: int = 1000000,
    ) -> None:
        self._device = spi_device.SPIDevice(spi, baudrate=baudrate)
        self._latch = latch
        self._latch.direction = digitalio.Direction.OUTPUT
        self._number_of_shift_registers = number_of_shift_registers
        self._gpio = bytearray(self._number_of_shift_registers)

    @property
    def number_of_shift_registers(self) -> int:
        """The number of shift register chips."""
        return self._number_of_shift_registers

    @property
    def gpio(self) -> ReadableBuffer:
        """The raw GPIO input register.  Each bit represents the input value of
        the associated pin (0 = low, 1 = high).
        """
        # Manage the latch (chip select) separately since it's values needs to
        # be set in reverse.
        self._latch.value = True
        with self._device as spi:
            # pylint: disable=no-member
            spi.readinto(self._gpio)
        self._latch.value = False
        return self._gpio

    @gpio.setter
    def gpio(self, val: ReadableBuffer) -> None:  # pylint: disable=no-self-use
        """``gpio`` setting is not supported."""
        raise RuntimeError("Setting gpio is not supported.")

    def get_pin(self, pin: int) -> DigitalInOut:
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this 74HC165 device.
        """
        assert 0 <= pin <= (self._number_of_shift_registers * 8) - 1
        return DigitalInOut(pin, self)
