from __future__ import division
import thread
import wave
import pyaudio
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


class Recorder:
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.frames = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.terminate()

    def terminate(self):
        self.pyaudio.terminate()

    def start(self):
        self.frames = []
        self.signal = False
        self.rec_thread = thread.start_new_thread(self.record, ())

    def stop(self):
        self.signal = True
        #time.sleep(0.2)

    def duration(self):
        return (len(self.frames) * CHUNK) / RATE

    def save(self, filename):
        if not self.frames:
            raise "No audio have been recorded yet !"

        wf = wave.open(filename, 'wb')

        # setup format metadata
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        # write audio data
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def record(self):
        stream = self.pyaudio.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   frames_per_buffer=CHUNK)
        self.frames = []
        while not self.signal:
            data = stream.read(CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

    def play(self):
        stream = self.pyaudio.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   output=True,
                                   frames_per_buffer=CHUNK)
        for chunk in self.frames:
            data = stream.write(chunk)

        stream.close()
