"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to create a high level Client class for the
BK Precision 4063B that can handle communication between the external
hardware and the local machine.

See the end of the file for a code example.


Last updated by Daniel-Iosif Trubacs on 9 August 2023.
"""

import pyvisa


class BKCom:
    """ High level client class to provide communications between the local
    machine and the BK Precision 4063B equipment. Please see
    https://www.bkprecision.com/products/signal-generators/4063B for more
    information about the specifics of this BNC.

    This Client class can ONLY handle communications through USB via pyvisa.
    For more information about this please check pyvisa documentation and
    coms.find_resources. For a full documentation about all the serial
    commands that can be used to control the BNC please check the
    BK_4060B_Series Programming Manual (freely available online).

    Attributes:
        resource: String representing the resource (as found by pyvisa)
            corresponding to the BK 4063 BNC.
        instrument: pyvisa resource object to write commands and read data
            from the BK 4063B BNC (see pyvisa.resources.resource for more
            information).
    """

    def __init__(self, resource: str) -> None:
        self.resource = resource
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)

    def set_channel_mode(self, channel: str = 'C1', mode: str = 'ON',
                         load: int = 75, polarisation: str = 'NOR',
                         query_mode: bool = False) -> None:
        """ Sets the mode of a specific channel.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            mode: String representing whether the channel is enabled (ON) or
                disabled (OFF) to send output signals
            load: Load (measured in Ohms).
            polarisation: Polarisation of the output signal (normal 'NOR' or
                inverted 'INVT').
            query_mode: Boolean representing whether you want to query the
                instrument after the command sent and print the response
                (used only for debugging).
        """
        # send the serial command to enable CH1
        self.instrument.write(f'{channel}:OUTP {mode},LOAD,{load},PLRT,'
                              f'{polarisation}')

        # query the instrument if necessary
        if query_mode:
            print(self.instrument.query(f'{channel}:OUTP?'))

    def send_waveform(self, channel: str = 'C1', waveform_type: str = 'SINE',
                      waveform_frequency: float = 1000,
                      waveform_offset: float = 0,
                      waveform_amplitude: float = 5,
                      waveform_max_amplitude: float = 5,
                      query_mode: bool = False) -> None:
        """ Sends a specific waveform to one channel.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            waveform_type: The type of waveform used (SINE, SQUARE, RAMP, etc.)
            waveform_frequency: The frequency of the waveform (in Hz).
            waveform_offset: The offset of the waveform send (in V).
            waveform_amplitude: The amplitude of the waveform (in V).
            waveform_max_amplitude: The maximum amplitude the waveform can
                have (in V).
            query_mode: Boolean representing whether you want to query the
                instrument after the command sent and print the response
                (used only for debugging).
        """
        # send the serial command to send a specific waveform
        self.instrument.write(
            f'{channel}:BaSic_WaVe WVTP,{waveform_type},FRQ,'
            f'{waveform_frequency}HZ,AMP,{waveform_amplitude}V,'
            f'OFST,{waveform_offset}V,MAX_OUTPUT_AMP,'
            f'{waveform_max_amplitude}V')

        # query the instrument if necessary
        if query_mode:
            print(self.instrument.query(f'{channel}:BaSic_WaVe?'))

    def set_digital_modulation(self, channel: str = 'C1',
                               modulation_mode: str = 'ON',
                               modulation_type: str = 'AM',
                               modulation_wave_shape: str = 'SINE',
                               modulation_source: str = 'INT',
                               modulation_frequency: float = 100,
                               modulation_depth: float = 100,
                               modulation_deviation: float = 180,
                               modulation_amplitude: float = 1,
                               query_mode: bool = False) -> None:
        """ Sets the digital modulation for a specific channel.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            modulation_mode: Enable (mode 'ON') or disable (mode 'OFF') the
                modulation for the given channel.
            modulation_type: The modulation type ('AM', 'PM', 'PWM', etc.).
            modulation_wave_shape: The shape of the modulating waveform
                ('SINE', 'UPRAMP', etc.).
            modulation_source: The source for the modulation signal (internal
                'INT' or external 'EXT').
            modulation_frequency: Frequency of the modulating signal (measured
                in Hz)
            modulation_depth: Depth of the amplitude modulation signal
                (0-120%).
            modulation_deviation: Deviation of the modulating signal
                (0-360 degrees).
            modulation_amplitude: Amplitude of the modulation (in V).
            query_mode: Boolean representing whether you want to query the
                instrument after the command sent and print the response
                (used only for debugging).
        """
        # set the modulation mode
        self.instrument.write(f'{channel}:MDWV STATE,{modulation_mode}')

        # set the parameters for the modulation signal
        self.instrument.write(f'{channel}:MDWV {modulation_type},MDSP,'
                              f'{modulation_wave_shape},SRC,'
                              f'{modulation_source},FRQ,{modulation_frequency}'
                              f',AMP,{modulation_amplitude}V'
                              f'HZ,DEPTH,{modulation_depth},DEVI,'
                              f'{modulation_deviation}')

        # query the instrument if necessary
        if query_mode:
            print(self.instrument.query(f'{channel}:MDWV?'))


if __name__ == '__main__':
    # used only for debugging and testing
    debug_bk_com = BKCom(resource='USB0::0xF4EC::0xEE38::574B21101::INSTR')

    # set CH2 to analog (constant signal)
    debug_bk_com.set_channel_mode(channel='C2', mode='OFF')

    # set the waveform to DC
    debug_bk_com.send_waveform(channel='C2', waveform_type='DC',
                               waveform_amplitude=1,
                               waveform_offset=0.25,
                               waveform_max_amplitude=1,
                               query_mode=True)

    # enable CH1 to send output signals
    debug_bk_com.set_channel_mode(channel='C1',
                                  mode='OFF', load=75, query_mode=True)

    # set the waveform to be square
    debug_bk_com.send_waveform(channel='C1',
                               waveform_type='PULSE', waveform_amplitude=1,
                               waveform_offset=0.1,
                               waveform_max_amplitude=1,
                               query_mode=True)

    # set the modulation mode
    debug_bk_com.set_digital_modulation(channel='C1',
                                        modulation_mode='OFF',
                                        modulation_frequency=100,
                                        modulation_wave_shape='SQUARE',
                                        modulation_amplitude=1.1,
                                        query_mode=True)
    

