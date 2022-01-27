import logging
from os import fdopen
from socket import close
import time
import math
import threading
import concurrent.futures
import queue
import paho.mqtt.client as mqtt

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uriTag = 'radio://0/80/2M/E7E7E7E7E7' # 01
uriDron  = 'radio://0/80/2M/E7E7E7E7E8' # 02
# LEGO trajectory
trajectoryCommand = "5, 500, 500" # velocity, radious, arc length
# Filenames
filenameTag = "trayectoriaENE11_log.txt"
filenameDron = "vueloENE11_log.txt"
filenameQueue = "queueENE11_content.txt"
# LEGO EV3 IP
ip_address = "10.0.1.20"
# flag to kwnow when LEGO ends trajectory
is_finished = False
# list to save dron logging positions
dronPositions = []

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# MQTT 'on connect' callback
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker! "+str(rc))
    client.subscribe("topic/finish")

# MQTT 'on message' callback
def on_message(client, userdata, msg):
    global is_finished
    print(msg.payload.decode())
    if (msg.payload.decode() == 'Finish'):
        is_finished = True

# MQTT 'on disconnect' callback
def on_disconnect(client, userdata,rc=0):
    logging.debug("Disconnected result code "+str(rc))
    client.loop_stop()

# Dron log callback
def log_stab_callback(timestamp, data, logconf):
    global dronPositions
    # print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    position = (data["stateEstimate.x"], data["stateEstimate.y"], data["stateEstimate.z"])
    dronPositions.append(position)

# Producer (vehicle Tag)
def producer(queue):
    fileTag = open(filenameTag, 'w')
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stateEstimate.x', 'float')
    lg_stab.add_variable('stateEstimate.y', 'float')
    lg_stab.add_variable('stateEstimate.z', 'float')
    cnt = 0

    with SyncCrazyflie(uriTag, cf=Crazyflie(rw_cache='./cache')) as scf:
        with SyncLogger(scf, lg_stab) as logger:

            for log_entry in logger:
                timestamp = log_entry[0]
                data = log_entry[1]
                logconf_name = log_entry[2]

                # print('[%d][%s]: %s' % (timestamp, logconf_name, data))
                a = '%s, %s, %s\n' % (data["stateEstimate.x"], data["stateEstimate.y"], data["stateEstimate.z"])
                x = float(data["stateEstimate.x"])
                y = float(data["stateEstimate.y"])
                fileTag.write(a)
                if cnt == 15:
                    consumerPos = (x, y)
                    queue.put(consumerPos)
                    cnt = 0
                else:
                    cnt += 1

                if is_finished == True:
                    endPos = (x, y)
                    queue.put(endPos)
                    break
    fileTag.close()
    print('Productor ended')

# Consumer (NAV)
def consumer(queue):

    with SyncCrazyflie(uriDron, cf=Crazyflie(rw_cache='./cache2')) as scf2:
        fileQueue = open(filenameQueue,'w')
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        scf2.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()
        
        scf2.cf.commander.send_position_setpoint(0, 0, 0.4, 0)
        message = queue.get()
        p = [0, 0]
        q = [message[0], message[1]]
        d = math.dist(p, q)
        x = message[0]
        y = message[1]
        z = 0.5
        if d > 0.15:
            n = int(d/0.1)
            for g in range(1, n):
                x_i = x*(g/n)
                y_i = y*(g/n)
                s = '{}, {}, {}\n'.format{x_i, y_i, z}
                fileQueue.write(s)
                print('Step {}  ({}, {}, {})'.format(g, x_i, y_i, z))
                scf2.cf.commander.send_position_setpoint(x_i, y_i, z, 0)
                time.sleep(1)
        else:
            print('Dron Inital pos ({}, {}, {})'.format(x, y, z))
            scf2.cf.commander.send_position_setpoint(x, y, z, 0)
            s = '{}, {}, {}\n'.format{x, y, z}
            fileQueue.write(s)
            time.sleep(1)

        while (is_finished == False) or (not(queue.empty())):
            message = queue.get()
            x = message[0]
            y = message[1]
            z = 0.5
            s = '{}, {}, {}\n'.format(x, y, z)
            fileQueue.write(s)
            print('Move dron to ({}, {}, {})'.format(x, y, z))
            scf2.cf.commander.send_position_setpoint(x, y, z, 0)
            time.sleep(0.2)

        scf2.cf.commander.send_stop_setpoint()
        time.sleep(1)
        lg_stab.stop()
        fileQueue.close()
        with open(filenameDron, 'w') as f:
            for q in dronPositions:
                a = '{}, {}, {}\n'.format(q[0], q[1], q[2])
                f.write(q)
    print('Consumer ended')

# Main thread
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    dronFile = open(filenameDron, 'w')

    client = mqtt.Client()
    client.connect(ip_address, 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.loop_start() # MQTT loop without blocking main Thread
    client.publish("topic/test", trajectoryCommand) # start LEGO trajectory

    pipeline = queue.Queue(maxsize=0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline) # Thread 1 producer
        executor.submit(consumer, pipeline) # Thread 2 consumer

    print('Main thread ends')















