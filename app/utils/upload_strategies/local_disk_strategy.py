import os
from typing import Optional
from pathlib import Path
import logging

from .upload_stategy import UploadStrategy
from app.config import BASE_DIR
    

class LocalDiskUploadStrategy(UploadStrategy):
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def upload(self, file, file_name: str) -> Optional[str]:
        
        # Create the full path for the file
        full_path = self.upload_dir / file_name
        
        # Write the file to disk
        with open(full_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Return the relative path
        # return os.path.relpath(full_path, start=self.upload_dir.parent)
        return os.path.relpath(full_path, start=self.upload_dir.parent.parent)

        
        # file_path = os.path.join(self.upload_dir, file_name)
        
        # # Read the file content asynchronously
        # content = await file.read()
        # with open(file_path, "wb") as buffer:
        #     buffer.write(content)
        
        # return file_path
    
    def delete(self, file_path: str) -> bool:
        try:
            # Convert the relative path to an absolute path
            absolute_path = BASE_DIR / file_path

            # Check if the file exists and delete it
            if os.path.exists(absolute_path):
                os.remove(absolute_path)
                logging.info(f"File deleted: {absolute_path}")
                return True
            else:
                logging.warning(f"File not found: {absolute_path}")
                return False
        except Exception as e:
            logging.error(f"Error deleting file {absolute_path}: {e}")
            return False


    # def delete(self, file_path: str) -> bool:
        
    #     # Convert the relative path to an absolute path
    #     base_dir = Path(__file__).resolve().parent.parent
    #     absolute_path = base_dir / file_path
        
    #     # Check if the file exists and delete it
    #     if os.path.exists(absolute_path):
    #         os.remove(absolute_path)
    #         return True
    #     return False
    
    
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        #     return True
        # return False
        
    