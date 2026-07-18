# Revenue AI Copilot

> Turning specialized knowledge into faster, better-informed decisions.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![RAG](https://img.shields.io/badge/RAG-LLM-orange)

Revenue AI Copilot is an AI-powered assistant designed to help hotel Revenue Managers access specialized knowledge, understand available information, and make better-informed decisions.

The project uses Revenue Management as its first real-world domain, while exploring a reusable AI architecture that could later be applied to other areas of specialized knowledge.

## Why Revenue Management?

Revenue Management was selected as the first domain because it combines complex documentation, analytical decision-making, and real operational challenges.

Having professional experience in this field allowed the project to be developed around real workflows and realistic user needs instead of hypothetical examples.

## The Problem

Revenue Managers often work with large amounts of information distributed across manuals, guides, reports, policies, and internal documentation.

Finding the right information at the right moment can be slow and inefficient, especially when decisions need to be made quickly.

## The Solution

Revenue AI Copilot transforms specialized documentation into a searchable knowledge base.

Users can ask questions in natural language, and the system retrieves relevant information from the available documents before generating a contextual answer with a Large Language Model.

## Project Status

🟢 Current Version: **v0.1.0**

The project is under active development.

## Current Capabilities

- Load PDF documents related to Revenue Management
- Extract and clean document text
- Divide documents into searchable chunks
- Retrieve relevant information using MinSearch
- Build contextual prompts
- Generate answers using Groq-hosted Large Language Models
- Answer domain-specific Revenue Management questions

## Example Questions

- What is RevPAR?
- Why is market segmentation important?
- What are the benefits of dynamic pricing?
- What is channel management?
- Which KPIs are commonly used in hotel Revenue Management?

## How It Works

```text
Revenue Management PDFs
          ↓
Text extraction and cleaning
          ↓
Document chunking
          ↓
MinSearch indexing
          ↓
Relevant context retrieval
          ↓
Prompt construction
          ↓
Groq LLM
          ↓
Context-aware answer

## Project Structure

```text
revenue-ai-copilot/
│
├── app/
│   ├── data_loader.py
│   ├── ingest.py
│   ├── rag.py
│   ├── rag_helper.py
│   └── search.py
│
├── data/
│   └── raw/
│
├── 01-rag-mvp.ipynb
├── 02-load-pdfs.ipynb
├── 03-rag-working.ipynb
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

The `data/raw/` directory is excluded from version control because the source PDF documents may have their own copyright and distribution restrictions.

## Architecture

Revenue AI Copilot follows a modular Retrieval-Augmented Generation (RAG) architecture.

The project is organized into independent components responsible for:

- Document ingestion
- Text preprocessing
- Chunk generation
- Search and retrieval
- Prompt construction
- LLM interaction

This modular design makes it easier to replace or improve individual components as the project evolves.

## Tech Stack

Python

uv

Jupyter Notebook

Groq API

Large Language Models

Retrieval-Augmented Generation (RAG)

MinSearch

PDF Processing

## Roadmap

Revenue AI Copilot is being developed incrementally, with each version introducing new capabilities while keeping the architecture modular and extensible.

### v0.1 — Knowledge Base ✅

The first milestone focuses on building a complete Retrieval-Augmented Generation (RAG) pipeline.

**Completed**

- PDF ingestion
- Text extraction and cleaning
- Document chunking
- MinSearch retrieval
- Prompt construction
- Groq LLM integration
- Functional RAG pipeline

---

### v0.2 — Semantic Search

The next step is improving information retrieval through semantic search.

**Planned**

- Generate document embeddings
- Introduce vector search
- Compare lexical and semantic retrieval
- Improve retrieval relevance

---

### v0.3 — Reliable Answers

Focus on making answers more reliable and measurable.

**Planned**

- Add source citations
- Improve prompt engineering
- Create an evaluation dataset
- Measure retrieval and answer quality
- Reduce unsupported answers

---

### v0.4 — User Experience

Transform the prototype into an interactive application.

**Planned**

- Build a Streamlit interface
- Add a conversational chat experience
- Support document uploads
- Display retrieved sources
- Add session history

---

### v0.5 — AI Copilot

Move beyond question answering towards an intelligent assistant.

**Planned**

- Summarize specialized documents
- Compare information across documents
- Identify relevant policies and strategies
- Assist with domain-specific workflows
- Introduce agent-based functionality

---

### v1.0 — Production MVP

First production-ready release.

**Goals**

- Production-ready application
- Persistent knowledge base
- Reliable evaluation pipeline
- Public deployment
- Complete technical documentation

---

## Long-Term Vision

Revenue AI Copilot is the first implementation of a broader AI architecture designed to work with specialized knowledge.

Revenue Management was selected as the initial domain because it combines complex documentation, data-driven decision-making, and real business expertise. This makes it an ideal environment for validating Retrieval-Augmented Generation (RAG), semantic search, and AI-assisted decision support.

The long-term vision is to build a reusable architecture that can be adapted to other knowledge-intensive domains such as Finance, Human Resources, Legal, Operations, or Customer Success, while maintaining reliable retrieval, transparent source attribution, and practical business value.

---

## Future Development

Revenue AI Copilot will continue evolving as new AI capabilities are incorporated throughout the project.

Future versions will focus on semantic retrieval, evaluation, AI agents, and practical decision-support features for knowledge-intensive domains.

---

## Disclaimer

Revenue AI Copilot is currently an educational and portfolio project under active development.

Although the system generates answers based on the provided documentation, its responses should not replace professional judgment, internal company policies, or validated business data.

