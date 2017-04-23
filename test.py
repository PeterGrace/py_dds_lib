import serial
import logging
import sys
from py_dds_lib import DDSInteraction

logging.basicConfig(level=logging.DEBUG)

dds = DDSInteraction('COM4')
dds.get_version()
dds.chan_on(1)
dds.set_waveform(1,1)
dds.set_duty_cycle(1,500)

dds.set_amplitude(1,500)
dds.set_offset(1,100)
dds.set_frequency(1, 5000)
#dds.chan_off(1)
#dds.set_pulse_time(1,10)

sys.exit(0)