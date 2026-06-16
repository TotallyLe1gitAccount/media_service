from ffmpeg_normalize import FFmpegNormalize
import subprocess

def normalize_video(file_path : str,
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
            "-i", file_path,
            "-vf", f"fps={fps}",
            "-c:v", codec,
            "-crf",str(crf),
            "-preset", preset,
        ]
    if audio_norm:
        cmd += ["-af", f"loudnorm=I={lufs}:TP-1.5:LRA=11"]

    cmd.append(output_path)
    subprocess.run(cmd, check=True)