import os
import json
from pathlib import Path
from pprint import pprint

from src.pdf_processor import PDFProcessor


def save_extracted_text(pages: list, parser: str, orig_filename: str) -> None:
    # Create a directory (do not raise if already present)
    os.makedirs(os.path.join("data", "extracted_texts"), exist_ok=True)

    orig_filename_without_ext = Path(orig_filename).stem
    new_filename = f"{parser}_{orig_filename_without_ext}.json"
    output_path = os.path.join("data", "extracted_texts", new_filename)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(pages, file, indent=2, ensure_ascii=False)

    print(f"Extracted text saved to {output_path}")


def extract_text_from_pdf(pdf_path: str = "fy10syb.pdf") -> None:
    """
    Extract text from a PDF using different parsers for comparison later.
    """

    processor = PDFProcessor()

    print("Testing text extraction from PDF\n")

    parsers = [
        "docling",
        "pdfplumber",
        "pymupdf",
        "pypdf",
    ]

    for parser in parsers:
        print(f"\nTesting parser: {parser}")

        try:
            pages = processor.process_pdf(
                pdf_path=pdf_path,
                parser_name=parser
            )

            print("First page content:")
            print("-" * 60)
            pprint(pages[0])
        except Exception as e:
            print(f"Error with parser {parser}: {e}\n")

        save_extracted_text(pages, parser=parser, orig_filename=pdf_path)


if __name__ == "__main__":
    extract_text_from_pdf()
