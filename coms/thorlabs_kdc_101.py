"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 8 August 2023. The
purpose of this module is to create a high level Client class for the
ThorLabs Kinesis KDC 101 Brushed Motors that can handle communication
between the external hardware and the local machine. To be able to communicate
to the KDC101 through the USB Port, install the correct APT drivers:
https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1 
and update the Brushed Motor Controller Device (in Device Manage for Windows)
with the correct driver.

This code uses the pylablib library and is heavily based on their
Thorlabs.KinesisMotor class. Please check their documentation for more
information: https://pylablib.readthedocs.io/en/latest/devices/Thorlabs_kinesis.html

See the end of the file for a code example.


Last update: 11 August 2023.
"""  # noqa
import time

from pylablib.devices import Thorlabs
from coms.find_resources import find_available_kdc_101


class KDC101Com:
    """ High level client class to provide communications between the local
    machine and the KD101 Brushed Motor Controller. Please see
    https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2419 for more
    information about the specifics of this product.

    This Client class can ONLY handle communications through USB via pylablib
    (which uses pyserial in their backend). To move the motor, simply use
    the move_to_position method. Keep in mind that the values are coming
    from the internal setup of the motor (they can be accessed via the
    self.distance_unit attribute).

    Attributes:
        serial_number: String representing the serial number written on the
            back of the motor. If None is given, the first available found by
            the coms.find_resources.find_available_kdc_101 function will be
            used.
        motor: Thorlabs.KinesisMotor object used to control the physical
            KDC101 motor.
        distance_unit: Integer representing the units corresponding to the
            real physical distance the motor has moved (in this case,
            1 distance_unit corresponds to 0.05 mm).
    """
    def __init__(self, serial_number: str = None) -> None:
        # search for the available KDC101 motors available if None is given
        if serial_number is None:
            self.serial_number = find_available_kdc_101()[0]
        # else, use the serial_number provided
        else:
            self.serial_number = serial_number

        self.motor = Thorlabs.KinesisMotor(self.serial_number)

        # get the distance units from the internal setup of the motor
        self.distance_unit = (
            self.motor.get_gen_move_parameters().__getitem__(0))

    def get_current_position(self) -> float:
        """ Gets the current position (measured in mm) of the motors."""
        return self.motor.get_position()/(self.distance_unit*20)

    def move_to_position(self, position: float) -> None:
        """ Moves the motor to a certain position.

        Args:
            position: The position at which the motor will move (measured in
                mm). Keep in mind that the position will always be relative to
                the 0 position of the motor.
        """
        # move the motor to the specific position
        self.motor.move_to(position*self.distance_unit*20)

        # wait until the motor stopped moving
        while self.motor.is_moving():
            time.sleep(0.1)


if __name__ == '__main__':
    # used only for debugging and testing
    debug_kdc_101 = KDC101Com()
    print(debug_kdc_101.serial_number)

    # move the motor
    debug_kdc_101.move_to_position(position=0)

    # get the current position
    print(debug_kdc_101.get_current_position())
