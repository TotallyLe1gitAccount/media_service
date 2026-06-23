import uuid

class VideoService:
    def __init__(self, validator, normalizer, saver, repo):
        self.validator = validator
        self.normalizer = normalizer
        self.saver = saver
        self.repo = repo

    def _generate_path(self, file):
        return f"uploads/raw/{uuid.uuid4()}.mp4"
        
    async def upload_video(self, file, db):
        path = self._generate_path(file)

        await self.validator.validate_size(file)
        await self.validator.validate_content(file)
        await self.saver.save_file(file, path)

        info = self.normalizer.probe(path)

        self.validator.validate_metadata(info)
        output_path = "uploads/processed/p_" + f"{uuid.uuid4()}" + ".mp4"
        final_path = self.normalizer.normalize_video(path, output_path)
        
        return self.repo.create_video(db, file.filename, final_path)