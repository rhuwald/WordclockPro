import json
import machine
import os
from phew import access_point, server, dns, logging
from phew.template import render_template
from os import stat

capito_SSID   = "WORDCLOCK"
capito_DOMAIN = "WORDCLOCK"
capito_HTDOCS = "htdocs"

@server.route("/hotspot-detect.html", methods=["GET"])
@server.route("/generate_204", methods=["GET"])
@server.route("/redirect", methods=["GET"])
def hotspot(request):
    return server.redirect(f"http://{capito_DOMAIN}/", 302)

@server.route("/ncsi.txt", methods=["GET"])
@server.route("/connecttest.txt", methods=["GET"])
def hotspot(request):
    return "", 200

@server.route("/", methods=['GET'])
def index(request):
    return render_template(capito_HTDOCS + "/index.html")
    
@server.route("/reset", methods=['GET'])
def index(request):
    ap_stop()
    # logging.info("> Stoppe accesspoint")
    # server.stop()
    # server.close()

@server.route("/setwlan", methods=['GET'])
def index(request):
    ssid     = request.query.get("ssid")
    password = request.query.get("password")
    api_key  = request.query.get("apikey")
    
    save_config(ssid, password, api_key)
    
    return render_template(capito_HTDOCS + "/ok.html")

@server.catchall()
def catch_all(request):
    try:
        stat(capito_HTDOCS + request.path)
        return render_template(capito_HTDOCS + request.path)
    except OSError:
        return "Not found: -" + request.path + "-", 404

def ap_start():
    # print(logging.LOG_ALL)
    # logging.disable_logging_types(logging.LOG_ALL)
    
    # print('START')
    logging.info("> Starte accesspoint, SSID {}".format(capito_SSID))
    ap = access_point(capito_SSID)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)
    # print('STARTED')
    server.run()


def ap_stop():
    logging.info("> Stoppe accesspoint")
    server.stop()
    server.close()


def delete_config():
    config_file = 'wordclock.conf'
    
    try:
        os.remove(config_file)
        return True
    except:
        return False


def load_config():
    config_file = 'wordclock.conf'
    
    try:
        stat(config_file)
    except OSError:
        file = open(config_file, 'w')
        config = {
            'ssid'    : '',
            'password': '',
            'apikey'  : ''
        }
        file.write(json.dumps(config))
        file.close()
        
    file = open(config_file, 'R')
    config = json.loads(file.read())
    # print(config)
    file.close()
    SSID = config['ssid']
    PASSWORD = config['password']
    API_KEY = config['apikey']
    # print('load_config()...')
    # print(f'ssid    : {SSID}')
    # print(f'password: {PASSWORD}')
    # print(f'api_key : {API_KEY}\n')
    
    return SSID, PASSWORD, API_KEY
    
    
def save_config(ssid, password, api_key):
    config_file = 'wordclock.conf'
    
    file = open(config_file, 'W')
    config = {
        'ssid'    : ssid,
        'password': password,
        'apikey'  : api_key
    }
    file.write(json.dumps(config))
    file.close()
