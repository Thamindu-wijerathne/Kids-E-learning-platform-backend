from faster_whisper import WhisperModel
import subprocess, tempfile, os, uuid


class SpeechRecognitionService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = WhisperModel(
                "small"
            )
        return cls._instance

    def transcribe(self, audio_file):
        segments, info = self.model.transcribe(audio_file)
        return list(segments)
    
    @staticmethod # this not class method, just a utility function
    def convert_webm_to_wav(webm_bytes: bytes) -> bytes:
        print("Converting webm to wav...")
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as in_f:
            in_f.write(webm_bytes)
            in_path = in_f.name

        out_path = in_path.replace(".webm", ".wav")

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", in_path,
                "-vn",
                "-ac", "1",        # mono
                "-ar", "16000",    # 16kHz
                "-f", "wav",
                out_path
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with open(out_path, "rb") as f:
            wav_bytes = f.read()
            
        # 🔽🔽🔽 ONLY ADDITION STARTS HERE 🔽🔽🔽
        # os.makedirs("processed_audio", exist_ok=True)
        # save_path = f"processed_audio/{uuid.uuid4()}.wav"

        # with open(save_path, "wb") as f:
        #     f.write(wav_bytes)

        # print("Saved processed audio to:", save_path)
        # 🔼🔼🔼 ONLY ADDITION ENDS HERE 🔼🔼🔼

        os.remove(in_path)
        os.remove(out_path)

        return wav_bytes
    
