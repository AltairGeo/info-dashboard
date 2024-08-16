import os
import json

try:
    config_path = os.path.join(os.environ['HOME'], '.config/dashserver.json')
    print(f'PATH TO CONFIG: {config_path}')
    with open(config_path) as f:
        confi = json.load(f)
    PASSWORD = confi['password'].encode('utf-8') 
    IP = str(confi['ip'])
    PORT = int(confi['port']) 
    print("Succefully load config file!")


except:
    try:
        config_path = 'C:/Program Files/dashserver.json'
        print(f'PATH TO CONFIG: {config_path}')
        with open(config_path) as f:
            confi = json.load(f)
        PASSWORD = confi['password'].encode('utf-8') 
        IP = str(confi['ip'])
        PORT = int(confi['port']) 
        print("Succefully load config file!")


    except:
        print("NON CONFIG FILE!\n PLEASE CREATE A CONFIG FILE IN $HOME/.config/dashserver.json")
        print('EXAMPLE:\n{\n    ip: "",\n    port: 1419,\n    password: "your password here"\n} ')
        PASSWORD = b"password"
        IP = ""
        PORT = 1419
        print("Get standart settings!")
        print("ip = any\nport = 1419\npassword = password")
    

