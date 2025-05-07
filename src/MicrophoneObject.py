import pyaudio
import wave
import time
import collections
import webrtcvad
from dotenv import load_dotenv, set_key
import os
from ConfigObject import ConfigObject

class MicrophoneObject:

    ## Class to handle microphone input and voice activity detection.
    # It uses the PyAudio library to access the microphone and the webrtcvad library
    # for voice activity detection. The class captures audio until silence is detected
    # for a specified duration, and saves the audio to a temporary WAV file.
    # @param device_name: The name of the microphone device to use.
    # @param aggressiveness: The aggressiveness level for the VAD (0-3).
    # @param silence_timeout: The duration of silence (in seconds) to wait before stopping the recording.
    def __init__(self,config : ConfigObject, env_path=".env", aggressiveness=2, silence_timeout=1.0):
        
        ## loading the main environment variables
        self.config = config

        load_dotenv(env_path)
        self.env_path = env_path
        self.device_index = config.getMicrophoneIndex()
        self.aggressiveness = aggressiveness
        self.silence_timeout = silence_timeout        
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.frame_duration = 30 # microseconds
        self.frame_size = int(self.rate * self.frame_duration / 1000)
        self.p = pyaudio.PyAudio()
        self.device_index = self.getDeviceIndex()
        self.vad = webrtcvad.Vad(self.aggressiveness)

    ## Get the index of the microphone device based on its name.
    def getDeviceIndex(self):

        ## Check if the device index is already set in the environment variable.
        if self.device_index and self.device_index.strip().isdigit():
            return int(self.device_index)
        
        ## If not set, prompt the user to select a microphone device.
        print("\n🎤 No MICROPHONE index set in .env. Listing available input devices:\n")
        input_devices = []
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                print(f"{i}: {info['name']}")
                input_devices.append((i, info["name"]))

        ## This will be set the default microphone
        selected = input("🔧 Enter the number of the microphone you'd like to use: ").strip()
        if selected.isdigit():
            selected_index = int(selected)
            set_key(self.env_path, "MICROPHONE", str(selected_index))
            print(f"✅ Saved MICROPHONE={selected_index} to {self.env_path}")
            return selected_index

        raise ValueError("❌ Invalid microphone selection.")

    ## Listen to the microphone until silence is detected for a specified duration.
    def listenUntilSilence(self):

        ## Open the microphone stream for recording.
        stream = self.p.open(format=self.format
            , channels=self.channels
            , rate=self.rate
            , input=True
            , input_device_index=self.device_index
            , frames_per_buffer=self.frame_size)

        frames = []
        ring_buffer = collections.deque(maxlen=int(self.silence_timeout * 1000 / self.frame_duration))
        triggered = False
        silence_start = None

        print("🎙️ Listening... Start speaking.")

        try:
            while True:
                
                ## Read audio data from the stream and check for voice activity.
                data = stream.read(self.frame_size, exception_on_overflow=False)

                ## Check if the audio data is speech using VAD.
                ## The VAD will return True if it detects speech, and False otherwise.
                is_speech = self.vad.is_speech(data, self.rate)

                if not triggered:
                    ring_buffer.append(data)
                    if is_speech:
                        triggered = True
                        print("🔊 Recording")
                        frames.extend(ring_buffer)
                        ring_buffer.clear()
                else:
                    frames.append(data)
                    if is_speech:
                        silence_start = None
                    else:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start > self.silence_timeout:
                            print("🤫 Stopping...")
                            break

        finally:
            stream.stop_stream()
            stream.close()

        ## Save the recorded audio to a temporary WAV file.
        os.makedirs("generated", exist_ok=True)
        wf_path = os.path.join("generated", "mic.wav")
        
        # Save audio
        with wave.open(wf_path, 'wb') as wave_file:
            wave_file.setnchannels(self.channels)
            wave_file.setsampwidth(self.p.get_sample_size(self.format))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(frames))

        return wf_path

    ## Terminate the PyAudio stream and release resources.
    def terminate(self):
        self.p.terminate()