import subprocess
import json
import asyncio

async def probe(file_path):
    process = await asyncio.create_subprocess_exec(
        "ffprobe",
        "-v",
        "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(stderr.decode())
    

    return json.loads(stdout.decode())