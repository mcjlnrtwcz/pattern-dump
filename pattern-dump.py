#!/usr/bin/env python3
import logging
import tkinter as tk
from tkinter import messagebox

from controller import PatternDumpController, WrongChannelError
from gui_utils import Selector


class PatternDumpGUI:

    PADDING = 4

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.pattern = tk.StringVar()
        self.pattern.set("1")

        self.bank = tk.StringVar()
        self.bank.set("A")

        self.length = tk.StringVar()
        self.length.set("4")

        self.samplerate = tk.StringVar()
        self.samplerate.set("44100")

        self.bitrate = tk.StringVar()
        self.bitrate.set("16")

        self.midi_channel = tk.StringVar()
        self.midi_channel.set("1")

        self.selected_midi_device = tk.StringVar()

        # Main window
        self.root.config(padx=self.PADDING * 2, pady=self.PADDING)
        self.root.title("pattern-dump")
        self.root.resizable(False, False)

        # Pattern settings
        self.pattern_settings_frame = tk.Frame(self.root)
        self.pattern_settings_frame.grid(
            row=0,
            column=0,
            sticky=tk.W + tk.E + tk.N,
            padx=self.PADDING,
            pady=self.PADDING,
        )

        self.pattern_label = tk.Label(self.pattern_settings_frame, text="Pattern")
        self.pattern_label.grid(row=0, column=0, sticky=tk.W, pady=self.PADDING)
        self.pattern_input = tk.Entry(
            self.pattern_settings_frame, width=2, textvariable=self.pattern
        )
        self.pattern_input.grid(row=0, column=1, padx=self.PADDING, pady=self.PADDING)

        self.bank_label = tk.Label(self.pattern_settings_frame, text="Bank")
        self.bank_label.grid(row=1, column=0, sticky=tk.W, pady=self.PADDING)
        self.bank_input = tk.Entry(
            self.pattern_settings_frame, width=2, textvariable=self.bank
        )
        self.bank_input.grid(row=1, column=1, padx=self.PADDING, pady=self.PADDING)

        self.length_label = tk.Label(self.pattern_settings_frame, text="Length")
        self.length_label.grid(row=2, column=0, sticky=tk.W, pady=self.PADDING)
        self.length_input = tk.Entry(
            self.pattern_settings_frame, width=2, textvariable=self.length
        )
        self.length_input.grid(row=2, column=1, padx=self.PADDING, pady=self.PADDING)

        # Audio/MIDI device settings
        self.device_settings_frame = tk.Frame(self.root)
        self.device_settings_frame.grid(
            row=1, column=0, columnspan=2, sticky=tk.W, padx=self.PADDING
        )
        self.device_settings_frame.columnconfigure(0, minsize=240)

        # Audio device
        self.audio_device_selector = Selector(
            self.device_settings_frame,
            "Audio device",
            controller.get_audio_devices(),
            lambda device_name: self.controller.set_audio_device(device_name),
        )
        self.audio_device_selector.grid(
            row=0, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )

        # Samplerate
        self.samplerate_selector = Selector(
            self.device_settings_frame,
            "Samplerate",
            ("44100", "48000"),
            lambda samplerate: self.controller.set_samplerate(int(samplerate)),
        )
        self.samplerate_selector.grid(
            row=1, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )

        # Bitrate
        self.bitrate_selector = Selector(
            self.device_settings_frame,
            "Bitrate",
            ("16", "24", "32"),
            lambda bitrate: self.controller.set_bitrate(int(bitrate)),
        )
        self.bitrate_selector.grid(
            row=2, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )

        # MIDI device
        self.midi_device_selector = Selector(
            self.device_settings_frame,
            "MIDI device",
            self.controller.get_midi_devices(),
            lambda device_name: self.controller.set_midi_device(device_name),
        )
        self.midi_device_selector.grid(
            row=3, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )

        # MIDI channel
        self.midi_channel_label = tk.Label(
            self.device_settings_frame, text="MIDI channel"
        )
        self.midi_channel_label.grid(row=4, column=0, sticky=tk.W, pady=self.PADDING)
        # TODO: Move input to the left
        self.midi_channel_input = tk.Entry(
            self.device_settings_frame, width=2, textvariable=self.midi_channel
        )
        self.midi_channel_input.grid(
            row=4, column=1, padx=self.PADDING, pady=self.PADDING
        )

        self.dump_button = tk.Button(self.root, text="Dump", command=self.dump)
        self.dump_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.E + tk.S,
            padx=self.PADDING,
            pady=2 * self.PADDING,
        )

    def dump(self):
        try:
            self.controller.set_midi_channel(int(self.midi_channel.get()))
        except ValueError:
            messagebox.showerror("Error", "MIDI channel must be an integer")
            return
        except WrongChannelError:
            messagebox.showerror("Error", "MIDI channel must be in range from 1 to 16")
            return

        try:
            self.controller.dump_pattern(
                120, int(self.pattern.get()), self.bank.get(), int(self.length.get())
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid bank or pattern")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s",
        level=logging.INFO,
    )
    root = tk.Tk()
    controller = PatternDumpController()
    PatternDumpGUI(root, controller)
    root.mainloop()
