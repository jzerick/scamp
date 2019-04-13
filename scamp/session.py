from .ensemble import Ensemble
from .transcriber import Transcriber
from .midi_listener import *
from .spelling import SpellingPolicy
from .instruments import ScampInstrument
from clockblocks import Clock
from typing import Sequence


class Session(Clock, Ensemble, Transcriber):

    def __init__(self, tempo=60, default_soundfont="default", default_audio_driver="default",
                 default_midi_output_device="default"):
        """
        :param default_soundfont: the default soundfont used by instruments in this session. (Can be overridden at
        instrument creation.)
        :param default_audio_driver: the default driver used by (soundfont) instruments to output audio. (Can be
        overridden at instrument creation.
        :param default_midi_output_device: the default midi_output_device for outgoing midi streams. (Again, can be
        overridden at instrument creation.
        """
        # noinspection PyArgumentList
        Clock.__init__(self, name="MASTER", initial_tempo=tempo)
        Ensemble.__init__(self, default_soundfont=default_soundfont, default_audio_driver=default_audio_driver,
                          default_midi_output_device=default_midi_output_device)
        Transcriber.__init__(self)

        # A policy for spelling notes used as the default for the entire session
        # Useful if the entire session is in a particular key, for instance
        self._default_spelling_policy = None

    # ----------------------------------- Listeners ----------------------------------

    @staticmethod
    def get_available_ports_and_devices():
        return get_available_ports_and_devices()

    @staticmethod
    def print_available_ports_and_devices():
        print_available_ports_and_devices()

    def register_midi_callback(self, port_number_or_device_name, callback_function,
                               time_resolution=0.005, synchronous=False):
        start_midi_listener(port_number_or_device_name, callback_function,
                            clock=self, time_resolution=time_resolution, synchronous=synchronous)

    # --------------------------------- Recording Stuff -------------------------------

    def start_recording(self, instruments: Sequence[ScampInstrument] = None, clock: Clock = None, units="beats"):
        """
        Starts a recording, defaults to using the session (master) clock and all session instruments
        :param instruments: which instruments to record
        :param clock: which clock to record on, i.e. what are all the timings notated relative to
        :param units: one of ["beats", "time"]. Do we use the beats of the clock or the time?
        :return the Performance we will be recording to
        """
        return super().start_recording(self.instruments if instruments is None else instruments,
                                       self if clock is None else clock, units=units)

    @property
    def default_spelling_policy(self):
        return self._default_spelling_policy

    @default_spelling_policy.setter
    def default_spelling_policy(self, value):
        if value is None or isinstance(value, SpellingPolicy):
            self._default_spelling_policy = value
        elif isinstance(value, str):
            self._default_spelling_policy = SpellingPolicy.from_string(value)
        else:
            raise ValueError("Spelling policy not understood.")
