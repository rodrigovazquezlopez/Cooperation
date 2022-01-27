#!/usr/bin/env python3

from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_C, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire
from time import sleep
import sys
import math
import paho.mqtt.client as mqtt

STUD_MM = 8
k0=11.5
alpha=90
rd=5
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_C, EV3Tire, k0 * STUD_MM)

gy = GyroSensor(INPUT_2)
sleep(0.5)
gy.calibrate
gy.reset

ip_address = "192.168.1.149" # IP del broker con mosquitto (raspberry o EV3)

def arco():
    mdiff.on_arc_right(rd,750,4550) #120 cm 550 y 3350 - 64 300 y 2000 - 169+7

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker! "+str(rc))
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    variables = message.split(",")
    speed = int(variables[0])
    radio = int(variables[1])
    distance = int(variables[2])
    print('speed: {}, radio: {}, distance: {}'.format(speed, radio, distance))

    mdiff.odometry_start(theta_degrees_start=0.0, x_pos_start=0.0, y_pos_start=0.0)
    mdiff.on_arc_right(speed, radio, distance)
    mdiff.odometry_stop()
    client.publish("topic/finish", "Finish")
    print("Trayectoria completa")
    #client.disconnect()
    
client = mqtt.Client()
client.connect(ip_address,1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()