"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to list all the resources available in the current
setup and check which ones correspond to the correct external lab equipment
(or also called instruments).


Last update: 11 August 2023
"""

import pyvisa
from pylablib.devices import Thorlabs


def find_available_visa_instruments(show_instruments_response: bool = False) \
        -> list:
    """ Finds  all the available instruments connected to the local machine.

    Keep in mind that only instruments that can  communicate through the visa
    protocol are shown.

    Args:
        show_instruments_response: Boolean representing whether to show the
            instruments resource and their response to the '*idn?' query.

    Returns:
        List of all the available resources representing instruments
        communicating through visa.
    """
    # list of resources representing available instruments
    available_instruments = []

    # go through all available resources and print their identity
    for resource in pyvisa.ResourceManager().list_resources():
        # try to open each resource and send a query message for identification
        try:
            instrument = pyvisa.ResourceManager().open_resource(resource)
            identity = instrument.query('*IDN?')
            if show_instruments_response:
                print('Resource:', resource, ' corresponds to instrument: ',
                      identity)
            available_instruments.append(resource)

        except Exception as ex:
            if show_instruments_response:
                print('Resource: ', resource, ' is not an instrument or the '
                      'local machine is not able to connect to it.')
                print('ERROR RETURNED:', ex)
                # leave a blank line after printing the error
                print()

    # return the available instruments found
    return available_instruments


def find_available_bk_precision_4063_b() -> list:
    """ Finds all the available BK Precision 4063B instruments available.

    Returns:
        List of the resources representing available BK Precision 4063B
        instruments.
    """
    # all the BK 4063B instruments found
    available_bk_precision_4063_b = []

    # check which available instruments are BK 4063B
    for resource in find_available_visa_instruments():
        instrument = pyvisa.ResourceManager().open_resource(resource)
        identity_split = instrument.query('*IDN?').split(',')
        if identity_split[0] == 'BK' and identity_split[1] == '4063B':
            available_bk_precision_4063_b.append(resource)

    # return the available resources corresponding to BK 4063B instruments
    return available_bk_precision_4063_b


def find_available_kdc_101() -> list:
    """  Finds all the available ThorLabs KDC101 Brushed Motor Controllers.

    Returns: List of all the serial numbers of ThorLabs KDC101 Brushed Motor
    Controllers found connected to the local machine.
    """
    # find all available kinesis devices
    kinesis_devices = Thorlabs.list_kinesis_devices()

    # empty list to add all the serial numbers for the kdc 101 Motors found
    kdc_101_serial_numbers = []

    # check which one are KDC 101 Motors
    for device in kinesis_devices:
        if device[1] == 'Brushed Motor Controller':
            kdc_101_serial_numbers.append(device[0])

    # return the serials number found
    return kdc_101_serial_numbers


if __name__ == '__main__':
    find_available_visa_instruments(show_instruments_response=True)
    print(find_available_bk_precision_4063_b())
    print(find_available_kdc_101())
