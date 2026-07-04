import uuid
def generate_raw_path():
        return f"uploads/raw/{uuid.uuid4()}.mp4"
    
def generate_processed_path():
        return "uploads/processed/p_" + f"{uuid.uuid4()}" + ".mp4"
        