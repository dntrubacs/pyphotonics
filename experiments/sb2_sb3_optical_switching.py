"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to control the optical switching of the ultra-low
loss phase change material Sb2Se3 experiment via a Python API. The experiment
was designed and build by Daniel Lawson. More information about the specifics
of the experiment can be found at:
https://iopscience.iop.org/article/10.1088/2040-8986/ac5ece/meta and
https://onlinelibrary.wiley.com/doi/full/10.1002/adfm.202002447.

See the end of the file for a code example.


Last update: 14 August 2023.
"""
import time
from matplotlib import pyplot as plt

from coms.thorlabs_kdc_101 import KDC101Com
from coms.bk_precision_4063_b import BKCom
from coms.find_resources import find_available_kdc_101
from utils import get_square_pattern


class Sb2Sb3ExperimentControl:
    """ High Level class used to control the Sb2Se3 optical switching
    experiment.

    The communications between the local machine and the external hardware
    (lab equipment) is done via the BKCom and KD101Com client classes. Please
    see coms.bk_precision_4063_b and coms.thorlabs_kdc_101 for more
    information.

    If no address is given for the BK 4063B or the KDC101 motors (either one
    of them), the local machine will automatically search for the ones
    available. Keep in Mind that this is not recommended as multiple devices
    might be connected in the same time.

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

        # as there are two motors, automatically searching for the first one
        # might make the code confuse the two motors. If one of them is None
        # manually search for two different available motors.
        if x_kdc101_address is None or y_kdc101_address is None:
            self.x_kdc101_address = find_available_kdc_101()[0]
            self.y_kdc101_address = find_available_kdc_101()[1]

        # else use the user given addresses
        else:
            self.x_kdc101_address = x_kdc101_address
            self.y_kdc101_address = y_kdc101_address

        # set up the client object for connection
        self.bnc = BKCom(self.bk_4063b_address)
        self.x_motor = KDC101Com(self.x_kdc101_address)
        self.y_motor = KDC101Com(self.y_kdc101_address)

    def _write_on_pixel(self, writing_time: float = 5,
                        analog_amplitude: float = 5,
                        digital_amplitude: float = 5,
                        pulse_duration: float = 0.1,
                        **kwargs) -> None:
        """ Writes on the pixel the laser is currently at.

        The digital modulation should always be connected to C1 of the BNC and
        the analog modulation should always be connected to C2 of the BNC. The
        maximum amplitude should always be less than 5V for both channels.

        The analog modulation simply represents a constant DC output for
        C2 and the digital modulation simply represents a one shoot
        (achieved here by a combination of BURST and PULSE functions of the
        BNC).

        Args:
            writing_time: The time the laser will write on the pixel (the
                time the laser modulation is on, measured in seconds).
            analog_amplitude: Amplitude of the analog modulation (must be
                smaller than 5V).
            digital_amplitude: Amplitude of the digital modulation (must
                be smaller than 5V).
            pulse_duration: Duration of the pulse during digital modulation
                (one shoot time duration of the laser signal). Must be
                smaller than writing_time.
            **kwargs: Other arguments given to coms.BKCom client methods.
        """
        # enable the putput of both channels
        self.bnc.set_channel_mode(channel='C1', mode='ON', load='HZ', **kwargs)
        self.bnc.set_channel_mode(channel='C2', mode='ON', load='HZ', **kwargs)

        # set the analog modulation (C2 is set to send a constant DC signal)
        self.bnc.send_waveform(channel='C2', waveform_type='DC',
                               waveform_amplitude=0,
                               waveform_offset=analog_amplitude,
                               waveform_max_amplitude=10,
                               **kwargs)

        # set the digital modulation (a burst function with a PULSE signal)
        # set the PULSE signal
        self.bnc.send_waveform(channel='C1',
                               waveform_type='PULSE',
                               waveform_amplitude=digital_amplitude,
                               waveform_offset=0,
                               waveform_max_amplitude=10,
                               waveform_frequency=1,
                               waveform_width=pulse_duration,
                               **kwargs)

        # send the burst signal
        self.bnc.send_burst(channel='C1', burst_wave_carrier='PULSE',
                            burst_wave_amplitude=digital_amplitude,
                            burst_period=1.5)

        # wait for the laser to write on the pixel
        time.sleep(writing_time)

        # stop the laser modulation
        self.bnc.set_channel_mode(channel='C1', mode='OFF', load='HZ',
                                  **kwargs)
        self.bnc.set_channel_mode(channel='C2', mode='OFF', load='HZ',
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

        # enable and disable the output of both channels of the BNC
        self.bnc.set_channel_mode(channel='C1', mode='ON', query_mode=True)
        self.bnc.set_channel_mode(channel='C2', mode='ON', query_mode=True)
        time.sleep(1)
        self.bnc.set_channel_mode(channel='C1', mode='OFF', query_mode=True)
        self.bnc.set_channel_mode(channel='C2', mode='OFF', query_mode=True)

    def run_experiment(self, n_pixels: int = 3, pixel_length: float = 1.0,
                       visual_feedback: bool = False, **kwargs) -> None:
        """ Runs the main experiment.

        Args:
            n_pixels: Number of pixels on side of the square. Keep in
                mind the actual total number of pixels will be n_pixels**2.
            pixel_length: The length of a pixel (the length side of the
                pixel).
            visual_feedback: Whether a plot showing the updates of the pixel
                map to be shown.
            **kwargs: Other arguments given to coms.BKCom client methods.
        """
        # get the correct pattern for the motors to follow
        pattern = get_square_pattern(n_pixels=n_pixels,
                                     pixel_length=pixel_length)

        # past points that represent pixels were written
        past_points = []

        # go through each point in the pattern and write a pixel
        for point in pattern:
            print(f'Move the motors to position: x={point[0]}'
                  f' y={point[1]}')

            # move the motors to each point in the pattern
            self.x_motor.move_to_position(position=point[0])
            self.y_motor.move_to_position(position=point[1])

            # the real position of the motors (as read directly from the motor)
            motors_position = [self.x_motor.get_current_position(),
                               self.y_motor.get_current_position()]
            print(f'The motors are now at position: x={motors_position[0]}'
                  f' y={motors_position[1]}')

            # append the motors position
            past_points.append(motors_position)

            # write on the current pixel
            print('Start writing on the current pixel')
            self._write_on_pixel(writing_time=2.5,
                                 analog_amplitude=5,
                                 digital_amplitude=5,
                                 pulse_duration=0.001,
                                 **kwargs)
            print('The pixel has been written and the modulation has '
                  'been stopped.')

            if visual_feedback:
                # set up the figure
                plt.figure(figsize=(12, 8))
                plt.title(f'Position of the motors: '
                          f' x={round(motors_position[0], 3)},'
                          f' y={round(motors_position[0], 3)}')
                plt.xlim([0, n_pixels * pixel_length])
                plt.ylim([0, n_pixels * pixel_length])

                # show the pixel grid
                for k in range(n_pixels):
                    plt.vlines(x=k*pixel_length, ymin=0,
                               ymax=n_pixels*pixel_length, color='black')
                    plt.hlines(y=k*pixel_length, xmin=0,
                               xmax=n_pixels*pixel_length, color='black')

                # show the pixel centers and their order
                written_pixel_number = 0
                for past_point in past_points:
                    plt.plot(past_point[0], past_point[1], marker='o',
                             markersize=10, color='blue')
                    plt.text(past_point[0], past_point[1],
                             str(written_pixel_number), fontsize=20)
                    written_pixel_number += 1
                plt.show()


if __name__ == '__main__':
    # used only for testing and debugging
    debug_experiment_control = Sb2Sb3ExperimentControl()

    # calibrate the experiment
    print('>>>>>>> Starting calibration!')
    debug_experiment_control.calibrate()
    print('>>>>>>> Ending calibration!')

    # run the experiment
    debug_experiment_control.run_experiment(n_pixels=3,
                                            pixel_length=3,
                                            visual_feedback=True,
                                            query_mode=False)
