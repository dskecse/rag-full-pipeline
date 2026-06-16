from pprint import pprint

from src.pdf_processor import PDFProcessor


def extract_text_from_pdf():
    """
    Extract text from a PDF using different parsers for comparison later.
    """

    processor = PDFProcessor()

    print("Testing text extraction from PDF\n")

    configurations = [
        {"parser": "docling"},
        {"parser": "pdfplumber"},
        {"parser": "pymupdf"},
        {"parser": "pypdf"},
    ]

    pdf_path = "fy10syb.pdf"

    for config in configurations:
        print(f"\nTesting configuration: {config}")

        try:
            pages = processor.process_pdf(
                pdf_path=pdf_path,
                parser_name=config["parser"]
            )

            print("First page content:")
            print("-" * 60)
            pprint(pages[0])
        except Exception as e:
            print(f"Error with configuration {config}: {e}\n")


if __name__ == "__main__":
    extract_text_from_pdf()
