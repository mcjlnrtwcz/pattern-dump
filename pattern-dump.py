#!/usr/bin/env python3
import logging
import tkinter as tk

from diquencer import Sequencer
from diquencer.models import Pattern, PatternEvent, MuteEvent
from diquencer.sequence import Sequence


class PatternDump:

    def __init__(self):
        self._sequencer = Sequencer()

    def get_output_ports(self):
        return self._sequencer.get_output_ports()

    def set_output_port(self, port):
        # TODO: Inform the user if port was set
        self._sequencer.set_output_port(port)

    def dump_pattern(self, tempo: int, pattern: int, bank: str, length: int) -> None:
        pattern_event = PatternEvent(0, Pattern(pattern, bank, length), 1)
        mute_event = MuteEvent(0, [2, 4, 6, 8])
        events = [pattern_event, mute_event]
        sequence = Sequence(tempo, events)
        self._sequencer.set_sequence(sequence)
        self._sequencer.start()


class PatternDumpGUI:

    PAD = 4

    def __init__(self, root, dumper):
        self.root = root
        self.dumper = dumper
        self.pattern = tk.StringVar()
        self.pattern.set('1')
        self.bank = tk.StringVar()
        self.bank.set('A')
        self.length = tk.StringVar()
        self.length.set('4')
        self.selected_midi_device = tk.StringVar()

        # Main window

        self.root.geometry('400x300+0+0')
        self.root.title('pattern-dump')

        # Configure grid

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=3)

        # Pattern settings

        self.pattern_settings_frame = tk.Frame(self.root)
        self.pattern_settings_frame.grid(
            row=0,
            column=0,
            sticky=tk.W+tk.E+tk.N,
            padx=self.PAD,
            pady=self.PAD
        )

        self.pattern_label = tk.Label(
            self.pattern_settings_frame,
            text='Pattern'
        )
        self.pattern_label.grid(row=0, column=0, sticky=tk.W, pady=self.PAD)
        self.pattern_input = tk.Entry(
            self.pattern_settings_frame,
            width=2,
            textvariable=self.pattern
        )
        self.pattern_input.grid(row=0, column=1, padx=self.PAD, pady=self.PAD)

        self.bank_label = tk.Label(
            self.pattern_settings_frame,
            text='Bank'
        )
        self.bank_label.grid(row=1, column=0, sticky=tk.W, pady=self.PAD)
        self.bank_input = tk.Entry(
            self.pattern_settings_frame,
            width=2,
            textvariable=self.bank
        )
        self.bank_input.grid(row=1, column=1, padx=self.PAD, pady=self.PAD)

        self.length_label = tk.Label(
            self.pattern_settings_frame,
            text='Length'
        )
        self.length_label.grid(row=2, column=0, sticky=tk.W, pady=self.PAD)
        self.length_input = tk.Entry(
            self.pattern_settings_frame,
            width=2,
            textvariable=self.length
        )
        self.length_input.grid(row=2, column=1, padx=self.PAD, pady=self.PAD)

        # Device settings
        # TODO: Fix spacing between label and option menu

        self.device_settings_frame = tk.Frame(self.root)
        self.device_settings_frame.grid(
            row=1,
            column=0,
            sticky=tk.W+tk.E,
            padx=self.PAD,
        )
        self.device_settings_frame.columnconfigure(0, weight=1)

        # Audio device
        self.audio_device_selector_label = tk.Label(
            self.device_settings_frame,
            text='Audio device'
        )
        self.audio_device_selector_label.grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=self.PAD
        )
        self.audio_device_selector = tk.OptionMenu(
            self.device_settings_frame,
            None,
            'Device 1',
            'Device 2'
        )
        self.audio_device_selector.grid(
            row=1,
            column=0,
            sticky=tk.W+tk.E,
            pady=self.PAD
        )

        # MIDI device
        self.midi_device_selector_label = tk.Label(
            self.device_settings_frame,
            text='MIDI device'
        )
        self.midi_device_selector_label.grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=self.PAD
        )
        self.midi_device_selector = tk.OptionMenu(
            self.device_settings_frame,
            self.selected_midi_device,
            *self.dumper.get_output_ports()
        )
        self.midi_device_selector.grid(
            row=3,
            column=0,
            sticky=tk.W+tk.E,
            pady=self.PAD
        )

        self.dump_button = tk.Button(self.root, text='Dump', command=self.dump)
        self.dump_button.grid(
            row=2,
            column=0,
            sticky=tk.E+tk.S,
            padx=self.PAD,
            pady=2*self.PAD
        )

    def dump(self):
        self.dumper.set_output_port(self.selected_midi_device.get())
        try:
            self.dumper.dump_pattern(
                120,
                int(self.pattern.get()),
                self.bank.get(),
                int(self.length.get())
            )
        except ValueError:
            # TODO: Handle bad input (str to int conversion)
            logging.warning('Invalid pattern settings')


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.DEBUG
    )
    root = tk.Tk()
    dumper = PatternDump()
    PatternDumpGUI(root, dumper)
    root.mainloop()
