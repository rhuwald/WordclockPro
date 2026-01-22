import machine
import urequests

# RTC stellen
def set(api_key = None):
    
    try:
        print(f"Verbinde zu api.timezonedb.com...")
        
        url = "https://api.timezonedb.com/v2.1/get-time-zone?key=" + api_key + "&format=json&by=zone&zone=Europe/Berlin"
        print(f'...api_key = {api_key}')
        print(f'...url     = {url}')
        response = urequests.get(url)
    except:
        print(f"...Verbindung konnte nicht hergestellt werden")
        return False
    
    if response.status_code != 200:
        print(f"...Http-Status {response.status_code}")
        print(f"...Http-Content {response.text}")
        return False
    
    jsonstring = response.json()
    
    response.close()
    
    datetime    = jsonstring["formatted"]
    print(f"...Uhrzeit ist {datetime}")
    
    # Wochentag wird nicht geliefert, wird vom Pico automatisch errechnet
    day_of_week = 0
    
    # Realtimeclock auslesen und neusetzen
    rtc = machine.RTC()
    rtc.datetime((
        int(datetime[0:4]),   # JJJJ
        int(datetime[5:7]),   # MM
        int(datetime[8:10]),  # TT
        int(day_of_week),     # T
        int(datetime[11:13]), # HH
        int(datetime[14:16]), # MM
        int(datetime[17:19]), # SS
        0))                   # MS
    
    return True
