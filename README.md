YABATMan
========

Yet Another Bitcoin ATM (man) main repo !

Everything's very experimental at the time, and the code is pretty messy...

The software part is basically based on :

- [Piper Printer](https://github.com/piperwallet/Piper)
- [Adafruit Thermal printer library for python](https://github.com/adafruit/Adafruit-Thermal-Printer-Library)

The main FSM is _gui.py_. It's a TKinter GUI python script that handles the whole process.

The hardware side is based on :

- An actual ATM
- A RPi + screen
- A wee Arduino Micro, to get the signals from the inputs (ATM buttons), and to create a keyboard input on the RPi accordingly
- A Adafruit Thermal Printer
- A cash reader, idealy with a parallel interface (ccTalk is a nonsense...) connected to the Arduino
- Some random components (FT232, level shifters...)

More to come on this side, sorry for the lack of information !
