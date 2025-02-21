'''
Purpose:  This module is used to interface with the MCC 152 DAQ device.
Author:   Matthew Martin
Date:     February 14, 2025
'''

import daqhats
import time

class MCC_152:
    def __init__(self, board_address):
        self._board_address = board_address
        self.hat = self._assign_board(self._board_address)

    '''
    Scans the system for the MCC 128 board.
    System design allows for multiple MCC 128 boards to be connected to the system.
    '''
    def _assign_board(self, board_address):
        hat_list = daqhats.hat_list(filter_by_id=324)
        if not hat_list:
            raise RuntimeError('No MCC 152 boards found')

        for hat in hat_list:  # Direct iteration
            if hat.address == board_address:
                return daqhats.mcc152(hat.address)

        raise RuntimeError(f'MCC 152 board not found at address {board_address}')
    
   

if __name__ == '__main__':
    # Test the MCC_152 class and its connnection
    mcc_152_01 = MCC_152(board_address=1)

    # Drive the analog output channel (Channel 0)
    mcc_152_01.hat.a_out_write(channel=0, value=1.5)


