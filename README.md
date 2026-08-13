# Revenue AI Copilot

> Turning specialized Revenue Management knowledge into fast, grounded, and traceable answers.

Revenue AI Copilot is a Retrieval-Augmented Generation (RAG) application designed to help hotel Revenue Management professionals access specialized knowledge through natural-language questions.

The system retrieves relevant information from a curated Revenue Management knowledge base and uses a Large Language Model to generate answers grounded in the retrieved documentation.

The project was developed as part of the **DataTalksClub LLM Zoomcamp** and demonstrates a complete RAG workflow including document ingestion, semantic retrieval, retrieval evaluation, LLM evaluation, a conversational interface, user feedback, and application monitoring.

---

## Problem Description

Hotel Revenue Management involves working with large amounts of specialized information covering topics such as:

- Pricing strategies
- Demand forecasting
- Market segmentation
- Distribution channels
- Revenue KPIs
- Revenue optimization

This information is often distributed across manuals, guides, reports, and other documentation.

Finding the right information quickly can be difficult, particularly when Revenue Managers need to make decisions based on specific business situations.

Revenue AI Copilot addresses this problem by transforming specialized Revenue Management documents into a searchable knowledge base.

Users can ask questions in natural language and receive answers grounded in the retrieved documentation, including references to the original sources and pages.

---

## Why Revenue Management?

Revenue Management was selected because it combines complex documentation, analytical decision-making, pricing strategy, forecasting, distribution, and real operational challenges.

Professional experience in this domain also made it possible to develop the project around realistic Revenue Management questions and workflows rather than hypothetical examples.

The architecture itself is domain-independent and could later be adapted to other knowledge-intensive business areas.

---

## Application

Revenue AI Copilot provides a conversational Streamlit interface where users can ask Revenue Management questions.

The application includes:

- Conversational chat interface
- Semantic knowledge retrieval
- Grounded LLM-generated answers
- Source and page attribution
- Retrieved-source similarity scores
- Example questions
- Conversation history
- User feedback (`Helpful` / `Not helpful`)
- Application monitoring dashboard

### Example Questions

- What is RevPAR?
- What is hotel Revenue Management?
- How does dynamic pricing work?
- Why is market segmentation important?
- How can hotels improve revenue during periods of low demand?
- What is channel management?

---

## RAG Architecture

The current application follows this pipeline:

```text
Revenue Management PDFs
          ↓
PDF ingestion
          ↓
Text extraction & cleaning
          ↓
Document chunking
          ↓
Embedding generation
          ↓
Persistent semantic index
          ↓
Semantic Search (Top-5)
          ↓
Context construction
          ↓
Groq-hosted LLM
          ↓
Grounded answer
          ↓
Source attribution
          ↓
Streamlit interface
          ↓
Feedback & Monitoring
```

The application separates ingestion, retrieval, generation, evaluation, and monitoring into independent components.

---

## Knowledge Base

The current knowledge base consists of specialized Hotel Revenue Management PDF documents.

During ingestion, the documents are:

1. Loaded from the source directory.
2. Extracted page by page.
3. Cleaned and normalized.
4. Split into smaller chunks.
5. Assigned metadata including source document, page, and chunk ID.
6. Converted into embeddings for semantic retrieval.

The current knowledge base contains:

**183 PDF pages → 358 searchable chunks**

The original PDFs are not included in the public repository because source documents may have their own copyright and redistribution restrictions.

Users wishing to reproduce the project should place their permitted source PDFs inside:

```text
data/raw/
```

and rebuild the semantic index.

---

## Semantic Search

The production retrieval system uses semantic search.

Document embeddings are generated once during index construction and stored in a persistent semantic index.

At query time:

1. The user question is converted into an embedding.
2. Its similarity with the indexed document chunks is calculated.
3. The most relevant chunks are retrieved.
4. The Top-5 results are passed to the RAG pipeline.

Persisting the document embeddings prevents the entire knowledge base from being embedded every time the application starts.

---

## Retrieval Evaluation

A dedicated evaluation dataset containing **50 Revenue Management questions** was created from the knowledge base.

Each evaluation question contains a known relevant document, allowing retrieval quality to be measured using:

- **Hit Rate@5**
- **MRR@5 (Mean Reciprocal Rank)**

