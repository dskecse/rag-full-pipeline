# RAG Full Pipeline

A Retrieval-Augmented Generation (RAG) system over PDFs with a comprehensive evaluation pipeline.

## TODO

1. Parse PDFs using different text-based parsers.
2. Chunk extracted text with different combination parameters (`chunk_size` + `overlap_size`).
3. Use different embedding models to embed chunks into a vector DB.
4. Generate a synthetic dataset of questions from chunks using LLM and label synthetic questions and chunk IDs.
5. Use LLM-as-a-Judge technique to evaluate the questions generated for a synthetic Q&A (dataset).
6. Evaluate performance using **retrieval metrics** such as Recall@k, Precision@k and MRR.
7. Use reranking to improve the best combination of techniques for top-k retrieval (optional).
8. Evaluate performance with and without reranking.
9. Pick the best combinations of chunking methods, embedding models and **retrieval methods** (BM25, vector search, hybrid approach).
10. Attach an LLM to the Retriever using prompt engineering.
11. Evaluate generated answers using **generation metrics** such as Faithfulness and Relevance.

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
```
