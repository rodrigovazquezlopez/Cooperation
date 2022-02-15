import logging
from os import fdopen
from socket import close
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uriDron  = 'radio://0/80/2M/E7E7E7E7E7' # 02

# Filenames
filenameDron = "vueloFEB8_22_log_3.txt"

# list to save dron logging positions
dronPositions = []

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


# Dron log callback
def log_stab_callback(timestamp, data, logconf):
    global dronPositions
    # print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    position = (data["stateEstimate.x"], data["stateEstimate.y"], data["stateEstimate.z"])
    dronPositions.append(position)


# Main thread
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    dronFile = open(filenameDron, 'w')
    with SyncCrazyflie(uriDron, cf=Crazyflie(rw_cache='./cache2')) as scf2:
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        scf2.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        with PositionHlCommander(scf2, default_height=0.4, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            x = 0.0
            y = 0.0
            pc.go_to(0, 0, 0.5)
            time.sleep(2)
            for i in range(0, 20):
                pc.go_to(x, 0, 0.5)
                time.sleep(2)
                x += 0.1
                print(x)

            #     y = y + 0.01

            
            
            # pc.go_to(0, 0, 0.5)
            # time.sleep(2)
            # pc.go_to(0.1, 0, 0.5)
            # time.sleep(2)
            # pc.go_to(0.1, 0.1, 0.5)
            # time.sleep(2)
            # pc.go_to(0, 0.1, 0.5)
            # time.sleep(2)
            # pc.go_to(0, 0, 0.5)
            # time.sleep(2)

        lg_stab.stop()
        with open(filenameDron, 'w') as f:
            for q in dronPositions:
                a = "{}, {}, {}\n".format(q[0], q[1], q[2])
                f.write(a)

        

    print('Main thread ends')