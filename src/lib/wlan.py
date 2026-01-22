import network
import time

class WLAN:
    def __init__(self, verbose_mode = False):
        self.wlan = network.WLAN(network.STA_IF)
        
        self.connected = False
        
        self.status = network.STAT_IDLE
        self.status_text = {}
        self.status_text[network.STAT_IDLE]           = 'Keine Verbingung, keine Aktivität'
        self.status_text[network.STAT_CONNECTING]     = 'Verbinde'
        self.status_text[network.STAT_WRONG_PASSWORD] = 'Fehler, falsches Passwort'
        self.status_text[network.STAT_NO_AP_FOUND]    = 'Fehler, Accesspoint antwortet nicht'
        self.status_text[network.STAT_CONNECT_FAIL]   = 'Fehler, unbekanntes Problem'
        self.status_text[network.STAT_GOT_IP]         = 'Verbindung erfolgreich'
        
        self.ip      = None
        self.netmask = None
        self.dns     = None
        self.gateway = None
        
        self.ssid     = None
        self.password = None
        
        self.verbose_mode = verbose_mode
    
    
    def connect(self, ssid = None, password = None, timeout = 60):
        if (ssid == None) or (password == None):
            ssid     = self.ssid
            password = self.password
        
        self.ssid     = ssid
        self.password = password
        
        if self.verbose_mode == True:
            print(f"WLAN - Verbinde mit ssid {ssid}...")
        
        self.connected = False
        self.status    = 0
        self.wlan.active(True)                                                # WLAN aktivieren
        
        connect_ok = False
        while connect_ok == False:
            try:
                self.wlan.connect(self.ssid, self.password)                   # Verbindung zum WLAN aufbauen
                connect_ok = True
            except:
                if self.verbose_mode == True:
                    print("WLAN - Fehler bei connect()...")
                time.sleep(1)
        
        i = 0
        while self.wlan.isconnected() == False and i < timeout:
            i += 1
            self.status = self.wlan.status()
            if self.verbose_mode == True:
                try:
                    _ = self.status_text[self.status]
                except:
                    _ = self.status
                print(f"...Versuch {i} / {timeout}, Status {_}")
            time.sleep(1)
        
        if self.wlan.isconnected() == False:
            self.connected = False
            self.status    = 0
            if self.verbose_mode == True:
                print("WLAN - Verbindung ist fehlgeschlagen")
            return False
        
        self.connected = True
        self.status    = self.wlan.status()
        
        ifconfig     = self.wlan.ifconfig()
        self.ip      = ifconfig[0]
        self.netmask = ifconfig[1]
        self.gateway = ifconfig[2]
        self.dns     = ifconfig[3]
        
        if self.verbose_mode == True:
            print(f"WLAN - Verbindung ist hergestellt")
            self.info()
        
        return True
    
    
    def disconnect(self):
        if self.wlan.isconnected() == True:
            self.wlan.disconnect()
        self.wlan.active(False)
        self.wlan.deinit()
        self.connected = False
        self.status = 0
        if self.verbose_mode == True:
            print(f"WLAN - Verbindung ist getrennt")
        return True
    
    
    def info(self):
        print("WLAN - Info")
        if self.connected == True:
            print(f"...IP-Adresse ist {self.ip}/{self.netmask}")
            print(f"...Gateway ist    {self.gateway}")
            print(f"...Nameserver ist {self.dns}")
        else:
            print("...Keine Verbindung")
