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
        self._sequencer = Sequencer(stop_callback=self._audio_recorder.stop)

    def get_output_ports(self):
        return self._sequencer.get_output_ports()

    def set_output_port(self, port):
        # TODO: Inform the user if port was set
        self._sequencer.set_output_port(port)

    def get_audio_devices(self):
        return self._audio_recorder.get_audio_devices()

    def set_audio_device(self, device, samplerate, bitrate):
        self._audio_recorder.set_audio_device(device)
        self._audio_recorder.samplerate = samplerate
        self._audio_recorder.bitrate = bitrate

    def set_midi_channel(self, channel: int) -> None:
        if not (channel > 0 and channel <= 16):
            raise WrongChannelError
        self._sequencer.set_midi_channel(channel)

    def dump_pattern(
            self,
            tempo: int,
            pattern: int,
            bank: str,
            length: int
    ) -> None:
        pattern_event = PatternEvent(0, Pattern(pattern, bank, length), 1)
        mute_event = MuteEvent(0, [2, 4, 6, 8])
        events = [pattern_event, mute_event]
        sequence = Sequence(tempo, events)
        self._sequencer.set_sequence(sequence)
        self._sequencer.start()
        self._audio_recorder.start()
