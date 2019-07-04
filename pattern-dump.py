#!/usr/bin/env python3
import logging
import tkinter as tk
from tkinter import messagebox

from controller import PatternDumpController, WrongChannelError


class PatternDumpGUI:

    PAD = 4

    def __init__(self, root, dumper):
        self.root = root
        self.dumper = dumper
        self.pattern = tk.StringVar()
        self.pattern.set("1")
        self.bank = tk.StringVar()
        self.bank.set("A")
        self.length = tk.StringVar()
        self.length.set("4")
        self.selected_audio_device = tk.StringVar()
        self.samplerate = tk.StringVar()
        self.samplerate.set("44100")
        self.bitrate = tk.StringVar()
        self.bitrate.set("16")
        self.midi_channel = tk.StringVar()
        self.midi_channel.set("1")
        self.selected_midi_device = tk.StringVar()

        # Main window

        self.root.geometry("400x480+0+0")
        self.root.title("pattern-dump")

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

        # Device settings
        # TODO: Fix spacing between label and option menu

        self.device_settings_frame = tk.Frame(self.root)
        self.device_settings_frame.grid(
            row=1, column=0, sticky=tk.W + tk.E, padx=self.PADDING
        )
        self.device_settings_frame.columnconfigure(1, weight=1)

        # Audio device
        self.audio_device_selector_label = tk.Label(
            self.device_settings_frame, text="Audio device"
        )
        self.audio_device_selector_label.grid(
            row=0, column=0, sticky=tk.W, pady=self.PADDING
        )
        self.audio_device_selector = tk.OptionMenu(
            self.device_settings_frame,
            self.selected_audio_device,
            *self.dumper.get_audio_devices()
        )
        self.audio_device_selector.grid(
            row=1, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )
        self.samplerate_selector_label = tk.Label(
            self.device_settings_frame, text="Samplerate"
        )
        self.samplerate_selector_label.grid(
            row=2, column=0, sticky=tk.W, pady=self.PADDING
        )
        self.samplerate_selector = tk.OptionMenu(
            self.device_settings_frame, self.samplerate, *("44100", "48000")
        )
        self.samplerate_selector.grid(
            row=2, column=1, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )
        self.bitrate_selector_label = tk.Label(
            self.device_settings_frame, text="Bitrate"
        )
        self.bitrate_selector_label.grid(
            row=3, column=0, sticky=tk.W, pady=self.PADDING
        )
        self.bitrate_selector = tk.OptionMenu(
            self.device_settings_frame, self.bitrate, *("16", "24", "32")
        )
        self.bitrate_selector.grid(
            row=3, column=1, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )

        self.device_margin = tk.Frame(self.device_settings_frame)
        self.device_margin.grid(
            row=4, column=0, columnspan=2, sticky=tk.W + tk.E, pady=2 * self.PADDING
        )

        # MIDI device
        self.midi_device_selector_label = tk.Label(
            self.device_settings_frame, text="MIDI device"
        )
        self.midi_device_selector_label.grid(
            row=5, column=0, sticky=tk.W, pady=self.PADDING
        )
        self.midi_device_selector = tk.OptionMenu(
            self.device_settings_frame,
            self.selected_midi_device,
            *self.dumper.get_output_ports()
        )
        self.midi_device_selector.grid(
            row=6, column=0, columnspan=2, sticky=tk.W + tk.E, pady=self.PADDING
        )
        self.midi_channel_label = tk.Label(
            self.device_settings_frame, text="MIDI channel"
        )
        self.midi_channel_label.grid(row=7, column=0, sticky=tk.W, pady=self.PADDING)
        self.midi_channel_input = tk.Entry(
            self.device_settings_frame, width=2, textvariable=self.midi_channel
        )
        self.midi_channel_input.grid(
            row=7, column=1, sticky=tk.W, padx=self.PADDING, pady=self.PADDING
        )

        self.dump_button = tk.Button(self.root, text="Dump", command=self.dump)
        self.dump_button.grid(
            row=2,
            column=0,
            sticky=tk.E + tk.S,
            padx=self.PADDING,
            pady=2 * self.PADDING,
        )

    def dump(self):
        self.dumper.set_output_port(self.selected_midi_device.get())
        try:
            self.dumper.set_audio_device(
                self.selected_audio_device.get(),
                int(self.samplerate.get()),
                int(self.bitrate.get()),
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid audio device settings")

        try:
            self.dumper.set_midi_channel(int(self.midi_channel.get()))
        except ValueError:
            messagebox.showerror("Error", "MIDI channel must be an integer")
        except WrongChannelError:
            messagebox.showerror("Error", "MIDI channel must be in range 1 to 16")

        try:
            self.dumper.dump_pattern(
                120, int(self.pattern.get()), self.bank.get(), int(self.length.get())
            )
        except ValueError:
            # TODO: Handle bad input (str to int conversion)
            messagebox.showerror("Error", "Invalid pattern settings")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s",
        level=logging.DEBUG,
    )
    root = tk.Tk()
    dumper = PatternDumpController()
    PatternDumpGUI(root, dumper)
    root.mainloop()
