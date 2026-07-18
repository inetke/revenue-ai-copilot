# Revenue AI Copilot

> **Turning specialized knowledge into faster, better-informed decisions.**

Revenue AI Copilot is an AI-powered assistant designed to help hotel Revenue Managers access specialized knowledge, understand available information, and make better-informed decisions.

The project uses Revenue Management as its first real-world domain, while exploring a reusable AI architecture that could later be applied to other areas of specialized knowledge.

## The Problem

Revenue Managers often work with large amounts of information distributed across manuals, guides, reports, policies, and internal documentation.

Finding the right information at the right moment can be slow and inefficient, especially when decisions need to be made quickly.

## The Solution

Revenue AI Copilot transforms specialized documentation into a searchable knowledge base.

Users can ask questions in natural language, and the system retrieves relevant information from the available documents before generating a contextual answer with a Large Language Model.

## Current Version

**Version:** `v0.1.0`  
**Status:** Early functional prototype

The current version demonstrates a complete Retrieval-Augmented Generation pipeline using Revenue Management documentation.

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