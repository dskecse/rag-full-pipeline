from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid

from pydantic import BaseModel


class Chunk(BaseModel):
    """Represents a text chunk."""
    id: str
    text: str
    page_number: int
    chunk_index: int
    method: str


class TextChunker(ABC):
    """Abstract base class for text chunkers."""

    @abstractmethod
    def chunk_text(self, pages: list[dict[str, any]], **kwargs) -> list[Chunk]:
        """Chunk text into smaller pieces."""
        pass


class FixedSizeChunker(TextChunker):
    """Chunks text into fixed-size pieces."""

    def chunk_text(self, pages: list[dict[str, any]],
                   chunk_size: int,
                   overlap_size: int) -> list[Chunk]:
        """Chunk text into fixed-size pieces with overlap."""
        if overlap_size >= chunk_size:
            raise ValueError(f"Overlap ({overlap_size}) should be less than chunk size ({chunk_size})")

        chunks = []
        chunk_index = 0
        stride = chunk_size - overlap_size

        for page in pages:
            page_num = page["page_number"]
            text = page["text"] # .replace("\n\n", " ").replace("\n", " ")

            if not text.strip():
                continue

            for i in range(0, len(text), stride):
                chunk_text = text[i : i + chunk_size]

                # Ignore chunks shorter than 30 chars
                if len(chunk_text.strip()) > 30:
                    chunk = Chunk(
                        id=str(uuid.uuid4()),
                        text=chunk_text,
                        page_number=page_num,
                        chunk_index=chunk_index,
                        method="fixed_size",
                    )
                    chunks.append(chunk)
                    chunk_index +=1

        return chunks


class Chunker:
    def __init__(self):
        self.chunkers = {
            "fixed_size": FixedSizeChunker(),
            "sentence": None,
            "semantic": None,
        }

    def chunk_text(self, pages: list[dict[str, any]],
                   chunking_method: str,
                   **chunking_kwargs) -> list[Chunk]:
        """Chunk provided text with a specified chunking method."""
        if chunking_method not in self.chunkers:
            raise ValueError(f"Unknown chunking method: {chunking_method}")

        print(f"Chunking text with '{chunking_method}' chunking method")
        print(f"Chunking options: {chunking_kwargs}")

        chunker = self.chunkers[chunking_method]
        chunks = chunker.chunk_text(pages, **chunking_kwargs)

        print(f"Created {len(chunks)} chunks")

        return chunks
