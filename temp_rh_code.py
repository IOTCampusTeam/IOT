from paho.mqtt import client as mqtt
import json
def on_connect(client, userdata, flags, rc):
    #connect mqtt broker
    client.subscribe([('temp', 0)])
    if rc == 0:
        print('连接成功')

def on_message(client, userdata, msg):
    # sub dht11 temperature/humidity data
    temp_rh = json.loads(str(msg.payload.decode('utf-8')))
    list_temp = temp_rh['temp']
    list_rh = temp_rh['humi']
    temp1 = list_temp
    rh1 = list_rh
    dict_wd1={}
    dict_sd1={}
    dict_wd1['temp1'] = temp1
    dict_sd1['rh1'] = rh1
    json_wd1 = json.dumps(dict_wd1)
    json_sd1 = json.dumps(dict_sd1)
    client.publish(topic='wd1', payload=json_wd1, qos=0)
    client.publish(topic='sd1', payload=json_sd1, qos=0)
    print(json_wd1)
    print(json_sd1)


def run():
    client = mqtt.Client()
    #w Edit mqtt cloud address
    client.connect('45.253.64.55', 12477, 60)
    client.username_pw_set('iot', 'iot')
    client.on_connect = on_connect
    client.on_message = on_message
    client.subscribe('temp')
    client.loop_forever()

if __name__ == '__main__':
    run()
