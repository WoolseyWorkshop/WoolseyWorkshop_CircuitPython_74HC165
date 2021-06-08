Introduction
============
.. image:: https://readthedocs.org/projects/woolseyworkshop-circuitpython-74hc165/badge/?version=latest
    :target: https://woolseyworkshop-circuitpython-74hc165.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165/workflows/Build%20CI/badge.svg
    :target: https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython driver for 74HC165 shift register.


Dependencies
============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing from PyPI
====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/woolseyworkshop-circuitpython-74hc165/>`_.
To install for current user:

.. code-block:: shell

    pip3 install woolseyworkshop-circuitpython-74hc165

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install woolseyworkshop-circuitpython-74hc165

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install woolseyworkshop-circuitpython-74hc165


Usage Example
=============
.. code-block:: python

    import time
    import board
    import digitalio
    import wws_74hc165

    latch_pin = digitalio.DigitalInOut(board.D5)
    sr = wws_74hc165.ShiftRegister74HC165(board.SPI(), latch_pin)

    pin1 = sr.get_pin(1)

    while True:
        print(f"pin 1 = {pin1.value}")
        time.sleep(1)


Contributing
============
Contributions are welcome! Please read our `Code of Conduct
<https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.


Documentation
=============
For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
