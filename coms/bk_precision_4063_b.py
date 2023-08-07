"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to create a high level Client class for the
BK Precision 4063B that can handle communication between the external
hardware and the local machine.

See the end of the file for a code example.


Last updated by Daniel-Iosif Trubacs on 7 August 2023.
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
            the BK BNC (see pyvisa.resources.resource for more information).
    """
    def __init__(self, resource: str) -> None:
        self.resource = resource
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)

    def set_channel_mode(self, channel: str = 'C1', mode: str = 'ON') -> None:
        """ Enables or disables a specific channel to send output signals.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            mode: String representing whether the channel is enabled (ON) or
                disabled (OFF) to send output signals
        """
        # send the serial command to enable CH1
        self.instrument.write(f'{channel}:OUTP {mode},LOAD,75,PLRT,NOR')
        # print the response of the BNC
        print(self.instrument.query('C1:OUTP?'))

    def send_waveform(self, channel: str = 'C1', waveform_type: str = 'SINE',
                      frequency: float = 10, offset: float = 0,
                      amplitude: float = 5) -> None:
        """ Sends a specific waveform to one channel.

        Args:
            channel: The channel used to send the waveform (C1 or C2).
            waveform_type: The type of waveform used (SINE, SQUARE, RAMP, etc.)
            frequency: The frequency of the waveform (in Hz).
            offset: The offset of the waveform send (in V).
            amplitude: The amplitude of the waveform (in V).
        """
        # send the serial command to send a specific waveform
        self.instrument.write(
                f'{channel}:BaSic_WaVe WVTP,{waveform_type},FRQ,{frequency}HZ,'
                f'AMP,{amplitude}V,OFST,{offset}V')

        # query the instrument
        print(self.instrument.query('C1:BaSic_WaVe?'))


if __name__ == '__main__':
    # used only for debugging and testing
    debug_bk_com = BKCom(resource='USB0::0xF4EC::0xEE38::574B21101::INSTR')
    # enable CH1 to send output signals
    debug_bk_com.set_channel_mode()
    # send a simple sine waveform
    debug_bk_com.send_waveform(waveform_type='SINE', frequency=1000)
