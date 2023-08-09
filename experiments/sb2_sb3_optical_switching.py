"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to control the optical switching of the ultra-low
loss phase change material Sb2Se3 experiment via a Python API. The experiment
was designed and build by Daniel Lawson. More information about the specifics
of the experiment can be found at:
https://iopscience.iop.org/article/10.1088/2040-8986/ac5ece/meta and
https://onlinelibrary.wiley.com/doi/full/10.1002/adfm.202002447.
"""


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
        bk_4063b: BKCom client object used to communicate with the physical
            instrument BK Precision 4063B BNC.
        x_kdc101: KD101Com client object used to communicated with the
            physical brushed motor ThorLabs Kinesis KD101 used to control the
            x movement.
        y_kdc101: KD101Com client object used to communicated with the
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
        self.bk_4063b = BKCom(self.bk_4063b_address)
        self.x_kdc101 = KDC101Com(self.x_kdc101_address)
        self.y_kdc101 = KDC101Com(self.y_kdc101_address)
