"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to create a high level Client class for the
BK Precision 4063B that can handle communication between the external
hardware and the local machine. Please see
https://www.bkprecision.com/products/signal-generators/4063B for more
information about the specifics of this BNC. For a full documentation about
all the serial commands that can be used to control the BNC please check the
BK_4060B_Series Programming Manual (freely available online).

See the end of the file for a code example.


Last update: 28 October 2023.
"""

import pyvisa
from coms.find_resources import find_available_bk_precision_4063_b
import time as time


class BKCom:
    """ High level client class to provide communications between the local
    machine and the BK Precision 4063B equipment. This Client class can ONLY
    handle communications through USB via pyvisa. For more information about
    this please check pyvisa documentation and coms.find_resources.

    This class has 3 client methods used to communicate between the local
    machine and the BNC: set_channel_mode, send_waveform and
    set_digital_modulation. To send any signal via channel the
    set_channel_mode method should always be used first to enable the channel
    to send output signals.

    Attributes:
        resource: String representing the resource (as found by pyvisa)
            corresponding to the BK 4063 BNC. If None is given, the first
            available found by the
            coms.find_resources.find_available_bk_precision_4063_b function
            will be used.
        instrument: pyvisa resource object to write commands and read data
            from the BK 4063B BNC (see pyvisa.resources.resource for more
            information).
    """

    def __init__(self, resource: str = None) -> None:
        # search for the available BK 4063B available if None is given
        if resource is None:
            self.resource = find_available_bk_precision_4063_b()[0]
        # else, use the resource provided
        else:
            self.resource = resource
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)

    def set_channel_mode(self, channel: str = 'C1', mode: str = 'ON',
                         load: int | str = 75, polarisation: str = 'NOR',
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
                      waveform_width: float = 1,
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
            waveform_width: The width the waveform can have (in s).
            query_mode: Boolean representing whether you want to query the
                instrument after the command sent and print the response
                (used only for debugging).
        """
        # send the serial command to send a specific waveform
        self.instrument.write(
            f'{channel}:BaSic_WaVe WVTP,{waveform_type},FRQ,'
            f'{waveform_frequency}HZ,AMP,{waveform_amplitude}V,'
            f'OFST,{waveform_offset}V,MAX_OUTPUT_AMP,'
            f'{waveform_max_amplitude}V,WIDTH,{waveform_width}')

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
                              f'{modulation_deviation}'
                              f'WIDTH,2')

        # query the instrument if necessary
        if query_mode:
            print(self.instrument.query(f'{channel}:MDWV?'))

    def send_burst(self, channel: str = 'C1',
                   burst_mode: str = 'ON',
                   burst_period: float = 1.0,
                   burst_source: str = 'INT',
                   burst_cycles: int = 1,
                   burst_wave_carrier: str = 'PULSE',
                   burst_wave_amplitude: float = 5,
                   burst_wave_offset: float = 0,
                   query_mode: bool = False) -> None:
        """ Sends a burst to a specific channel.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            burst_mode: Enable (mode 'ON') or disable (mode 'OFF') the
                burst mode for the given channel.
            burst_period: The period of the burst (in s).
            burst_source: The source of the burst signal (internal
                'INT' or external 'EXT').
            burst_cycles: The number of cycles for the burst function.
            burst_wave_carrier: The wave carrier for the burst signal
                ('SINE', 'PULSE', 'SQUARE', etc.).
            burst_wave_amplitude: The amplitude of the signal sent (in V).
            burst_wave_offset: The offset of the signal sent (in V).
            query_mode: Boolean representing whether you want to query the
                instrument after the command sent and print the response
                (used only for debugging).
        """
        # send the burst signal
        self.instrument.write(f'{channel}:BTWV STATE,{burst_mode},'
                              f'PRD,{burst_period},TRSR,{burst_source},'
                              f'TIME,{burst_cycles},GATE_NCYC,NCYC,CARR,WVTP,'
                              f'{burst_wave_carrier},AMP,'
                              f'{burst_wave_amplitude}V,OFST,'
                              f'{burst_wave_offset}V')

        if query_mode:
            print(self.instrument.query('C1:BTWV?'))

    def send_constant_signal(self, analog_amplitude: float = 1.0,
                             digital_amplitude: float = 5.0) -> None:
        """ Send a constant signal of given power.

        Args:
            analog_amplitude: The amplitude of the analog channel (C2 in
                this case) measured in V. Must be less than 10V.
            digital_amplitude: The amplitude of the digital channel (C1 in
                this case) measured in V. Must be less than 10V.
        """
        # set the channels mode to ON
        self.set_channel_mode(channel='C2', mode='ON', load='HZ')
        self.set_channel_mode(channel='C1', mode='ON', load='HZ')

        # set the waveform of Analog to DC and the waveform of digital to PULSE
        self.send_waveform(channel='C2', waveform_type='DC',
                           waveform_offset=analog_amplitude,
                           waveform_max_amplitude=10)
        self.send_waveform(channel='C1', waveform_type='DC',
                           waveform_offset=digital_amplitude,
                           waveform_max_amplitude=10)

        # set both channels mode to OFF
        self.set_channel_mode(channel='C1', mode='OFF', load='HZ')
        self.set_channel_mode(channel='C2', mode='OFF', load='HZ')

    def send_pulse(self, analog_amplitude: float = 1.0,
                   digital_amplitude: float = 5.0,
                   pulse_width: float = 1E4) -> None:
        """ Send a short pulse of given duration.

        Args:
            analog_amplitude: The amplitude of the analog channel (C2 in
                this case) measured in V. Must be less than 10V.
            digital_amplitude: The amplitude of the digital channel (C1 in
                this case) measured in V. Must be less than 10V
            pulse_width: Duration of the pulse (measured in s)
        """
        # set the channels mode to ON
        self.set_channel_mode(channel='C2', mode='ON', load='HZ')
        self.set_channel_mode(channel='C1', mode='ON', load='HZ')

        # set the waveform of Analog to DC and the waveform of digital to PULSE
        self.send_waveform(channel='C2', waveform_type='DC',
                           waveform_offset=analog_amplitude,
                           waveform_max_amplitude=10)
        self.send_waveform(channel='C1', waveform_type='PULSE',
                           waveform_amplitude=digital_amplitude,
                           waveform_max_amplitude=10, waveform_frequency=1,
                           waveform_width=pulse_width)

        # set the digital channel to burst mode (send only shot)
        self.send_burst(channel='C1', burst_wave_carrier='PULSE',
                        burst_wave_amplitude=5, burst_period=1.5)

        # delay for 2 seconds (enough time to send one pulse)
        time.sleep(2)

        # set both channels mode to OFF
        self.set_channel_mode(channel='C1', mode='OFF', load='HZ')
        self.set_channel_mode(channel='C2', mode='OFF', load='HZ')


if __name__ == '__main__':
    # used only for debugging and testing
    debug_bk_com = BKCom('USB0::0xF4EC::0xEE38::574B21101::INSTR')

    # send a pulse of duration 1E-4
    debug_bk_com.send_pulse(analog_amplitude=1.4, digital_amplitude=5,
                            pulse_width=1E-4)
