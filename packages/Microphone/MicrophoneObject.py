import os
import time
import wave
import collections
import pyaudio
import webrtcvad
from dotenv import load_dotenv, set_key
from packages.Config.ConfigObject import ConfigObject

class MicrophoneObject:

    ## This class is used to manage microphone input and voice activity detection (VAD).
    # It uses the PyAudio library to capture audio and the webrtcvad library for VAD.
    # The class allows for configuration of microphone settings, including aggressiveness and silence timeout.
    def __init__(self, config: ConfigObject, env_path=".env", aggressiveness=3, silence_timeout=1.0):
        self.config = config
        load_dotenv(env_path)
        self.env_path = env_path
        self.device_index = config.getMicrophoneIndex()
        self.aggressiveness = aggressiveness
        self.silence_timeout = float(config.getSilenceTimeout())

        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.frame_duration = int(config.getFrameDuration())
        self.frame_size = int(self.rate * self.frame_duration / 1000)

        self.p = pyaudio.PyAudio()
        self.device_index = self.getDeviceIndex()
        self.vad = webrtcvad.Vad(self.aggressiveness)

    ## Check if the microphone index is valid
    def getDeviceIndex(self):
        if self.device_index and self.device_index.strip().isdigit():
            return int(self.device_index)

        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                print(f"{i}: {info['name']}")

        selected = input("Enter microphone index: ").strip()
        if selected.isdigit():
            selected_index = int(selected)
            set_key(self.env_path, "MICROPHONE", str(selected_index))
            return selected_index

        raise ValueError("Invalid microphone selection.")

    ## This function listens to the microphone until silence is detected.
    def listenUntilSilence(self):
        stream = self.p.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             input_device_index=self.device_index,
                             frames_per_buffer=self.frame_size)

        frames = bytearray()
        ring_buffer = collections.deque(maxlen=int(self.silence_timeout * 1000 / self.frame_duration))
        triggered = False
        consecutive_silence_frames = 0
        required_silence_frames = int(self.silence_timeout * 1000 / self.frame_duration)

        max_recording_seconds = 15
        start_time = time.time()

        try:
            while True:
                if time.time() - start_time > max_recording_seconds:
                    break
                
                ## Read audio data from the stream and check for speech activity
                data = stream.read(self.frame_size, exception_on_overflow=False)

                ## Check if the audio data is speech or silence using VAD
                is_speech = self.vad.is_speech(data, self.rate)

                ## if isnt triggered, append the data to the ring buffer
                if not triggered:
                    ring_buffer.append(data)
                    if is_speech:
                        triggered = True
                        for chunk in ring_buffer:
                            frames.extend(chunk)
                        ring_buffer.clear()
                else:
                    ## else we append the data to the ring buffer and check if it is speech or silence
                    frames.extend(data)
                    if is_speech:
                        consecutive_silence_frames = 0
                    else:
                        consecutive_silence_frames += 1
                        if consecutive_silence_frames >= required_silence_frames:
                            break
        finally:
            stream.stop_stream()
            stream.close()

        return self.saveAudio(frames)

    ## This function saves the recorded audio frames to a WAV file.
    # It creates the directory if it doesn't exist and writes the audio data to the file.
    # The file path is returned for further processing.
    def saveAudio(self, frames: bytearray) -> str:
        os.makedirs(self.config.getGeneratedDir(), exist_ok=True)
        wf_path = self.config.getAudioFile()

        with wave.open(wf_path, 'wb') as wave_file:
            wave_file.setnchannels(self.channels)
            wave_file.setsampwidth(self.p.get_sample_size(self.format))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(frames)

        return wf_path

    ## This function terminates the PyAudio stream and releases resources.
    # It is important to call this function when the microphone is no longer needed to avoid resource leaks.
    def terminate(self):
        self.p.terminate()
