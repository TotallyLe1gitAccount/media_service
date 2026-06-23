import anyio

class VideoSaver:
    async def save_file(self, file, path: str):
        def _write():
            with open(path, "wb") as buffer:
                while chunk := file.file.read(1024 * 1024):
                    buffer.write(chunk)

        await anyio.to_thread.run_sync(_write)