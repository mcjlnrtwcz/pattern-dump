import logging

from diquencer import Sequencer
from diquencer.events import MuteEvent, PatternEvent
from diquencer.models import Pattern
from diquencer.sequence import Sequence

from audio_recorder import AudioRecorder


class WrongChannelError(Exception):
    pass


class PatternDumpController:
    def __init__(self):
        self._audio_recorder = AudioRecorder()
        self._sequencer = Sequencer(start_callback=self._audio_recorder.start)

    def get_output_ports(self):
        return self._sequencer.output_ports

    def set_output_port(self, port):
        self._sequencer.set_output_port(port)

    def get_audio_devices(self):
        return self._audio_recorder.get_audio_devices()

    def set_audio_device(self, device_name):
        self._audio_recorder.set_audio_device(device_name)

    def set_samplerate(self, samplerate):
        self._audio_recorder.samplerate = samplerate

    def set_bitrate(self, bitrate):
        self._audio_recorder.bitrate = bitrate

    def set_midi_channel(self, channel):
        if not (channel > 0 and channel <= 16):
            raise WrongChannelError
        self._sequencer.set_midi_channel(channel)

    def dump_pattern(self, tempo, pattern, bank, length):
        pattern_event = PatternEvent(0, Pattern(f"{bank}{pattern}", pattern, bank, length), 1)
        for track in range(1, 9):
            logging.info(f"Recording track {track}")
            mute_event = MuteEvent(0, (track,))
            events = [pattern_event, mute_event]
            sequence = Sequence(tempo, events)
            self._audio_recorder.filename = f"track{track}.wav"
            self._audio_recorder.prepare_recording()
            self._sequencer.set_sequence(sequence)
            self._sequencer.start(blocking=True)
            self._audio_recorder.stop()
        logging.info("All tracks recorded")
