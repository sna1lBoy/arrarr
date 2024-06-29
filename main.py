# initialize web app
from flask import Flask; from waitress import serve; import configparser, socket
app = Flask(__name__)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localhost = s.getsockname()[0]

# try to open config
config = configparser.ConfigParser(interpolation = None)
config.read("./files/config.ini")

# extract app info
try:
    port = config.get("arrarr", "port")
except:
    port = ""
try:
    address = config.get("arrarr", "address")
except:
    address = ""

# revert to defaults if no given value
if port == "":
    port = "9999"
if address == "":
    address = "http://localhost"

# serving main page
@app.route("/")
def index():

    # read in html in a totally normal and sane pythonic way
    file = open("./files/index.html", "r")
    html = "".join(file.readlines())

    # modify appearance based on config
    try:
        html = html.replace("background-color: black", "background-color: " + config.get("arrarr", "background color"))
    except:
        pass
    try:
        html = html.replace("url()", "url(" + config.get("arrarr", "background image") + ")")
    except:
        pass

    # fill in all the given config information, or fill in defaults if none
    for arr in [["sonarr", "8989", "https://avatars.githubusercontent.com/u/1082903?s=280&v=4"], ["radarr", "7878", "https://avatars.githubusercontent.com/u/25025331?s=280&v=4"], ["lidarr", "8686", "https://avatars.githubusercontent.com/u/28475832?s=280&v=4"], ["readarr", "8787", "https://avatars.githubusercontent.com/u/57576474?s=280&v=4"], ["prowlarr", "9696", "https://avatars.githubusercontent.com/u/73049443?v=4"]]:
        try:
            if config.get(arr[0], "hidden") == "yes":
                html=html.replace("<a href=\"" + arr[0], "<a hidden href=\"" + arr[0])
        except:
            pass
        try:
            html = html.replace(arr[0] + " address", config.get(arr[0], "address").replace("localhost", localhost).replace("0.0.0.0", localhost))
        except:
            html = html.replace(arr[0] + " address", "http://" + localhost)
        try:
            html = html.replace(arr[0] + " port", config.get(arr[0], "port"))
        except:
            html = html.replace(arr[0] + " port", arr[1])
        try:
            html = html.replace(arr[0] + " icon", config.get(arr[0], "icon"))
        except:
            html = html.replace(arr[0] + " icon", arr[2])

    # give flask the modified html
    return html

serve(app, host = address, port = port)