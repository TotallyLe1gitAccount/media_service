import subprocess
import json
import os

import subprocess
import json

def probe(file_path):
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