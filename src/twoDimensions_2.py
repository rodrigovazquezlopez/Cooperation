import datetime
import logging
from os import fdopen
import random
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
dat = datetime.datetime.now()
directory = "./data/twoDim/"
filenameDron = directory + dat.strftime("VueloTwoDim_%d%b%Y_%H.%M_log") + ".txt"
filenameMoves = directory + dat.strftime("MovesTwoDim_%d%b%Y_%H.%M_log") + ".txt"

# list to save dron logging positions
dronPositions = []
counterPositions = []

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


# Dron log callback
def log_stab_callback(timestamp, data, logconf):
    global dronPositions
    # print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    position = (timestamp, data["stateEstimate.x"], data["stateEstimate.y"], data["stateEstimate.z"], data["acc.x"], data["acc.y"])
    dronPositions.append(position)


# Main thread
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    #dronFile = open(filenameDron, 'w')
    #movesFile = open(filenameMoves, 'w')
    with SyncCrazyflie(uriDron, cf=Crazyflie(rw_cache='./cache2')) as scf2:
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        lg_stab.add_variable('acc.x', 'float')
        lg_stab.add_variable('acc.y', 'float')
        scf2.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        with PositionHlCommander(scf2, default_height=0.4, controller=PositionHlCommander.CONTROLLER_PID) as pc:            
            x = 0.0
            y = 0.0
            z = 0.4
            # go to start (0, 0, 0.5)
            pc.go_to(0, 0, 0.4)
            time.sleep(2)
            cntXplus = 0
            cntXminus = 0
            cntYplus = 0
            cntYminus = 0
            move = 'L'
            for i in range(50):
                r = random.randint(0, 1)
                random.seed()
                if r == 0:
                    print("Moviendo x+")
                    moveX = 'x+'
                    cntXplus += 1
                    x += 0.1
                else:
                    print("Moviendo x-")
                    moveX = 'x-'
                    cntXminus += 1
                    x -= 0.1
                
                r = random.randint(0, 1)
                random.seed()
                if r == 0: 
                    print("Moviendo y+")
                    moveY = 'y+'
                    cntYplus += 1
                    y += 0.1
                else:
                    print("Moviendo y-")
                    moveY = 'y-'
                    cntYminus += 1
                    y -= 0.1
                # t = datetime.datetime.now()
                totalmoves = (i, x, y, z, moveX, moveY, cntXplus, cntXminus, cntYplus, cntYminus)
                counterPositions.append(totalmoves)
                pc.go_to(x, y, z)
                time.sleep(1)

            lg_stab.stop()
            with open(filenameDron, 'w') as f:
                for elem in dronPositions:
                    text = "{}, {}, {}, {}, {}, {}\n".format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5])
                    f.write(text)
                    
            with open(filenameMoves, 'w') as f:
                for elem in counterPositions:
                    text = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9])
                    f.write(text)

        

    print('Main thread ends')