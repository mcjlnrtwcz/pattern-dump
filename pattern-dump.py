#!/usr/bin/env python3
import logging
import tkinter as tk
from tkinter import messagebox

from controller import PatternDumpController, WrongChannelError
from gui_utils import Selector


PADDING = 4


class LabeledEntry(tk.Frame):
    def __init__(self, parent, name, default_value, callback, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.user_callback = callback

        self.input_value = tk.StringVar()
        self.input_value.trace_add("write", self.input_callback)
        self.input_value.set(default_value)

        self.label = tk.Label(self, text=name)
        self.label.grid(row=0, column=0, sticky=tk.W, pady=PADDING)
        self.input = tk.Entry(self, width=2, textvariable=self.input_value)
        self.input.grid(row=0, column=1, padx=PADDING, pady=PADDING)

    def input_callback(self, *args):
        input_value = self.input_value.get()
        if input_value != "":
            self.user_callback(input_value)


class PatternSettingsFrame(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.pattern_input = LabeledEntry(self, "Pattern", "1", self.pattern_callback)
        self.pattern_input.grid(row=0, sticky=tk.W)

        self.bank_input = LabeledEntry(self, "Bank", "A", self.bank_callback)
        self.bank_input.grid(row=1, sticky=tk.W)

        self.length_input = LabeledEntry(self, "Length", "4", self.length_callback)
        self.length_input.grid(row=2, sticky=tk.W)

    def pattern_callback(self, pattern):
        try:
            self.controller.pattern = int(pattern)
        except ValueError:
            messagebox.showerror("Error", "Pattern must be a number")  # FIXME

    def bank_callback(self, bank):
        self.controller.bank = bank

    def length_callback(self, length):
        try:
            self.controller.length = int(length)
        except ValueError:
            messagebox.showerror("Error", "Length must be a number")  # FIXME


class PatternDumpView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        # Main window
        self.config(padx=PADDING * 2, pady=PADDING)
        self.title("pattern-dump")
        self.resizable(False, False)

        # Pattern settings
        self.pattern_settings_frame = PatternSettingsFrame(self, controller)
        self.pattern_settings_frame.grid(
            row=0, column=0, sticky=tk.W + tk.E + tk.N, padx=PADDING, pady=PADDING
        )

        # Audio/MIDI device settings
        self.device_settings_frame = tk.Frame(self)
        self.device_settings_frame.grid(
            row=1, column=0, columnspan=2, sticky=tk.W, padx=PADDING
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
            row=0, column=0, columnspan=2, sticky=tk.W + tk.E, pady=PADDING
        )

        # Samplerate
        self.samplerate_selector = Selector(
            self.device_settings_frame,
            "Samplerate",
            ("44100", "48000"),
            lambda samplerate: self.controller.set_samplerate(int(samplerate)),
        )
        self.samplerate_selector.grid(
            row=1, column=0, columnspan=2, sticky=tk.W + tk.E, pady=PADDING
        )

        # Bitrate
        self.bitrate_selector = Selector(
            self.device_settings_frame,
            "Bitrate",
            ("16", "24", "32"),
            lambda bitrate: self.controller.set_bitrate(int(bitrate)),
        )
        self.bitrate_selector.grid(
            row=2, column=0, columnspan=2, sticky=tk.W + tk.E, pady=PADDING
        )

        # MIDI device
        self.midi_device_selector = Selector(
            self.device_settings_frame,
            "MIDI device",
            self.controller.get_midi_devices(),
            lambda device_name: self.controller.set_midi_device(device_name),
        )
        self.midi_device_selector.grid(
            row=3, column=0, columnspan=2, sticky=tk.W + tk.E, pady=PADDING
        )

        # MIDI channel
        self.midi_channel_input = LabeledEntry(self.device_settings_frame, "MIDI channel", "1", self.set_midi_channel)
        self.midi_channel_input.grid(row=4, sticky=tk.W)

        self.dump_button = tk.Button(self, text="Dump", command=self.dump)
        self.dump_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.E + tk.S,
            padx=PADDING,
            pady=2 * PADDING,
        )

    def set_midi_channel(self, midi_channel):  # FIXME
        try:
            self.controller.set_midi_channel(int(midi_channel))
        except WrongChannelError:
            messagebox.showerror("Error", "MIDI channel must be in range from 1 to 16")
            return
        except ValueError:
            messagebox.showerror("Error", "MIDI channel must be an integer")
            return

    def dump(self):
        self.controller.dump_pattern(120)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s",
        level=logging.INFO,
    )
    controller = PatternDumpController()
    view = PatternDumpView(controller)
    view.mainloop()
