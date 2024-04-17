import datetime, time
import base64

def channel_id():
    return str(5) # set

def server_id():
    return str(1) # set

def req_id():
    return str(0) # default

def req_time():
    d = datetime.datetime.now()
    date = d.strftime('%Y-%m-%d') 
    time = d.strftime('%X.%f')
    t = date + 'T' + time + 'Z'
    return t
  
def req_image(entry):
    img = open(entry, 'rb')
    base64_string = base64.b64encode(img.read())
    return str(base64_string)[2:-1]
