from setuptools import setup, find_packages

setup(
    name='strubloid-translate',
    version='1.2.0',
    description="OpenAI Whisper speech recognition",
    author="Strubloid",
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy",
        "ffmpeg-python",
        "tqdm",
        "more-itertools",
        "openai>=1.0.0",
        "numba",
        "typing-extensions>=4.10.0",
        "python-dotenv>=0.21.0",
        "webrtcvad",
        "pyaudio",
        "openai-whisper @ git+https://github.com/openai/whisper.git"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)