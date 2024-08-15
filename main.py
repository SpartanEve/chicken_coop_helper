from machine import ADC, Pin, I2C
import utime
import time 
from libs.dht import DHT11, InvalidPulseCount
import server
import feeds

# Sensors and LED initilized
photoresistor = ADC(28) # Photoresistor, senses the lightness/brightness
pin = Pin(16, Pin.IN, Pin.PULL_UP) # Temp and humidity sensor
sensor = DHT11(pin)
led1 = Pin(1, Pin.OUT) # LED light

lightness = 10000

time.sleep(5) # initial delay

def check_time():
    localTime = time.localtime()
    curr_hour = localTime[3]
    morning = 8
    evening = 20
    print('Current time: ', curr_hour)
    
    if (curr_hour >= morning) and (curr_hour <= evening):
        return 'day'
    return 'night'

def change_LED(light_state):
    day_night = check_time()
    # Changing LED depending on the time and if it's ligth outside or not
    if light_state >= lightness and day_night == 'day':
        led1.value(1) # Starting light if it'd daytime and it's still dark
    elif light_state >= lightness and day_night == 'night':
        led1.value(0) # Stop light if it's dark and night time
    elif light_state <= lightness and day_night == 'day':
        led1.value(0) # Stop light if it's light and day time
    elif light_state <= lightness and day_night == 'night':
        led1.value(0) # Stop light if it's light and night time
    
    # Alternatively could just write
    # else: led1.value(0)
    
    

# Program starts here
# Getting connection
ip = server.connect()

# Creating a client
mqtt_client = server.client()

if mqtt_client is not None:
    # Connect client
    mqtt_client.connect()
    try:
        while True:
            try:
                # Measures light
                light_value  = photoresistor.read_u16()
                print('Light value: ', light_value)
                mqtt_client.publish(feeds.lightness, str(light_value).encode())
            except InvalidPulseCount as e:
                print('Bad pulse count - retrying ...')
                utime.sleep(4)
            
            # Measures humidity and temperature
            sensor.measure()
            mqtt_client.publish(feeds.temperature, str(sensor.temperature).encode())
            mqtt_client.publish(feeds.humidity, str(sensor.humidity).encode())
            string = "Temperature: {}\nHumidity: {}".format(sensor.temperature, sensor.humidity)
            print(string)
            change_LED(light_value)
            utime.sleep(10)
            # sleep set to 10 for tersting purposes, when used in the chicken coop sleep will be set to 60 minutes since it doesn't need to be as precise

    except Exception as e:
        print(f'Failed to publish message: {e}')
    finally:
        mqtt_client.disconnect()
else:
    print("Failed to create MQTT client. Exiting...")