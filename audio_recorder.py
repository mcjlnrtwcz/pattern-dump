import logging
import wave
from queue import Empty, Queue
from threading import Event, Thread
from time import sleep

import sounddevice as sd


class AudioRecorder:
    def __init__(self):
        self.samplerate = 44100
        self.bitrate = 16
        self.channels = 1
        self.filename = "recording.wav"
        self._queue = Queue()
        self._stream = None
        self._consumer = None
        self._before_first_callback = True
        self._latency = 0

    def get_audio_devices(self):
        return [
            device["name"]
            for device in sd.query_devices()
            if device["max_input_channels"] > 0
        ]

    def set_audio_device(self, device_name):
        sd.default.device = device_name
        sd.default.latency = "low"
        sd.default.blocksize = 128

    def _callback(self, indata, frames, time, status):
        if self._before_first_callback:
            self._latency = time.currentTime - time.inputBufferAdcTime
            self._before_first_callback = False
        self._queue.put(indata[:])

    def prepare_recording(self):
        self._stream = sd.RawInputStream(
            samplerate=self.samplerate,
            dtype=f"int{self.bitrate}",
            callback=self._callback,
            channels=self.channels,
        )
        self._consumer = Consumer(
            self._queue,
            self.channels,
            self.bitrate / 8,  # wave writer accepts number of bytes
            self.samplerate,
            self.filename,
        )

    def start(self):
        self._before_first_callback = True
        self._stream.start()
        self._consumer.start()
        while self._before_first_callback:
            sleep(0.0001)

    def stop(self):
        self._stream.stop()
        self._consumer.stop()
        self._consumer.join()
        logging.info(f"Audio recorder stopped. Latency: {self._latency}")


class Consumer(Thread):
    def __init__(self, queue, channels, sampwidth, samplerate, filename):
        super().__init__()
        self._queue = queue
        self._channels = channels
        self._sampwidth = sampwidth
        self._samplerate = samplerate
        self._filename = filename
        self._stop_event = Event()

    def run(self):
        with wave.open(self._filename, mode="wb") as wave_file:
            wave_file.setnchannels(self._channels)
            wave_file.setsampwidth(int(self._sampwidth))
            wave_file.setframerate(self._samplerate)
            while not self._stop_event.is_set():
                try:
                    data = self._queue.get(timeout=2)
                    wave_file.writeframes(data)
                except Empty:
                    break
        logging.debug("Finished saving data to disk")

    def stop(self):
        self._stop_event.set()
