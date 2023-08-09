"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to control the optical switching of the ultra-low
loss phase change material Sb2Se3 experiment via a Python API. The experiment
was designed and build by Daniel Lawson. More information about the specifics
of the experiment can be found at:
https://iopscience.iop.org/article/10.1088/2040-8986/ac5ece/meta and
https://onlinelibrary.wiley.com/doi/full/10.1002/adfm.202002447.
"""
import time

from coms.thorlabs_kdc_101 import KDC101Com
from coms.bk_precision_4063_b import BKCom


class Sb2Sb3ExperimentControl:
    """ High Level class used to control the Sb2Se3 optical switching
    experiment.

    The communications between the local machine and the external hardware
    (lab equipment) is done via the BKCom and KD101Com client classes. Please
    see coms.bk_precision_4063_b and coms.thorlabs_kdc_101 for more
    information.

    Attributes:
        bk_4063b_address: String representing the address (visa resource) of
            the BK Precision 4063B BNC.
        x_kdc101_address: String representing the address (serial_number) of
            the ThorLabs Kinesis KD101 used to control the x movement.
        y_kdc101_address: String representing the address (serial_number) of
            the ThorLabs Kinesis KD101 used to control the y movement.
        bnc: BKCom client object used to communicate with the physical
            instrument BK Precision 4063B BNC.
        x_motor: KD101Com client object used to communicated with the
            physical brushed motor ThorLabs Kinesis KD101 used to control the
            x movement.
        y_motor: KD101Com client object used to communicated with the
            physical brushed motor ThorLabs Kinesis KD101 used to control the
            y movement.
    """
    def __init__(self, bk_4063b_address: str = None,
                 x_kdc101_address: str = None,
                 y_kdc101_address: str = None) -> None:

        self.bk_4063b_address = bk_4063b_address
        self.x_kdc101_address = x_kdc101_address
        self.y_kdc101_address = y_kdc101_address

        # automatically search for the available instruments
        if bk_4063b_address is None:
            pass
        if x_kdc101_address is None:
            pass
        if y_kdc101_address is None:
            pass

        # else set up the connection manually
        else:
            self.bnc = BKCom(self.bk_4063b_address)
            self.x_motor = KDC101Com(self.x_kdc101_address)
            self.y_motor = KDC101Com(self.y_kdc101_address)

    def _send_digital_modulation_pump(self, **kwargs) -> None:
        """ Sends digital modulation to the pump.

        The digital modulation should always be connected to C1 of the BNC.

        Args:
            **kwargs: Other arguments given to coms.BKCom.send_waveform
            and coms.BKCom.set_digital_modulation methods.
        """
        # open the C1 port
        self.bnc.set_channel_mode(channel='C1', mode='ON', **kwargs)

        # send a normal sinusoidal wave
        self.bnc.send_waveform(channel='C1', waveform_type='PULSE', **kwargs)

        # digitally modulate the signal
        self.bnc.set_digital_modulation(channel='C1', modulation_type='PWM',
                                        **kwargs)

    def _send_analog_modulation_pump(self, **kwargs) -> None:
        """ Sends analog modulation to the pump.

        The digital modulation should always be connected to C2 of the BNC.

        Args:
            **kwargs: Other arguments given to coms.BKCom.send_waveform
            and coms.BKCom.set_digital_modulation methods.
        """
        # open the C2 port
        self.bnc.set_channel_mode(channel='C2', mode='ON', **kwargs)

        # send a normal sinusoidal wave
        self.bnc.send_waveform(channel='C2', waveform_type='SINE', **kwargs)

        # digitally modulate the signal
        self.bnc.set_digital_modulation(channel='C2', modulation_type='AM',
                                        **kwargs)

    def calibrate(self) -> None:
        """ Calibrate the experiment.

        Always Check that everything is set in place before running the
        experiment. Please read the printing messages and check that all
        pieces of equipment have received the right commands.
        """
        # move both motors to position 0 (corresponding to [0,0] in xy
        # coordinates
        self.x_motor.move_to_position(position=0)
        self.y_motor.move_to_position(position=0)

        # check that both motors are at position 0
        print('The x-motor is at position: ',
              self.x_motor.get_current_position())
        print('The y-motor is at position: ',
              self.x_motor.get_current_position())

        # try to send analog modulation to the pump
        self._send_analog_modulation_pump(query_mode=True)

        # try to send digital modulation to the pump
        self._send_digital_modulation_pump(query_mode=True)


if __name__ == '__main__':
    # used only for testing and debugging
    debug_experiment_control = Sb2Sb3ExperimentControl(
        bk_4063b_address='USB0::0xF4EC::0xEE38::574B21101::INSTR',
        x_kdc101_address='27005180',
        y_kdc101_address='27005183'
        )
    debug_experiment_control.calibrate()
