from typing import List

def split_to_chunks(content: str= "", size: int = 1000) -> List[str]:
   return [content[i:i+size].ljust(size) for i in range(0, len(content), size)]