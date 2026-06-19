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
- [ ] Evaluate performance with and without reranking (optional).
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

| Component               | Options                              | Details                       |
| :---------------------- | :----------------------------------- | :---------------------------- |
| **PDF Parsing**         | docling                              |                               |
|                         | pdfplumber                           |                               |
|                         | PyMuPDF                              |                               |
|                         | pypdf                                |                               |
| **Chunking Method**     | Fixed-size (128 chars + 32 overlap)  |                               |
|                         | Fixed-size (256 chars + 50 overlap)  |                               |
|                         | Fixed-size (512 chars + 100 overlap) |                               |
|                         | Sentence-based (3 sentences max)     | Natural sentence boundaries   |
|                         | Semantic (300 tokens max)            | AI-driven semantic boundaries |
| **Embedding Model**     | text-embedding-3-small (1536d)       | OpenAI efficient model        |
|                         | text-embedding-3-large (3072d)       | OpenAI high-performance model |
|                         | GTE-large-en-v1.5 (1024d)            | Alibaba (open-source)         |
| **Vector Database**     | FAISS (local)                        | High-performance local search |
|                         | Pinecone (cloud)                     | Managed vector DB             |
| **Retrieval Method**    | BM25                                 | Keyword-based search          |
|                         | Vector search                        | Semantic similarity search    |
|                         | Hybrid approach (BM25 + Vector)      | Combined approach             |
| **Reranking**           | None                                 | Direct retrieval results      |
|                         | Cohere Rerank                        | TBD                           |
| **Question Generation** | Gemini 3.5 Flash                     | AI-generated questions        |

### Evaluation Metrics

| Metric Category        | Specific Metrics                      | Details                                                  |
| :--------------------- | :------------------------------------ | :------------------------------------------------------- |
| **Retrieval Coverage** | Recall@1, Recall@3, Recall@5          | Are we retrieving any relevant chunks in the top K?      |
| **Retrieval Accuracy** | Precision@1, Precision@3, Precision@5 | How many retrieved chunks are relevant?                  |
| **Ranking Quality**    | MRR (Mean Reciprocal Rank)            | Position of the 1st relevant chunk                       |
| **Performance**        | Average Retrieval Time                | Speed of retrieval operations                            |

### Experimental Scale

| Dimension             |                 Count | Details                                            |
| :-------------------- | --------------------: | :------------------------------------------------- |
| **PDF Parsers**       |                     4 | docling + pdfplumber + PyMuPDF + pypdf             |
| **Chunking Methods**  |                     5 | Fixed-size (3) + Sentence (1) + Semantic (1)       |
| **Embedding Models**  |                     3 | text-embedding-3-{small,large} + gte-large-en-v1.5 |
| **Vector Databases**  |                     1 | FAISS (Facebook AI Similarity Search)              |
| **Retrieval Methods** |         3 per dataset | BM25 + Vector + Hybrid                             |
| **Reranking Options** |                     1 | Without reranking                                  |
| **Questions**         |         20 per method | Separate datasets per chunking method              |
| **Total Experiments** |  **180 combinations** | 4 × 5 × 3 × 1 × 3 × 1 = 180                        |
