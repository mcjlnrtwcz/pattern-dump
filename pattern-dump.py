#!/usr/bin/env python3
import logging
import tkinter as tk
from tkinter import messagebox

from controller import PatternDumpController, WrongChannelError
from gui_utils import Selector


PADDING = 4


class PatternSettingsFrame(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.pattern = tk.StringVar()
        self.pattern.trace_add("write", self.pattern_callback)
        self.pattern.set("1")

        self.bank = tk.StringVar()
        self.bank.trace_add("write", self.bank_callback)
        self.bank.set("A")

        self.length = tk.StringVar()
        self.length.trace_add("write", self.length_callback)
        self.length.set("4")

        self.pattern_label = tk.Label(self, text="Pattern")
        self.pattern_label.grid(row=0, column=0, sticky=tk.W, pady=PADDING)
        self.pattern_input = tk.Entry(self, width=2, textvariable=self.pattern)
        self.pattern_input.grid(row=0, column=1, padx=PADDING, pady=PADDING)

        self.bank_label = tk.Label(self, text="Bank")
        self.bank_label.grid(row=1, column=0, sticky=tk.W, pady=PADDING)
        self.bank_input = tk.Entry(self, width=2, textvariable=self.bank)
        self.bank_input.grid(row=1, column=1, padx=PADDING, pady=PADDING)

        self.length_label = tk.Label(self, text="Length")
        self.length_label.grid(row=2, column=0, sticky=tk.W, pady=PADDING)
        self.length_input = tk.Entry(self, width=2, textvariable=self.length)
        self.length_input.grid(row=2, column=1, padx=PADDING, pady=PADDING)

    def pattern_callback(self, *args):
        try:
            pattern = self.pattern.get()
            if pattern != "":
                self.controller.pattern = int(pattern)
        except ValueError:
            messagebox.showerror("Error", "Pattern must be a number")

    def bank_callback(self, *args):
        bank = self.bank.get()
        if bank != "":
            self.controller.bank = bank

    def length_callback(self, *args):
        try:
            length = self.length.get()
            if length != "":
                self.controller.length = int(length)
        except ValueError:
            messagebox.showerror("Error", "Length must be a number")


class PatternDumpView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        self.samplerate = tk.StringVar()
        self.samplerate.set("44100")

        self.bitrate = tk.StringVar()
        self.bitrate.set("16")

        self.midi_channel = tk.StringVar()
        self.midi_channel.set("1")

        self.selected_midi_device = tk.StringVar()

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
        self.midi_channel_label = tk.Label(
            self.device_settings_frame, text="MIDI channel"
        )
        self.midi_channel_label.grid(row=4, column=0, sticky=tk.W, pady=PADDING)
        # TODO: Move input to the left
        self.midi_channel_input = tk.Entry(
            self.device_settings_frame, width=2, textvariable=self.midi_channel
        )
        self.midi_channel_input.grid(row=4, column=1, padx=PADDING, pady=PADDING)

        self.dump_button = tk.Button(self, text="Dump", command=self.dump)
        self.dump_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.E + tk.S,
            padx=PADDING,
            pady=2 * PADDING,
        )

    def dump(self):
        try:
            self.controller.set_midi_channel(int(self.midi_channel.get()))
        except WrongChannelError:
            messagebox.showerror("Error", "MIDI channel must be in range from 1 to 16")
            return
        except ValueError:
            messagebox.showerror("Error", "MIDI channel must be an integer")
            return

        try:
            self.controller.dump_pattern(120)
        except ValueError:
            messagebox.showerror("Error", "Invalid bank or pattern")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s",
        level=logging.INFO,
    )
    controller = PatternDumpController()
    view = PatternDumpView(controller)
    view.mainloop()
