'''
Test daqhats module hardware interface
'''
import sys
import multiprocessing
import psutil
import time
import math

sys.path.append('../hardware/MCC_DAQs/daq_instruments')
from MCC_152 import MCC_152
from MCC_128 import MCC_128

# System configuration and constants
REAL_TIME_CORE = 3          # SBC Core to run the real-time process
WAVEFORM_FREQ = 25          # Frequency of the sinosoidal waveform generator
REAL_TIME_FREQ = 1000       # Frequency of the real-time process
AMP = 0.05                  # Amplitude of the sinosoidal waveform

def initialize_MCC_128():
    '''
    Initialize and configure the MCC 128 board
    '''
    mcc_128 = MCC_128(board_address=0)

def sinosoidal_generator(init_event):
    '''
    Generation of a pseudo sinosoidal waveform to be run on dedicated core
    '''
    mcc_152 = MCC_152(board_address=1)
    w = 2 * math.pi * WAVEFORM_FREQ
    GENERATOR_T_STEP = 1 / REAL_TIME_FREQ
    init_event.set()

    while True:
        for n in range(int(REAL_TIME_FREQ / WAVEFORM_FREQ)):
            v_out = AMP * math.sin(w * n * GENERATOR_T_STEP)
            mcc_152.hat.a_out_write(channel=0, value=v_out)
            time.sleep(GENERATOR_T_STEP)

def system_startup():
    '''
    Start up the enitre SBC system
    '''
    # Initialize the MCC 152 voltage signal on the dedicated SBC core
    init_event = multiprocessing.Event()
    realtime_process = multiprocessing.Process(
        target=sinosoidal_generator, 
        args=(init_event,)
    )
    realtime_process.start()
    init_event.wait()
    print('Real-time process started.')
    pid = realtime_process.pid
    p = psutil.Process(pid)
    p.cpu_affinity([REAL_TIME_CORE])  
    print(f'Real-time process pinned to core {REAL_TIME_CORE}.')

def main():
    print('Starting daq tests.')
    system_startup()

if __name__ == '__main__':
    main()