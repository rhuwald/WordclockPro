# Wordclock Pro

Wordclock based on a Raspberry Pi Pico with a Waveshare 3.7" e-paper display and a MAX 98357A mono amplifier. The Wordclock displays the current time in German every minute on the 3.7" e-paper display. For example, "ES IST GENAU FÜNF MINUTEN NACH ACHT".

<div><img src="pictures/IMG_8315.JPEG" width="30%" align="left" alt="Screenshot 1">
<img src="pictures/IMG_8316.JPEG" width="30%" align="left" alt="Screenshot 2">
<img src="pictures/IMG_8311.JPEG" width="30%" alt="Screenshot 3"></div>

There is a light and dark mode that can be set in the wordclock.py code:

```python

# Night_Mode is white text on a black background (e.g., for nighttime)
Night_Mode_Hours = False
# Night_Mode_Hours = True
# Night_Mode_Hours = (18,19,20,21,22,23,0,1,2,3,4,5)

```

The clock is synchronized twice a day with an RTC: at 2:00 AM and 3:00 AM (due to daylight saving time issues)...

- [Required Hardware](#Hardware)
- [Installation](#installation)
- [Links](#Links)

The four buttons have the following functions:

- Button 1 announces the current time
- Button 2 plays one of the available SCP fan chants
- Button 3 is used to reset the Wi-Fi connection required (pressing 5 times within 2 seconds deletes the Wi-Fi DNS and API key configuration)
- Button 4 is currently not used in the program and can be used for other purposes

## Hardware
* Raspberry Pi Pico, Pico 2 or Pimoroni Pico Plus 2W (with more RAM/Flash for longer sounds)
* Waveshare e-paper display 3.7", 480 x 280 pixels
* 3-watt, 8-ohm speaker
* MAX 98357A mono amplifier
* 2 x 20-pin female header, 1 x 8-pin female header
* 1 x 8-pin angled male header
* 3 or 4 short-stroke pushbuttons (approx. 6x6x9mm), ideally with caps in club colors (black, white, green)
* 4 x 2.5mm screws
* 4 x 2.5mm standoffs, approx. 30mm long
* Circuit board (see sample in files)
* 5V power supply
* Soldering iron

## Installation

1. Solder the Pico, pin headers, and short-stroke push button onto the circuit board (short-stroke push button on the back!).
2. 3D print the housing.
3. Attach the circuit board to the e-paper display using the standoffs and screws.
4. Install the circuit board.
5. Obtain the API key from **Free Time Zone Database & API**.
6. Copy all files to the Pico (e.g., using [Thonny](https://thonny.org/)).
7. Start wordclock.py (e.g., using Thonny).
8. The Wordclock requires a Wi-Fi connection and an API key for time synchronization. The configuration is saved in the file wordclock.conf. If no Wi-Fi connection or time can be determined, a Wi-Fi hotspot *WORDCLOCK* starts automatically. The configuration (SSID, password, API key) can be entered there.
9. In order for the word clock to start automatically, the file wordclock.py on the Pico must be renamed to main.py

## Links
* [Raspberry Pi Pico-series](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
* [Pimoroni Pico Plus 2W](https://shop.pimoroni.com/products/pimoroni-pico-plus-2-w?variant=42182811942995)
* [Waveshare 3.7" e-paper display](https://www.waveshare.com/pico-epaper-3.7.htm)
* [Free Time Zone Database & API](https://www.timezonedb.com/)


This text was translated using google translate.
