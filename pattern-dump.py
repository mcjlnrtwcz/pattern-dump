#!/usr/bin/env python3

import tkinter as tk


class PatternDump:

    PAD = 4

    def __init__(self, root):
        self.root = root

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
        self.pattern_input = tk.Entry(self.pattern_settings_frame, width=2)
        self.pattern_input.grid(row=0, column=1, padx=self.PAD, pady=self.PAD)

        self.bank_label = tk.Label(
            self.pattern_settings_frame,
            text='Bank'
        )
        self.bank_label.grid(row=1, column=0, sticky=tk.W, pady=self.PAD)
        self.bank_input = tk.Entry(self.pattern_settings_frame, width=2)
        self.bank_input.grid(row=1, column=1, padx=self.PAD, pady=self.PAD)

        self.length_label = tk.Label(
            self.pattern_settings_frame,
            text='Length'
        )
        self.length_label.grid(row=2, column=0, sticky=tk.W, pady=self.PAD)
        self.length_input = tk.Entry(self.pattern_settings_frame, width=2)
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
            None,
            'Device 1',
            'Device 2'
        )
        self.midi_device_selector.grid(
            row=3,
            column=0,
            sticky=tk.W+tk.E,
            pady=self.PAD
        )

        self.dump_button = tk.Button(self.root, text='Dump')
        self.dump_button.grid(
            row=2,
            column=0,
            sticky=tk.E+tk.S,
            padx=self.PAD,
            pady=2*self.PAD
        )


if __name__ == '__main__':
    root = tk.Tk()
    PatternDump(root)
    root.mainloop()
