# Wordclock Pro

Wordclock auf Basis eines  Raspberry Pi Pico mit Waveshare e-paper 3.7" Display und MAX 98357A Mono Verstärker. Die Workclock zeigt minütlich die aktuelle Zeit in deutscher Sprache auf dem 3.7" e-paper display an. Z.B. "ES IST FÜNF MINUTEN NACH VIER".

Es gibt einen Hell- und Dunkel-Modus, der im Code von wordclock.py festgelegt werden kann:

```python
# Night_Mode ist Weisse Schrift auf schwarzem Grund (z.B. für nachts)
Night_Mode_Hours = False
# Night_Mode_Hours = True
# Night_Mode_Hours = (18,19,20,21,22,23,0,1,2,3,4,5)
```

Die Uhr wird zweimal am Tag mit einer RTC synchronisiert: Um 02:00 Uhr und im 03:00 (wegen Sommerzeit-Problem)...

- [Benötigte Hardware](#Hardware)
- [Installation](#installation)
- [Links](#Links)

## Hardware
* Raspberry Pi Pico, Pico " oder Pimoroni Pico Plus 2W (mit mehr RAM/Flash für längere Sounds)
* Waveshare e-paper display 3.7", 480 x 280 pixel
* Lautsprecher 3 Watt, 8 Ohm
* MAX 98357A Mono Verstärker
* Buchsenleiste 2 x 20 Pin, 1 x 8 Pin
* Stiftleiste gewinkelt 1 x 8 Pin
* 3 Kurzhubtaster (etwa 6x6x9mm) optimalerweise mit Kappen in Vereinsfarben (schwarz, weiss, grün)
* 4 Schrauben 2.5mm
* 4 Abstandhalter 2.5mm, etwa 30mm lang
* Platine (Muster siehe bei **Links**)
* 5V Stromquelle
* Lötkolben

## Installation
1. Pino, Buchsenleisten, Stiftleiste und Kurzhubtaster auf die Platine löten (Kurzhubtaster auf die Rückseite!)
2. Gehäuse mit 3D-Drucker ausdrucken
3. Platine mittels der Abstandhalter und Schrauben an das e-paper Display anschrauben
4. Platine einbauen
1. API key von **Free Time Zone Database & API** beschaffen
3. Upload all files to your Raspberry Pi Pico (e.g., with [Thonny](https://thonny.org/)).
4. Start wordclock.py (e.g., with Thonny)
5. wordclock needs a wifi connection and an api key for syncing time. This config is saved in wordclock.conf. If not set, wordclock starts a wifi access point *WORDCLOCK*, where you are able to enter the values.
6. To start wordclock automaticaly - rename wordclock.py to main.py

## Links
* [Raspberry Pi Pico-series](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
* [Waveshare 3.7" e-paper display](https://www.waveshare.com/pico-epaper-3.7.htm)
* [Free Time Zone Database & API](https://www.timezonedb.com/)
