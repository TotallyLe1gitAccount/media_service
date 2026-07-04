import pytest
import re
from API.utils.path_generator import (
    generate_processed_path, 
    generate_raw_path
    )

def test_generate_raw__path():
    pattern = r"uploads/raw/[0-9a-fA-F-]{36}\.mp4"
    result = generate_raw_path()
    assert re.match(pattern, result) is not None

def test_generate_processed_path():
    pattern = r"uploads/processed/p_[0-9a-fA-F-]{36}\.mp4"
    result = generate_processed_path()
    assert re.match(pattern, result) is not None



