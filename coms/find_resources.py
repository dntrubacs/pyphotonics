"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to list all the resources available in the current
setup and check which ones correspond to the correct external lab equipment
(or also called instruments).


Last updated on 9 August 2023 by Daniel-Iosif Trubacs
"""

import pyvisa
from pylablib.devices import Thorlabs


def find_available_visa_instruments() -> None:
    """ Finds and returns all the available instruments connected to the local
    machine. Keep in mind that only instruments that can  communicate through
    the visa protocol are shown.
    """
    # find all resources available
    rm = pyvisa.ResourceManager()

    # go through all available resources and print their identity
    for resource in rm.list_resources():
        # try to open each resource and send a query message for identification
        try:
            instrument = rm.open_resource(resource)
            identity = instrument.query('*IDN?')
            print('Resource:', resource, ' corresponds to instrument: ',
                  identity)
        except Exception as ex:
            print('Resource: ', resource, ' is not an instrument or the local '
                  'machine is not able to connect to it.')
            print('ERROR RETURNED:', ex)
            # leave a blank line after printing the error
            print()


def find_available_kinesis_devices() -> None:
    """ Finds all the available ThorLabs Kinesis devices. """
    print(Thorlabs.list_kinesis_devices())


if __name__ == '__main__':
    find_available_visa_instruments()
    find_available_kinesis_devices()
