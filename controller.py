from diquencer import Sequencer
from diquencer.models import Pattern, PatternEvent, MuteEvent
from diquencer.sequence import Sequence


class WrongChannelError(Exception):
    pass


class PatternDumpController:

    def __init__(self):
        self._sequencer = Sequencer()

    def get_output_ports(self):
        return self._sequencer.get_output_ports()

    def set_output_port(self, port):
        # TODO: Inform the user if port was set
        self._sequencer.set_output_port(port)

    def set_midi_channel(self, channel: int) -> None:
        if not (channel > 0 and channel <= 16):
            raise WrongChannelError
        self._sequencer.set_midi_channel(channel)

    def dump_pattern(self, tempo: int, pattern: int, bank: str, length: int) -> None:
        pattern_event = PatternEvent(0, Pattern(pattern, bank, length), 1)
        mute_event = MuteEvent(0, [2, 4, 6, 8])
        events = [pattern_event, mute_event]
        sequence = Sequence(tempo, events)
        self._sequencer.set_sequence(sequence)
        self._sequencer.start()
