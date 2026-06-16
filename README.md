# RAG Full Pipeline

A Retrieval-Augmented Generation (RAG) system over PDFs with a comprehensive evaluation pipeline.

## TODO

- [x] Parse PDFs using different text-based parsers.
- [ ] Chunk extracted text with different combination parameters (`chunk_size` + `overlap_size`).
- [ ] Use different embedding models to embed chunks into a vector DB.
- [ ] Generate a synthetic dataset of questions from chunks using LLM and label synthetic questions and chunk IDs.
- [ ] Use LLM-as-a-Judge technique to evaluate the questions generated for a synthetic Q&A (dataset).
- [ ] Evaluate performance using **retrieval metrics** such as Recall@k, Precision@k and MRR.
- [ ] Use reranking to improve the best combination of techniques for top-k retrieval (optional).
- [ ] Evaluate performance with and without reranking.
- [ ] Pick the best combinations of chunking methods, embedding models and **retrieval methods** (BM25, vector search, hybrid approach).
- [ ] Attach an LLM to the Retriever using prompt engineering.
- [ ] Evaluate generated answers using **generation metrics** such as Faithfulness and Relevance.

## Prerequisites

* Git
* Python 3.13.x

## Setup

```sh
git clone https://github.com/dskecse/rag-full-pipeline
cd $_
python3.13 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Run

```sh
python3 main.py
```

## Comprehensive Experimental Combinations

The following table shows all components and variations tested in the RAG system evaluation:

### System Components and Variations

| Component       | Options Tested | Details |
| :-------------- | :------------- | :------ |
| **PDF Parsing** | docling        |         |
|                 | pdfplumber     |         |
|                 | PyMuPDF        |         |
|                 | pypdf          |         |
