# Refract

Advanced NLP + RAG based audience intelligence engine for systems programming discussions. Collects and analyzes ~46,000 real developer comments from YouTube and Stack Overflow, enriches them with sentiment analysis, keyword extraction, named entity recognition, and topic modeling, then indexes everything into a vector database to support grounded question answering, semantic retrieval, and evidence-backed insights.

---

## What it does

You ask a question about systems programming. Refract retrieves the most relevant real developer comments and Stack Overflow answers from its dataset, generates a grounded answer using only that evidence, and shows you exactly which discussions it used including sentiment breakdown, keyword frequency, and a side-by-side comparison of what YouTube developers vs Stack Overflow experts said.

If the question is outside the scope of the dataset, it falls back to a local Ollama model and clearly labels the response as such.

---

## Stack

- **NLP** - VADER, RoBERTa, KeyBERT, spaCy, BERTopic
- **Embeddings** - sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB** - Weaviate (Docker)
- **LLM** - Ollama (llama3.2:3b)
- **Interface** - Streamlit
- **Monitoring** - MLflow

---

## Requirements

- Python 3.12+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com)

---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/siinzn/Refract.git
cd Refract
```

**2. Create and activate virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Install spaCy model**

```bash
python -m spacy download en_core_web_md
```

**5. Pull Ollama model**

Make sure Ollama is installed and running, then:

```bash
ollama pull llama3.2:3b
```

**6. Set up environment variables**

Create a `.env` file at the project root:

```
YOUTUBE_API_KEY=your_youtube_data_api_v3_key
```

YouTube API key is only needed if you want to rerun data collection. If you are using the existing dataset it is not required.

**7. Start Weaviate**

```bash
docker compose up -d
```

This starts Weaviate at `localhost:8080`. Your data persists in a Docker volume so you only need to index once.

---

## Running the pipeline

If you are using the existing dataset in `data/raw/`, run the full pipeline to preprocess, analyze, embed, and index everything into Weaviate:

```bash
python pipeline.py
```

This will take around 2-3 hours due to the analysis stage (sentiment, keywords, NER, topic modeling on 46,000 rows). Run it once, then the Weaviate index persists and you never need to run it again unless you want to rebuild.

---

## Running the app

Once the pipeline is complete and Docker is running:

```bash
streamlit run main.py
```

Opens at `http://localhost:8501`.

---

## Data collection (optional)

If you want to recollect data from scratch:

```bash
# Collect YouTube video IDs
python -m src.collection.search

# Collect YouTube comments
python -m src.collection.comments
```

Stack Overflow data was collected manually via [Stack Exchange Data Explorer](https://data.stackexchange.com). The SQL query used is documented in `projectplan.md`.

---

## Project structure

```
refract/
├── data/
│   ├── raw/                  # raw collected data
│   ├── processed/            # cleaned and enriched data
│   ├── embeddings/           # saved embeddings if any
│   └── evaluation/           # evaluation results
├── src/
│   ├── collection/           # YouTube API collection
│   ├── preprocessing/        # text cleaning pipeline
│   ├── analysis/             # NLP enrichment pipeline
│   ├── embeddings/           # embedding generation
│   ├── vector_db/            # Weaviate indexing
│   ├── retrieval/            # Hybrid retrieval
│   └── rag/                  # RAG chain and routing
├── pipeline.py               # end to end pipeline
├── main.py                   # Streamlit interface
├── docker-compose.yml        # Weaviate + Ollama
└── requirements.txt
```

---

## MLflow monitoring

To view the MLflow experiment dashboard:

```bash
mlflow ui
```

Opens at `http://localhost:5000`. Every RAG query is automatically logged.
