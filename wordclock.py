import asyncio
import bixel
import machine
from picozero_button import Button
import random
import rtc
import sys
import time
import wlan
import wordclockconfig


print(f'Programm          : WordClock ePaper (3.7" Version)')
print(f'Machine-Id        : {machine.unique_id()}')
print(f'Machine-Freq      : {machine.freq() / 1_000_000} MHz')
print(f'sys.implementation: {sys.implementation}')

"""
Pico W:          sys.implementation: (
                    name='micropython',
                    version=(1, 22, 0, ''),
                    _machine='Raspberry Pi Pico W with RP2040',
                    _mpy=4614)
Pimoroni Plus 2: sys.implementation: (
                    name='micropython',
                    version=(1, 27, 0, 'preview'),
                    _machine='Pimoroni Pico Plus 2 (PSRAM + LTE + WiFi) with RP2350',
                    _mpy=7942,
                    _build='pimoroni_pico_plus2',
                    _thread='unsafe')
"""

if "Pimoroni Pico Plus" in sys.implementation._machine:
    print("Pico Plus gefunden, SCP komplette Fassung")
    SCP_WAV = ("allez_allez_allez.wav", "alle_zusammen.wav", "scheiss_osna.wav", "vorwärts_sc_preussen_muenster.wav", "scp.wav")
    SCP_WAV_last = 0
    
    Es_ist_1906_WAV = "es_ist_genau_19_uhr_6.wav"
else:
    print("Kein Pico Plus gefunden, kein SCP Sound")
    SCP_WAV = None
    Es_ist_1906_WAV = "es_ist_genau_19_uhr_6.wav"

# Bixel initialisieren (Big Pixel)
print("vor Bixel")
Bixel = bixel.Bixel(X_Size = 4, Y_Size = 4, X_Spacing = 1, Y_Spacing = 1, X_Offset = 3, Y_Offset = -3)
print("nach bixel")

# Sound via I2S Anfang
# Die Soundschnipsel stammen von:
# - URL   : https://speechgen.io/de
# - Stimme: Alma
# - Speed : 0,9x
SOUND = True
if SOUND == True:
    from wavplayer import WavPlayer
    wp = WavPlayer(
        id     = 0,
        sck_pin= machine.Pin(16),
        ws_pin = machine.Pin(17),
        sd_pin = machine.Pin(18),
        ibuf   = 5_000,
        root   = "/sound"
    )
# Sound via I2S Ende

# Merker für "letzte Worte", damit das Display nicht unnötig aktualisiert wird
Last_Words = None

time_or_scp = None

reset_wifi_ticks = {}
for _ in range(0,5):
    reset_wifi_ticks[_] = False


def say_time():
    # print("Button 1/19 gedrückt")
    global time_or_scp
    time_or_scp = "time"

def sing_scp():
    # print("Button 2/20 gedrückt")
    global time_or_scp
    time_or_scp = "scp"

def button_reset_wifi_pressed():
    # print("Button 3/21 gedrückt")
    global reset_wifi_ticks
    reset_wifi_ticks[0] = reset_wifi_ticks[1]
    reset_wifi_ticks[1] = reset_wifi_ticks[2]
    reset_wifi_ticks[2] = reset_wifi_ticks[3]
    reset_wifi_ticks[3] = reset_wifi_ticks[4]
    reset_wifi_ticks[4] = time.ticks_ms()
    
    if reset_wifi_ticks[0] is not None:
        diff = reset_wifi_ticks[4] - reset_wifi_ticks[0]
        if diff <= 2000:
            print("5x reset gedrückt...")
            for _ in range(0,5):
               reset_wifi_ticks[_] = False
            if wordclockconfig.delete_config() == True:
                # raise SystemExit
                time_or_scp = "SystemExit"

