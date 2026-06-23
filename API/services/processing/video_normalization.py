from ffmpeg_normalize import FFmpegNormalize
import subprocess
import json
import os

class VideoNormalizer:
    def normalize_video(self, file_path : str,
        output_path : str,
        crf: int = 23,
        fps: int = 30,
        preset: str = "medium",
        codec: str = "libx264",
        audio_norm : bool = True,
        lufs: float = -14.0
        ):

        cmd = [
                "ffmpeg",
                "-y",
                "-i", file_path,
                "-vf", f"fps={fps}",
                "-c:v", codec,
                "-crf",str(crf),
                "-preset", preset,
            ]
        if audio_norm:
            cmd += ["-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11"]

        cmd.append(output_path)
        process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )

        if process.returncode != 0:
            print("FFMPEG ERROR:\n", process.stderr)
            raise RuntimeError(process.stderr)

        return output_path

    def probe(self, file_path):
        file_path = os.path.abspath(file_path)

        print("FILE:", file_path)
        print("EXISTS:", os.path.exists(file_path))

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        process = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-print_format", "json",
                "-show_streams",
                "-show_format",
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(f"""
    FFPROBE ERROR

    file: {file_path}

    stderr:
    {process.stderr}
    """)

        try:
            return json.loads(process.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(f"""
    FFPROBE OUTPUT IS NOT JSON

    stdout:
    {process.stdout}

    stderr:
    {process.stderr}
    """)
