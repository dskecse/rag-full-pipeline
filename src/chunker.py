from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
import uuid

from pydantic import BaseModel
import spacy


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


class SentenceChunker(TextChunker):
    """Chunks text by sentences."""

    def chunk_text(self, pages: list[dict[str, any]],
                   max_sentences: int = 3) -> list[Chunk]:
        """Chunk text by sentences."""
        chunks = []
        chunk_index = 0

        for page in pages:
            page_num = page["page_number"]
            text = page["text"]

            if not text.strip():
                continue

            sentences = re.split(r'(?<=[.!?])\s+', text)
            current_chunk = []

            for sentence in sentences:
                current_chunk.append(sentence.strip())

                if len(current_chunk) >= max_sentences:
                    chunk_text = " ".join(current_chunk)

                    if chunk_text:
                        chunk = Chunk(
                            id=str(uuid.uuid4()),
                            text=chunk_text,
                            page_number=page_num,
                            chunk_index=chunk_index,
                            method="sentence",
                        )
                        chunks.append(chunk)
                        chunk_index +=1

                    current_chunk = []

            # Handle remaining sentences
            if len(current_chunk):
                chunk_text = " ".join(current_chunk)

                if chunk_text:
                    chunk = Chunk(
                        id=str(uuid.uuid4()),
                        text=chunk_text,
                        page_number=page_num,
                        chunk_index=chunk_index,
                        method="sentence",
                    )
                    chunks.append(chunk)
                    chunk_index +=1

        return chunks


class SemanticChunker(TextChunker):
    """Chunks text based on semantic boundaries using spaCy."""

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found, skipping semantic chunking")
            print("To download, run:\n\tpython -m spacy download en_core_web_sm")
            self.nlp = None

    def chunk_text(self, pages: list[dict[str, any]],
                   max_tokens: int = 300) -> list[Chunk]:
        """Chunk text based on sematic boundaries."""
        if not self.nlp:
            print("Skipping semantic chunking")
            return []

        chunks = []
        chunk_index = 0

        for page in pages:
            page_num = page["page_number"]
            text = page["text"]

            if not text.strip():
                continue

            doc = self.nlp(text)
            sentences = list(doc.sents)

            current_chunk = []
            current_tokens = 0

            for sentence in sentences:
                sentence_tokens = len(sentence)

                if current_tokens + sentence_tokens > max_tokens and current_chunk:
                    # Create chunk from current sentences
                    chunk_text = " ".join([s.text for s in current_chunk]).strip()

                    if chunk_text:
                        chunk = Chunk(
                            id=str(uuid.uuid4()),
                            text=chunk_text,
                            page_number=page_num,
                            chunk_index=chunk_index,
                            method="semantic",
                        )
                        chunks.append(chunk)
                        chunk_index +=1

                    current_chunk = [sentence]
                    current_tokens = sentence_tokens
                else:
                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens

            # Handle remaining sentences
            if current_chunk:
                chunk_text = " ".join([s.text for s in current_chunk]).strip()

                if chunk_text:
                    chunk = Chunk(
                        id=str(uuid.uuid4()),
                        text=chunk_text,
                        page_number=page_num,
                        chunk_index=chunk_index,
                        method="semantic",
                    )
                    chunks.append(chunk)
                    chunk_index +=1

        return chunks


class Chunker:
    def __init__(self):
        self.chunkers = {
            "fixed_size": FixedSizeChunker(),
            "sentence": SentenceChunker(),
            "semantic": SemanticChunker(),
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
