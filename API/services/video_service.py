import uuid
from API.utils.path_generator import (
    generate_processed_path, 
    generate_raw_path)

class VideoService:
    def __init__(self, validator, normalizer, saver, repo):
        self.validator = validator
        self.normalizer = normalizer
        self.saver = saver
        self.repo = repo
     
    async def upload_video(self, file, db):
        path = generate_raw_path()

        ok, error = self.validator.validate_size(file)
        if not ok:
            return error

        ok, error = await self.validator.validate_content(file)
        if not ok:
            return error

        info = self.normalizer.probe(path)

        ok, error = self.validator.validate_metadata(info)
        if not ok:
            return error

        output_path = generate_processed_path()
        final_path = self.normalizer.normalize_video(path, output_path)
        
        return self.repo.create_video(db, file.filename, final_path)