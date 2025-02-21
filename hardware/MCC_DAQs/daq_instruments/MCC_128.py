'''
Purpose:  This module is used to interface with the MCC 128 DAQ device.
Author:   Matthew Martin
Date:     February 14, 2025
'''

import daqhats
import time

class MCC_128:
    def __init__(self, board_address):
        self._board_address = board_address
        self.hat = self._assign_board(self._board_address)

    '''
    Scans the system for the MCC 128 board.
    System design allows for multiple MCC 128 boards to be connected to the system.
    '''
    def _assign_board(self, board_address):
        hat_list = daqhats.hat_list(filter_by_id=326)
        if not hat_list:
            raise RuntimeError('No MCC 128 boards found')

        for hat in hat_list:  # Direct iteration
            if hat.address == board_address:
                return daqhats.mcc128(hat.address)

        raise RuntimeError(f'MCC 128 board not found at address {board_address}')
    
   

if __name__ == '__main__':
    # Test the MCC_128 class and its connnection
    mcc_128_01 = MCC_128(board_address=0)
    mcc_128_01.hat.blink_led(0)

    # Configure the analog input channels (Single ended, 5V range)
    mcc_128_01.hat.a_in_mode_write(0)
    mcc_128_01.hat.a_in_range_write(1)
    print(mcc_128_01.hat.a_in_mode_read())

    # Start a hardware pace scan
    mcc_128_01.hat.a_in_scan_start(0x01, 10000, 1000, 16)
    time.sleep(0.5)
    print(mcc_128_01.hat.a_in_scan_read(-1, -1))
    print('Pausing scan for 1 seconds...')
    time.sleep(1)
    print(mcc_128_01.hat.a_in_scan_read(-1, -1))
    
    

    # Shut down the MCC 128 board
    time.sleep(1)
    mcc_128_01.hat.blink_led(1)
