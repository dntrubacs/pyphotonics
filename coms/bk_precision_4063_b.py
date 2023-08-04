"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to create a high level Client class for the
BK Precision 4063B that can handle communication between the external
hardware and the local machine.

Code examples:


Last updated by Daniel-Iosif Trubacs on 4 August 2023.
"""

import pyvisa


class BKCom:
    """ High level client class to provide communications between the local
    machine and the BK Precision 4063B equipment. Please see
    https://www.bkprecision.com/products/signal-generators/4063B for more
    information about the specifics of this BNC.

    This Client class can ONLY handle communications through USB via pyvisa.
    For more information about this please check pyvisa documentation and
    coms.find_resources.

    Attributes:
        resource: String representing the resource (as found by pyvisa)
            corresponding to the BK 4063 BNC.
        instrument: pyvisa resource object to write commands and read data
            the BK BNC (see pyvisa.resources.resource for more information).
    """
    def __init__(self, resource: str) -> None:
        self.resource = resource
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)


if __name__ == '__main__':
    # used only for debugging and testing
    debug_bk_com = BKCom(resource='USB0::0xF4EC::0xEE38::574B21101::INSTR')