Multiple retrieval strategies were evaluated.

| Retrieval Method | Hit Rate@5 | MRR@5 |
|---|---:|---:|
| Keyword Search | 0.7800 | 0.6907 |
| Semantic Search | 0.8800 | 0.7657 |
| Hybrid Search | 0.9000 | 0.7397 |

Additional hybrid weighting experiments were performed:

| Semantic / Keyword Weight | Hit Rate@5 | MRR@5 |
|---|---:|---:|
| 0.6 / 0.4 | 0.8800 | 0.7517 |
| 0.7 / 0.3 | 0.8800 | 0.7417 |
| 0.8 / 0.2 | 0.8800 | 0.7617 |

Although Hybrid Search achieved the highest Hit Rate@5 in one experiment, Semantic Search produced the strongest overall MRR and provided a simpler production retrieval architecture.

Semantic Search was therefore selected for the final application.

---

## End-to-End RAG Evaluation

The complete RAG pipeline was evaluated using an **LLM-as-a-Judge** approach.

A sample of 20 evaluation questions was used to assess four dimensions:

- Relevance
- Groundedness
- Completeness
- Hallucination safety

### Results

| Metric | Average Score |
|---|---:|
| Relevance | 4.65 / 5 |
| Groundedness | 4.65 / 5 |
| Completeness | 4.65 / 5 |
| Hallucination Safety | 4.75 / 5 |

Most evaluated answers received maximum scores.

Two weaker cases were manually inspected. The analysis showed that some failures were caused not only by retrieval quality, but also by evaluation questions requesting information broader than what was explicitly supported by their assigned ground-truth chunks.

Prompt constraints were subsequently strengthened to reduce unsupported extrapolation.

Top-3 and Top-5 retrieval contexts were also compared. Top-3 reduced some unsupported information but slightly decreased relevance and completeness, so **Top-5 was retained** for the final pipeline.

---

## Grounded Generation

Revenue AI Copilot is explicitly instructed to answer using only the retrieved context.

The generation prompt requires the model to:

- Focus on the user's specific question.
- Use only claims supported by retrieved documentation.
- Avoid external Revenue Management knowledge.
- Avoid unsupported recommendations or consequences.
- Respect conditions such as low demand, high demand, or peak periods.
- Prefer concise answers over unnecessary extrapolation.
- Cite the relevant source and page.
- State when the retrieved context is insufficient.

This helps reduce hallucinations and keeps answers traceable to the underlying knowledge base.

---

## User Feedback

Users can evaluate individual answers directly from the chat interface using:

- 👍 Helpful
- 👎 Not helpful

Feedback is associated with the corresponding interaction and persisted in a local SQLite database.

This provides a foundation for identifying weak answers and improving the RAG system over time.

---

## Monitoring

The application records operational information for each interaction, including:

- Timestamp
- User question
- Generated answer
- Response latency
- Number of retrieved sources
- User feedback

Monitoring data is stored in SQLite.

A dedicated Streamlit monitoring page provides summary metrics and visualizations covering:

1. Questions over time
2. Response latency over time
3. User feedback distribution
4. Retrieved sources per question
5. Latency distribution

The dashboard also displays overall metrics such as total questions, average latency, feedback responses, and positive feedback.

---

## Project Structure

```text
revenue-ai-copilot/
│
├── app/
│   ├── build_index.py
│   ├── data_loader.py
│   ├── ingest.py
│   ├── monitoring.py
│   ├── rag.py
│   ├── rag_helper.py
│   ├── search.py
│   └── semantic_search.py
│
├── pages/
│   └── 01-monitoring.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   └── semantic_index.json
│   └── monitoring/
│       └── revenue_ai_copilot.db
│
├── 01-rag-mvp.ipynb
├── 02-load-pdfs.ipynb
├── 03-rag-working.ipynb
├── 04-semantic-search.ipynb
├── 05-evaluation.ipynb
│
├── streamlit_app.py
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
└── .gitignore
```

---

## Notebooks

The notebooks document the development and experimentation process.

### `01-rag-mvp.ipynb`

Initial Retrieval-Augmented Generation prototype.

### `02-load-pdfs.ipynb`

PDF loading and document ingestion experiments.

