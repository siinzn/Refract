# Refract - Project Plan

## Project Overview

Refract is an advanced NLP + RAG based audience intelligence engine focused on large-scale YouTube discussions related to Systems Programming using C/C++.

The system automatically discovers relevant YouTube videos based on predefined systems programming topics, extracts comments and metadata, preprocesses noisy social-media text, and transforms discussions into structured knowledge using NLP techniques.

Instead of functioning as a basic chatbot or sentiment dashboard, Refract focuses on intelligent retrieval, grounded reasoning, topic-level audience analysis, insight generation, and explainable AI behavior over real-world programming discussions.

---

# Main Domain

Systems Programming using C/C++

---

# Sub-Domains

- Modern C++
- Operating Systems
- Multithreading / Concurrency
- Performance Optimization
- Backend / System Design
- Memory Management
- Low-Level Programming

---

# Video Discovery Strategy

The system should automatically search and discover YouTube videos related to the selected systems programming topics instead of using manually hardcoded video links.

## Video Selection Criteria

- Tutorials
- Debate / Opinion Videos
- Advanced Programming Discussions
- Conference Talks
- Beginner Problem Discussions
- Performance Engineering Discussions

## Filtering Strategy

Videos should be filtered based on:

- Comment count
- Relevance to systems programming
- Technical discussion quality
- English language
- Avoid YouTube Shorts
- Avoid low-quality or spam-heavy videos

---

# Dataset Goals

- Around 20 videos
- Around 500 comments per video
- Target dataset size: ~10,000 comments

The dataset should contain discussions from multiple perspectives and experience levels to support meaningful NLP analysis and RAG retrieval.

---

# Dataset Structure

Each dataset entry should contain:

## Video Metadata

- Video ID
- Video Title
- Channel Name
- Upload Date
- Video Likes
- Video URL

## Comment Metadata

- Comment ID
- Parent Comment ID
- Comment Text
- Comment Replies
- Comment Likes
- Comment Timestamp

## NLP Metadata

- Cleaned Comment
- Sentiment Label
- Extracted Keywords
- Named Entities
- Topic Label
- Embedding Reference

---

# NLP Pipeline

The NLP pipeline should preprocess and enrich YouTube discussions using:

- Text Cleaning
- Tokenization
- Stopword Removal
- Lemmatization
- Sentiment Analysis
- Keyword Extraction
- Named Entity Recognition (NER)
- Topic Modeling
- Embedding Generation

---

# RAG Architecture Goals

The Retrieval-Augmented Generation system should support:

- Semantic Search
- Hybrid Retrieval
- Context-Aware Question Answering
- Grounded Response Generation
- Evidence-Based Insights
- Hallucination Reduction
- Topic-Aware Retrieval

The retrieved comments should act as the grounding context for generated responses.

---

# Intended System Capabilities

The system should be able to answer questions such as:

- What frustrates beginner C++ developers?
- What topics create polarized opinions?
- Which concepts are repeatedly described as difficult?
- What are common misconceptions?
- What performance topics are most discussed?
- How do opinions differ between beginner and advanced audiences?
- What tools or frameworks are repeatedly praised or criticized?
- Which systems programming concepts generate the most confusion?
- What learning patterns repeatedly appear in discussions?

---

# System Design Goals

The project should emphasize:

- Modular architecture
- Clean NLP pipeline design
- Strong retrieval quality
- Explainable AI behavior
- Scalable dataset pipeline
- Intelligent audience reasoning
- Analytical insight generation
- Academically strong evaluation

---

# Evaluation Goals

The system should later be evaluated on:

- Retrieval relevance
- Grounded answer quality
- Topic coherence
- Sentiment consistency
- Hallucination reduction
- Retrieval accuracy
- Insight usefulness

---

# Final Product Vision

Refract should function as an intelligent developer audience analysis and reasoning engine capable of understanding large-scale systems programming discussions on YouTube rather than acting as a simple chatbot or visualization dashboard.
