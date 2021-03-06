'''Module for controlling MHS-52XX series DDS Function Generators'''
import logging
import sys

import serial


class DDSInteraction:
    '''Class for interacting with MHS-52XX series DDS Function Generators'''
    def __init__(self, port):
        try:
            self.s = serial.Serial(
                port,
                57600,
                timeout=0.1,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE
            )
        except Exception as e:
            logging.error("Exception: {}".format(e))
            sys.exit(1)

    def _get_result_from_cmd(self, cmd):
        cmdlen = len(cmd)
        fm = bytearray("{}\n".format(cmd), 'utf-8')
        self.s.write(b":\n")
        rs = self.s.read(5)
        self.s.write(fm)
        rs = self.s.read(255)
        logging.debug("rs: {}".format(rs))
        return rs[cmdlen:]

    def get_version(self):
        """Return DDS Signal Generator Version String"""
        cmd = ":r0c"
        foo = self._get_result_from_cmd(cmd)
        return foo

    def chan_on(self, channel):
        """Enable waveform output on channel"""
        cmd = ":s{}b1".format(channel)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def chan_off(self, channel):
        """Disable waveform output on channel"""
        cmd = ":s{}b0".format(channel)
        foo = self._get_result_from_cmd(cmd)
        return foo


    def set_waveform(self, channel, waveform):
        """Change waveform type for channel.  0=sine, 1=square, 2=tri, 3=up, 4=dn, 100+ arb
        """
        cmd = ":s{}w{}\r\n".format(channel, waveform)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_duty_cycle(self, channel, duty):
        """set duty cycle for waveform.  duty is 0-1000, with 1000 being 100%
        """
        cmd = ":s{}d{}".format(channel, duty)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_pulse_time(self, channel, pulse_time):
        """ Set duty cycle by pulse time, in microseconds."""    
        # get_freq = ":r{}f".format(channel)
        # freqbytes = self._get_result_from_cmd(get_freq)
        # freq = int(freqbytes.decode().rstrip())/100
        # logging.debug("Frequency is {}Hz".format(freq))
        # If 1000Hz means 1000 pulses in 1 second, and duty cycle means 
        one_sec = 1000000
        res = one_sec / pulse_time

    def set_amplitude(self, channel, amplitude):
        """set amplitude for output signal, in millivolts"""
        cmd=":s{}a{}\r\n".format(channel, amplitude)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_offset(self, channel, offset):
        """set offset of waveform from zero-line by +/- percent"""
        offset = offset + 120
        if offset > 240:
            offset = 240
        elif offset < 0:
            offset = 0
        logging.debug("offset = {}".format(offset))    
        cmd = ":s{}o{}\r\n".format(channel, offset)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_phase(self, channel, phase):
        """set phase of waveform for channel, in degrees"""
        phase = int(phase)
        cmd = ":s{}p{}".format(channel, phase)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_frequency(self, channel, frequency):
        """set frequency of waveform, in hertz"""
        frequency = frequency * 100
        cmd = ":s{}f{}".format(channel, frequency)
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_attenuation(self, channel, attenuate=False):
        """Attenuate selected channel by 20dB."""
        if attenuate:
            val = 0
        else:
            val = 1
        cmd = ":s{}y{}".format(channel, val)    
        foo = self._get_result_from_cmd(cmd)
        return foo

    def set_tracking(self, trace=False):
        """Set Ch2 frequency to same as Ch1.  If both Ch1 and Ch2 have same amplitude at time of trace set,
        amplitude is also tracked.  Same for duty cycle; if they are equal when tracking is turned on, they will track
        for further changes."""
        if trace:
            val = 1
        else:
            val = 0
        cmd = ":s3b{}".format(val)
        foo = self._get_result_from_cmd(cmd)
        return foo    

    def ttl_input(self, TTL=True):
        """Set input to TTL if passed True."""
        if TTL:
            val = 1
        else:
            val = 0
        cmd = ":s4b{}".format(val)
        foo = self._get_result_from_cmd(cmd)
        return foo        


    def engage_counter(self, counter=False):
        if counter:
            val = 1
        else:
            val = 0    
        cmd = ":s6b{}".format(val)
        foo = self._get_result_from_cmd(cmd)
        return foo