def Get_Active_Words(Local_Time = None):
    if Local_Time == None:
        Local_Time = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    
    Active_Words = []
    Active_Words.append("ES")
    Active_Words.append("IST")
    
    if Local_Minute % 5 == 0:
            Active_Words.append("GENAU")
    if Local_Minute == 0:
        # Active_Words.append("UHR")
        pass
    elif Local_Minute in (1,2):
        for _ in ("KURZ", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (3,4,5,6,7):
        for _ in ("FUENF", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (8,9,10,11,12):
        for _ in ("ZEHN", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (13,14,15,16,17):
        for _ in ("VIERTEL","NACH"):
            Active_Words.append(_)
    elif Local_Minute in (18,19,20,21,22):
        for _ in ("ZWANZIG", "MINUTEN", "NACH"):
            Active_Words.append(_)
    elif Local_Minute in (23,24,25,26,27):
        for _ in ("FUENF", "MINUTEN", "VOR", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (28,29):
        for _ in ("KURZ", "VOR", "HALB"):
            Active_Words.append(_)
    elif Local_Minute == 30:
        Active_Words.append("HALB")
    elif Local_Minute in (31,32):
        for _ in ("KURZ", "NACH", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (33,34,35,36,37):
        for _ in ("FUENF", "MINUTEN", "NACH", "HALB"):
            Active_Words.append(_)
    elif Local_Minute in (38,39,40,41,42):
        for _ in ("ZWANZIG", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (43,44,45,46,47):
        for _ in ("VIERTEL", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (48,49,50,51,52):
        for _ in ("ZEHN", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (53,54,55,56,57):
        for _ in ("FUENF", "MINUTEN", "VOR"):
            Active_Words.append(_)
    elif Local_Minute in (58,59):
        for _ in ("KURZ", "VOR"):
            Active_Words.append(_)
    
    # Stunde noch berechnen
    Local_Hour_Logical = Local_Hour
    if Local_Minute == 0 and Local_Hour == 1:
        Local_Hour_Logical = -1
    elif Local_Minute >= 23:
        Local_Hour_Logical += 1
    
    if Local_Hour_Logical == 0:
        Local_Hour_Logical = 12
    elif Local_Hour_Logical > 12:
        Local_Hour_Logical -= 12
    
    Active_Words.append(Local_Hour_Logical)
    
    if Local_Minute == 0:
        Active_Words.append("UHR")
    
    return Active_Words



async def main():
    global time_or_scp, Last_Words, reset_wifi_ticks
    print("buttons initialisieren")
    button_say_time                = Button(19) #, pull_up = False)
    button_say_time.when_pressed   = say_time
    button_sing                    = Button(20) #, pull_up = False)
    button_sing.when_pressed       = sing_scp
    button_reset_wifi              = Button(21) #, pull_up = False)
    button_reset_wifi.when_pressed = button_reset_wifi_pressed
    
    print("lege task an")
    asyncio.create_task(time_or_scp_task())
    print("task ist angelegt")
    
    # Night_Mode ist Weisse Schrift auf schwarzem Grund (z.B. für nachts)
    # Night_Mode_Hours = False
    # Night_Mode_Hours = True
    Night_Mode_Hours = (18,19,20,21,22,23,0,1,2,3,4,5)
    
    SSID, PASSWORD, API_KEY = wordclockconfig.load_config()
    
    # WLAN aktivieren (notwendig für Ermittlung der aktuellen Uhrzeit)
    WLAN = wlan.WLAN(verbose_mode = True)

    while WLAN.connect(ssid=SSID, password = PASSWORD, timeout = 30) == False:
        WLAN.info()
        Bixel.ePaper.image4Gray.fill(Bixel.ePaper.white)
        Bixel.Draw_Word(5, Bixel.Y_Max, "WLAN ERROR", Bixel.ePaper.black, True, 270)
        Bixel.Draw_Word(5 + 7 + 7, Bixel.Y_Max, "STARTE NUN DEN", Bixel.ePaper.black, False, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7, Bixel.Y_Max, "WLAN HOTSPOT", Bixel.ePaper.black, False, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max, "-= WORDCLOCK =-", Bixel.ePaper.black, True, 270)
        Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
        
        # Phew Accesspoint starten (wird beendet, sobald die Config geschrieben wird)
        wordclockconfig.ap_start()
        # Config erneut einlesen
        SSID, PASSWORD, API_KEY = wordclockconfig.load_config()


    # Realtimeclock setzen anhand der Zeit eines Timeservers
    while rtc.set(API_KEY) == False:
        print("RTC ERROR")
        Bixel.ePaper.image4Gray.fill(Bixel.ePaper.white)
        Bixel.Draw_Word(5, Bixel.Y_Max, "RTC ERROR", Bixel.ePaper.black, True, 270)
        Bixel.Draw_Word(5 + 7 + 7, Bixel.Y_Max, "STARTE NUN DEN", Bixel.ePaper.black, False, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7, Bixel.Y_Max, "WLAN HOTSPOT", Bixel.ePaper.black, False, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max, "-= WORDCLOCK =-", Bixel.ePaper.black, True, 270)
        Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
        
        # Phew Accesspoint starten (wird beendet, sobald die Config geschrieben wird)
        wordclockconfig.ap_start()
        
        # Config erneut einlesen
        SSID, PASSWORD, API_KEY = wordclockconfig.load_config()


    # WLAN de-aktivieren (zum Strom sparen)
    WLAN.disconnect()
    
    # Beim Start der Uhr erstmal dem Geburtstagskind zum Geburtstag gratulieren...
    if False:
        Bixel.ePaper.image4Gray.fill(Bixel.ePaper.white)
        Bixel.Draw_Word(5, Bixel.Y_Max - 6, "LIEBER XXXX!!!", Bixel.ePaper.black, True, 270)
        Bixel.Draw_Word(5 + 7 + 7, Bixel.Y_Max - 3, "ALLES LIEBE ZUM", Bixel.ePaper.black, True, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7, Bixel.Y_Max - 3, "99. GEBURTSTAG!!!", Bixel.ePaper.black, True, 270)
        Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max - 3, "VON A, B, C + D", Bixel.ePaper.black, True, 270)
        for _ in range(Bixel.Y_Max, 0, -1):
            Bixel.Draw( + 7 + 7 + 7 + 7 + 7 + 7 + 4, _, Bixel.ePaper.black, False)
        Bixel.Draw_Word(5 + 7 + 7 + 7 + 7 + 7 + 7 + 7, Bixel.Y_Max, "NUR DER SCP 1906", Bixel.ePaper.black, False, 270)
        Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
        if SOUND == True:
            if SCP_WAV != None:
                print("Spiele allez_allez_allez.wav")
                wp.play("allez_allez_allez.wav", loop=False)
                while wp.isplaying():
                    time.sleep(1)
        else:
            time.sleep(30)
    
    # Alle Buchstaben der Uhr (8 Zeilen mit je 16 Zeichen)
    Clock_Letters = [
        'ESQLZISTHXGENAUM',
        'IFÜNFKZEHNGKURZR',
        'ZWANZIGDVIERTELA',
        'MINUTENYÖVORNACH',
        'HALBÜSECHSIEBENW',
        'MDREINSBZWEIJELF',
        'UVIERSZWÖLFÜNFEQ',
        'PACHTZEHNEUNÄUHR'
    ]


    # Positionen der einzelnen Teil-Worte und Zahlen
    Clock_Words = {}
    Clock_Words["ES"]       = [[0,0],  [0,1]]
    Clock_Words["IST"]      = [[0,5],  [0,6],  [0,7]]
    Clock_Words["GENAU"]    = [[0,10], [0,11], [0,12], [0,13],[0,14]]
    Clock_Words["FUENF"]    = [[1,1],  [1,2],  [1,3],  [1,4]]
    Clock_Words["ZEHN"]     = [[1,6],  [1,7],  [1,8],  [1,9]]
    Clock_Words["KURZ"]     = [[1,11], [1,12], [1,13], [1,14]]
    Clock_Words["ZWANZIG"]  = [[2,0],  [2,1],  [2,2],  [2,3],[2,4],[2,5],[2,6]]
    Clock_Words["VIERTEL"]  = [[2,8],  [2,9],  [2,10], [2,11],[2,12],[2,13],[2,14]]
    Clock_Words["MINUTEN"]  = [[3,0],  [3,1],  [3,2],  [3,3],[3,4],[3,5],[3,6]]
    Clock_Words["VOR"]      = [[3,9],  [3,10],  [3,11]]
    Clock_Words["NACH"]     = [[3,12], [3,13], [3,14], [3,15]]
    Clock_Words["HALB"]     = [[4,0],  [4,1],  [4,2],  [4,3]]
    Clock_Words[6]          = [[4,5],  [4,6],  [4,7],  [4,8],[4,9]]
    Clock_Words[7]          = [[4,9],  [4,10], [4,11], [4,12],[4,13],[4,14]]
    Clock_Words[3]          = [[5,1],  [5,2],  [5,3],  [5,4]]
    Clock_Words[-1]         = [[5,3],  [5,4],  [5,5]]
    Clock_Words[1]          = [[5,3],  [5,4],  [5,5],  [5,6]]
    Clock_Words[2]          = [[5,8],  [5,9],  [5,10], [5,11]]
    Clock_Words[11]         = [[5,13], [5,14], [5,15]]
    Clock_Words[4]          = [[6,1],  [6,2],  [6,3],  [6,4]]
    Clock_Words[12]         = [[6,6],  [6,7],  [6,8],  [6,9],[6,10]]
    Clock_Words[5]          = [[6,10], [6,11], [6,12], [6,13]]
    Clock_Words[8]          = [[7,1],  [7,2],  [7,3],  [7,4]]
    Clock_Words[10]         = [[7,5],  [7,6],  [7,7],  [7,8]]
    Clock_Words[9]          = [[7,8],  [7,9],  [7,10], [7,11]]
    Clock_Words["UHR"]      = [[7,13], [7,14], [7,15]]


    # Nächsten Lauf für Ermittlung der Uhrzeit (wegen Sommer-/Winterzeitwechsel) festlegen
    Local_Time   = time.localtime()
    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
    if Local_Hour < 2: #                   Nächster Lauf um 02:00
        next_run = time.mktime((Local_Year, Local_Month, Local_Day, 2, 0, 0, 0, 0))
    elif Local_Hour == 2: #                Nächster Lauf um 03:00
        next_run = time.mktime((Local_Year, Local_Month, Local_Day, 3, 0, 0, 0, 0))
    else: #                                Nächster Lauf morgen um 02:00
        next_run = time.mktime((Local_Year, Local_Month, Local_Day + 1, 2, 0, 0, 0, 0))
    
    
    while True:
        Local_Time  = time.localtime()
        Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
        print(f"RTC Uhrzeit {Local_Hour:02d}:{Local_Minute:02d}:{Local_Second:02d}")
        
        if next_run <= time.time():
            print("RTC wird nun neugestellt...")
            if WLAN.connect(timeout = 5) == True:
                if rtc.set() == True:
                    print("RTC erfolgreich neugestellt...")
                    Local_Time  = time.localtime()
                    Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
                    if Local_Hour < 2: #       Nächster Lauf um 02:00
                        next_run = time.mktime((Local_Year, Local_Month, Local_Day, 2, 0, 0, 0, 0))
                    elif Local_Hour == 2: #    Nächster Lauf um 03:00
                        next_run = time.mktime((Local_Year, Local_Month, Local_Day, 3, 0, 0, 0, 0))
                    else: #                    Nächster Lauf morgen um 02:00
                        next_run = time.mktime((Local_Year, Local_Month, Local_Day  + 1, 2, 0, 0, 0, 0))
                    WLAN.disconnect()
                else: #                        Nächster Lauf in 1 Minute
                    print("RTC ERROR, neuer Versuch in 60 Sekunden...")
                    next_run += 60
            else:
                print("RTC ERROR (WLAN ERROR), neuer Versuch in 60 Sekunden...")
                next_run += 60
        else:
            next_run_time     = next_run-time.time()
            next_run_stunden  = next_run_time // 3600
            next_run_sekunden = next_run_time % 3600
            next_run_minuten  = next_run_sekunden // 60
            next_run_sekunden = next_run_sekunden % 60
            print(f"RTC wird in {next_run_stunden} Stunde(n), {next_run_minuten} Minute(n), {next_run_sekunden} Sekunde(n) neugestellt...")
            
        Local_Time  = time.localtime()
        Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
        
        Active_Words = Get_Active_Words(Local_Time)
        print(Active_Words)
        
        # Die Uhrzeit nur aktualisieren, wenn sich die Anzeige geändert hat
        if Active_Words != Last_Words:
            
            print("Aktualisiere das epaper Display...")
            Last_Words = Active_Words
            
            # Night_Mode prüfen
            if (type(Night_Mode_Hours) == bool) and (Night_Mode_Hours == True):
                # print("Night_Mode on")
                Color_Background  = Bixel.ePaper.black
                Color_Letter_On   = Bixel.ePaper.white
                Filled_Letter_On  = True
                Color_Letter_Off  = Bixel.ePaper.darkgray
                Filled_Letter_Off = True
            elif (type(Night_Mode_Hours) == tuple) and (Local_Hour in Night_Mode_Hours):
                # print("Night_Mode on")
                Color_Background  = Bixel.ePaper.black
                Color_Letter_On   = Bixel.ePaper.white
                Filled_Letter_On  = True
                Color_Letter_Off  = Bixel.ePaper.darkgray
                Filled_Letter_Off = True
            else:
                # print("Night_Mode off")
                Color_Background  = Bixel.ePaper.white
                Color_Letter_On   = Bixel.ePaper.black
                Filled_Letter_On  = True
                Color_Letter_Off  = Bixel.ePaper.grayish
                Filled_Letter_Off = True
            
            # Komplette Anzeige leeren
            Bixel.ePaper.image4Gray.fill(Color_Background)
            
            # Gewünschte Buchstaben der Uhr "highlighten"
            Clock_Colors = [[(Color_Letter_Off, Filled_Letter_Off) for x in range(16)] for y in range(8)]
            
            for Active_Word in Active_Words:
                Clock_Word = Clock_Words[Active_Word]
                for _ in range(len(Clock_Word)):
                    Clock_Colors[Clock_Word[_][0]][Clock_Word[_][1]] = (Color_Letter_On, Filled_Letter_On)
            
            # Aktuelle Uhrzeit anzeigen (Alle Buchstaben zeichnen)
            x = 5 #                            Untere Reihe der 1. Zeile
            for _ in range(0, len(Clock_Letters)):
                Clock_Letters_Line = Clock_Letters[_]
                y = Bixel.Y_Max #        1. Spalte der aktuellen Zeile
                for __ in range(0, len(Clock_Letters_Line)):
                    color, filled = Clock_Colors[_][__]
                    Bixel.Draw_Letter(x, y, Clock_Letters_Line[__], color, filled, 270)
                    y -= 6
                x += 7
            
            # ePaper aktualisieren
            Bixel.ePaper.EPD_3IN7_4Gray_Display(Bixel.ePaper.buffer_4Gray)
        
        # Sound via I2S Anfang
        if SOUND == True:
            if (Local_Hour == 19) and (Local_Minute == 6):
                what_to_say = "1906"
        # Sound via I2S Ende
        
        Local_Time   = time.localtime()
        Local_Year, Local_Month, Local_Day, Local_Hour, Local_Minute, Local_Second, Local_DoW, Local_DoY = Local_Time
        
        print(f'Warte {60 - Local_Second} Sekunde(n) bis zur nächsten vollen Minute')
        
        await asyncio.sleep(60 - Local_Second)
        
        print("Bin wieder wach...")



async def time_or_scp_task():
    global time_or_scp, wp, SOUND, Last_Words, SCP_WAV_last
    print('starte time_or_scp_task')
    
    while True:
        await asyncio.sleep(.25)
        
        if time_or_scp == "SystemExit":
            raise SystemExit
        
        if SOUND == True:
            if time_or_scp == "1906":
                time_or_scp = None
                if wp.isplaying():
                    wp.stop()
                if Es_ist_1906_WAV != None:
                    wp.play(Es_ist_1906_WAV, loop=False)
            elif time_or_scp == "time":
                time_or_scp = None
                if Last_Words != None:
                    if wp.isplaying():
                        wp.stop()
                    else:
                        for Last_Word in Last_Words:
                            while wp.isplaying():
                                await asyncio.sleep_ms(10)
                            if time_or_scp != None:
                                break
                            if Last_Word == -1:
                                Last_Word = 'ein'
                            elif Last_Word == 1:
                                Last_Word = 'eins'
                            elif Last_Word == 2:
                                Last_Word = 'zwei'
                            elif Last_Word == 3:
                                Last_Word = 'drei'
                            elif Last_Word == 4:
                                Last_Word = 'vier'
                            elif Last_Word == 5:
                                Last_Word = 'fuenf'
                            elif Last_Word == 6:
                                Last_Word = 'sechs'
                            elif Last_Word == 7:
                                Last_Word = 'sieben'
                            elif Last_Word == 8:
                                Last_Word = 'acht'
                            elif Last_Word == 9:
                                Last_Word = 'neun'
                            elif Last_Word == 10:
                                Last_Word = 'zehn'
                            elif Last_Word == 11:
                                Last_Word = 'elf'
                            elif Last_Word == 12:
                                Last_Word = 'zwoelf'
                            elif Last_Word == 'ES':
                                Last_Word = 'es'
                            elif Last_Word == 'IST':
                                Last_Word = 'ist'
                            elif Last_Word == 'GENAU':
                                Last_Word = 'genau'
                            elif Last_Word == 'FUENF':
                                Last_Word = 'fuenf'
                            elif Last_Word == 'ZEHN':
                                Last_Word = 'zehn'
                            elif Last_Word == 'HALB':
                                Last_Word = 'halb'
                            elif Last_Word == 'KURZ':
                                Last_Word = 'kurz'
                            elif Last_Word == 'ZWANZIG':
                                Last_Word = 'zwanzig'
                            elif Last_Word == 'VIERTEL':
                                Last_Word = 'viertel'
                            elif Last_Word == 'MINUTEN':
                                Last_Word = 'minuten'
                            elif Last_Word == 'VOR':
                                Last_Word = 'vor'
                            elif Last_Word == 'NACH':
                                Last_Word = 'nach'
                            wp.play(Last_Word + ".wav", loop=False)
            elif time_or_scp == "scp":
                time_or_scp = None
                if wp.isplaying():
                    wp.stop()
                else:
                    if SCP_WAV != None:
                        random.choice(SCP_WAV)
                        wp.play(SCP_WAV[SCP_WAV_last], loop=False)
                        SCP_WAV_last += 1
                        if SCP_WAV_last == len(SCP_WAV):
                            SCP_WAV_last = 0
            else:
                pass


print('start')
asyncio.run(main())
print('ende')

