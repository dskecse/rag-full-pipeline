import os
import json
from pathlib import Path
from pprint import pprint

from src.pdf_processor import PDFProcessor
from src.chunker import Chunk, Chunker

_all_parsers = [
    "docling",
    "pdfplumber",
    "pymupdf",
    "pypdf",
]


def _print_summary(pages: list[str]) -> None:
    print("First page content:")
    print("-" * 60)
    pprint(pages[0])


def _print_chunking_summary(chunks: list[Chunk]) -> None:
    print("First 2 chunks:")
    print("-" * 60)
    pprint(chunks[:2])


def _save_extracted_text(pages: list, parser: str, orig_filename: str) -> None:
    # Create a directory (do not raise if already present)
    os.makedirs(os.path.join("data", "extracted_texts"), exist_ok=True)

    orig_filename_without_ext = Path(orig_filename).stem
    new_filename = f"{parser}_{orig_filename_without_ext}.json"
    output_path = os.path.join("data", "extracted_texts", new_filename)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(pages, file, indent=2, ensure_ascii=False)

    print(f"Extracted text saved to {output_path}")


def _save_chunks(chunks: list[Chunk], filename: str) -> None:
    # Create a directory (do not raise if already present)
    os.makedirs(os.path.join("data", "chunks"), exist_ok=True)

    output_path = os.path.join("data", "chunks", filename)

    serialized_chunks = []
    for chunk in chunks:
        serialized_chunks.append(chunk.model_dump())

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(serialized_chunks, file, indent=2, ensure_ascii=False)

    print(f"Saved {len(chunks)} chunks to {output_path}")


def extract_text_from_pdf(pdf_path: str = "fy10syb.pdf", parsers: list[str] = _all_parsers) -> dict[str, list]:
    """
    Extract text from a PDF using different parsers for comparison later.
    """
    if len(parsers) == 0:
        raise ValueError("'parsers' param cannot be empty")

    processor = PDFProcessor()

    print("Testing text extraction from PDF\n")

    pages_by_parser = {}

    for parser in parsers:
        print(f"\nTesting parser: {parser}")

        try:
            pages = processor.process_pdf(
                pdf_path=pdf_path,
                parser_name=parser
            )
            pages_by_parser[parser] = pages

            _print_summary(pages=pages)
        except Exception as e:
            print(f"Error with parser {parser}: {e}\n")

        _save_extracted_text(pages, parser=parser, orig_filename=pdf_path)

    return pages_by_parser


def perform_chunking(pages: dict[str, list]) -> dict[str, list[Chunk]]:
    configurations = [
        {"chunking": "fixed_size", "chunk_size": 128, "overlap_size": 32},
        {"chunking": "fixed_size", "chunk_size": 256, "overlap_size": 50},
        {"chunking": "fixed_size", "chunk_size": 512, "overlap_size": 100},
        # {"chunking": "sentence", "max_sentences": 3},
        # {"chunking": "semantic", "max_tokens": 300},
    ]

    chunker = Chunker()

    print("\n\nTesting extracted text chunking")

    chunk_sets = {}

    for parser, pages in pages.items():
        print(f"\nParser: {parser}")
        for config in configurations:
            print(f"\nTesting chunking configuration: {config}")

            # Extract chunking options
            chunking_options = {k: v for k, v in config.items() if k != "chunking"}

            try:
                chunks = chunker.chunk_text(
                    pages=pages,
                    chunking_method=config["chunking"],
                    **chunking_options
                )

                config_name = f"{parser}_{config["chunking"]}"
                if chunking_options:
                    options = "_".join([f"{k}{v}" for k, v in chunking_options.items()])
                    config_name += f"_{options}"

                chunk_sets[config_name] = chunks

                _print_chunking_summary(chunks=chunks)
                _save_chunks(chunks, filename=f"{config_name}.json")
            except Exception as e:
                print(f"Error with configuration {config}: {e}\n")

    return chunk_sets


if __name__ == "__main__":
    pdf_path = "fy10syb.pdf"
    pages_by_parser = extract_text_from_pdf(pdf_path=pdf_path)
    chunk_sets = perform_chunking(pages=pages_by_parser)
