import logging
import wave
from queue import Empty, Queue
from threading import Event, Thread

import sounddevice as sd


class AudioRecorder:

    def __init__(self):
        self.samplerate = 44100
        self.bitrate = 16
        self.channels = 1
        # TODO: Is it safe with set_audio_device?
        self._queue = Queue()
        self._stream = None
        self._consumer = None

    def get_audio_devices(self):
        return [
            device['name']
            for device in sd.query_devices()
            if device['max_input_channels'] > 0
        ]

    def set_audio_device(self, device):
        sd.default.device = device

    def _callback(self, indata, frames, time, status):
        self._queue.put(indata[:])

    def start(self):
        logging.info('Starting audio recorder')
        # TODO: Is it safe with set_audio_device?
        self._stream = sd.RawInputStream(
            samplerate=self.samplerate,
            dtype=f'int{self.bitrate}',
            callback=self._callback,
            channels=self.channels
        )
        # TODO Check settings with check_input_settings
        self._consumer = Consumer(
            self._queue,
            self.channels,
            self.bitrate / 8,  # wave writer accepts number of bytes
            self.samplerate
        )
        self._stream.start()
        self._consumer.start()

    def stop(self):
        logging.info('Stopping audio recorder')
        self._stream.stop()
        self._consumer.stop()


class Consumer(Thread):

    def __init__(self, queue, channels, sampwidth, samplerate):
        super().__init__()
        self._queue = queue
        self._channels = channels
        self._sampwidth = sampwidth
        self._samplerate = samplerate
        self._stop_event = Event()

    def run(self):
        with wave.open('recording.wav', mode='wb') as wave_file:
            wave_file.setnchannels(self._channels)
            wave_file.setsampwidth(int(self._sampwidth))
            wave_file.setframerate(self._samplerate)
            while not self._stop_event.is_set():
                try:
                    data = self._queue.get(timeout=2)
                    wave_file.writeframes(data)
                except Empty:
                    break
        logging.debug('Finished saving data to disk')

    def stop(self):
        self._stop_event.set()