### `03-rag-working.ipynb`

Working RAG pipeline and retrieval experiments.

### `04-semantic-search.ipynb`

Semantic retrieval and embedding experiments.

### `05-evaluation.ipynb`

Evaluation pipeline including:

- Evaluation dataset generation
- Keyword retrieval evaluation
- Semantic retrieval evaluation
- Hybrid retrieval experiments
- Hit Rate and MRR
- End-to-end RAG evaluation
- LLM-as-a-Judge
- Error analysis

---

## Tech Stack

- **Python**
- **Streamlit** — application interface and monitoring dashboard
- **OpenAI API** — embedding generation
- **Groq API** — LLM inference
- **SQLite** — interaction and feedback monitoring
- **Pandas** — monitoring data processing
- **PyPDF** — PDF ingestion
- **NumPy** — semantic similarity calculations
- **MinSearch / lexical retrieval** — retrieval experiments
- **Jupyter Notebook** — experimentation and evaluation
- **uv** — dependency and environment management

---

## Installation

Clone the repository:

```bash
git clone <https://github.com/inetke/revenue-ai-copilot>
cd revenue-ai-copilot
```

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

Do not commit this file to version control.

---

## Adding the Knowledge Base

Place the Revenue Management PDF documents inside:

```text
data/raw/
```

Then build the semantic index:

```bash
uv run python -m app.build_index
```

A persistent semantic index will be created under:

```text
data/processed/semantic_index.json
```

---

## Running the Application

Start the Streamlit application:

```bash
uv run streamlit run streamlit_app.py
```

Open the URL displayed by Streamlit.

The main page provides the Revenue AI Copilot chat interface.

The **Monitoring** page is available from the Streamlit navigation menu.

---

## Running with Docker

The application can also be executed inside a Docker container for a reproducible environment.

Build the Docker image:

```bash
docker build -t revenue-ai-copilot .
```

Run the container using the required API keys and mounting the local knowledge base:

```bash
docker run --rm \
  -p 8501:8501 \
  --env-file .env \
  -v "$(pwd)/data/raw:/app/data/raw:ro" \
  revenue-ai-copilot
```

The application will be available on port `8501`.

If the semantic index does not exist, the application automatically builds it from the PDF documents available in `data/raw/`.

The source documents are mounted as a read-only Docker volume and are not included in the Docker image.

---

## Environment Variables

The application requires:

```text
OPENAI_API_KEY
GROQ_API_KEY
```

`OPENAI_API_KEY` is used for semantic embeddings.

`GROQ_API_KEY` is used for LLM answer generation.

Secrets must not be committed to Git.

---

## Current Status

- [x] PDF ingestion
- [x] Text preprocessing
- [x] Document chunking
- [x] Keyword retrieval
- [x] Semantic retrieval
- [x] Persistent semantic index
- [x] Retrieval evaluation
- [x] Hybrid retrieval experiments
- [x] End-to-end RAG evaluation
- [x] LLM-as-a-Judge evaluation
- [x] Source attribution
- [x] Streamlit chat interface
- [x] Conversation history
- [x] Example questions
- [x] User feedback
- [x] SQLite interaction logging
- [x] Monitoring dashboard
- [x] Docker containerization
- [ ] Public deployment

---

## Future Development

Potential future improvements include:

- Query rewriting
- More advanced re-ranking
- Larger domain-specific knowledge bases
- Automated evaluation pipelines
- Improved monitoring and analytics
- Document upload and ingestion from the interface
- Conversation-aware retrieval
- Agent-based Revenue Management workflows
- Integration with live hotel operational data

---

## Long-Term Vision

Revenue AI Copilot is the first implementation of a broader architecture for AI-assisted access to specialized business knowledge.

Revenue Management provides a useful environment for validating RAG, semantic retrieval, grounded generation, evaluation, and monitoring because it combines complex documentation with real business decision-making.

The same architecture could eventually be adapted to other knowledge-intensive domains while maintaining reliable retrieval, transparent source attribution, and measurable answer quality.

---

## Disclaimer

Revenue AI Copilot is an educational and portfolio project.

The application generates answers based on the documents available in its knowledge base. Its responses should not replace professional judgment, internal company policies, validated operational data, or commercial decision-making.