from abc import ABC, abstractmethod
import time

from docling.document_converter import DocumentConverter
import pdfplumber
import pymupdf
from pypdf import PdfReader


class PDFParser(ABC):
    """Abstract base class for PDF parsers."""

    @abstractmethod
    def extract_text(self, pdf_path: str) -> list[dict[str, any]]:
        """Extract text from PDF with page information."""
        pass


class DoclingParser(PDFParser):
    def extract_text(self, pdf_path: str) -> list[dict[str, any]]:
        """Extract text using docling."""
        pages = []

        result = DocumentConverter().convert(pdf_path)
        document = result.document
        for page_num in range(len(document.pages)):
            # Caveat: page indexing starts with 1 in Docling.
            page_num += 1
            text = document.export_to_text(page_no=page_num)
            pages.append({
                "page_number": page_num,
                "text": text,
                "char_count": len(text),
                "parser": "docling"
            })

        return pages


class PDFPlumberParser(PDFParser):
    def extract_text(self, pdf_path: str) -> list[dict[str, any]]:
        """Extract text using pdfplumber."""
        pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages.append({
                    "page_number": page_num,
                    "text": text,
                    "char_count": len(text),
                    "parser": "pdfplumber"
                })

        return pages


class PyMuPDFParser(PDFParser):
    def extract_text(self, pdf_path: str) -> list[dict[str, any]]:
        """Extract text using PyMuPDF."""
        pages = []

        with pymupdf.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                text = doc.load_page(page_num).get_text()
                pages.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "char_count": len(text),
                    "parser": "pymupdf"
                })

        return pages


class PyPDFParser(PDFParser):
    def extract_text(self, pdf_path: str) -> list[dict[str, any]]:
        """Extract text using pypdf."""
        pages = []

        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            pages.append({
                "page_number": page_num,
                "text": text,
                "char_count": len(text),
                "parser": "pypdf"
            })

        return pages


class PDFProcessor:
    def __init__(self):
        self.parsers = {
            "docling": DoclingParser(),
            "pdfplumber": PDFPlumberParser(),
            "pymupdf": PyMuPDFParser(),
            "pypdf": PyPDFParser(),
        }

    def process_pdf(self, pdf_path: str, parser_name: str) -> list[str]:
        if parser_name not in self.parsers:
            raise ValueError(f"Unknown parser: {parser_name}")

        print(f"Processing PDF with '{parser_name}' parser")

        parser = self.parsers[parser_name]

        start_time = time.perf_counter()
        pages = parser.extract_text(pdf_path)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        print(f"Extracted {len(pages)} pages from PDF")
        print(f"Text extraction using '{parser_name}' parser took {elapsed_time:.6f} seconds")

        return pages
