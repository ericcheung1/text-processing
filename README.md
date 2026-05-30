# Word processing-as-a-service - NLP Inference API

A lightweight, production‑style REST API built with FastAPI for serving natural language processing (NLP) models for tasks such as sentiment analysis. The system and models are designed for deployment on constrained environments such as a low-memory VPS. This project emphasizes modularity, scalability, and ease of deployment.

Currently supported NLP tasks: sentiment analysis, keyword extractions.

This project generalizes my earlier Canucks sentiment analysis work @ [canucks-sentiment](https://github.com/ericcheung1/canucks-sentiment). It breaks the monolithic repo which combined Reddit scraping, sentiment analysis, and a Flask display layer into a dedicated inference API designed to serve multiple clients.

Check out some models/endpoints in action @ [word-processor-dot-com](https://github.com/ericcheung1/word-processor-dot-com).

- [Architecture](#architecture)
- [Deployment](#deployment)
- [Example Requests](#example-requests)
- [Run Locally](#run-locally)
- [Models](#models)

## Architecture

![Architecture](docs/wpaas-diagram.png)

The system is designed as a collection of isolated inference services to keep models modular and independently deployable.

- Service-per-model design: each NLP task runs as its own FastAPI app
- Shared schema layer: common Pydantic models ensure consistent input validation across services
- Containerized services: each endpoint builds into its own Docker image
- Extensible structure: new NLP tasks can be added without modifying existing services

This structure prioritizes modularity and makes it easier to scale, swap, or deploy models independently.

## Deployment

The system is currently deployed on a single low-memory VPS using the following:

- CI/CD: GitHub Actions builds and deploys container images
- Orchestration: Docker Compose manages the multi-service setup
- Reverse proxy: Caddy handles HTTPS and request routing

This setup keeps infrastructure simple while still following production-style deployment patterns.

## Example Requests

### Input

Input payloads are consistant across all models since they share a common Pydantic schema.

```
Request: # Can also be sent without text_id field

{
  "texts": [
    {
      "text": "I love eating nachos!",
      "text_id": "abc123"
    },
    {
      "text": "I hate eating nachos!",
      "text_id": "def345"
    }
  ]
}
```

### Output

- POST /sentiment
```
{
  "sentiment": [
    {
      "sentiment_classification": "POSITIVE",
      "sentiment_confidence": [
        0.0003287792205810547,
        0.99951171875
      ],
      "text_id": "abc123"
    },
    {
      "sentiment_classification": "NEGATIVE",
      "sentiment_confidence": [
        0.9765625,
        0.023345947265625
      ],
      "text_id": "def345"
    }
  ]
}
```
 Note: The first element of the `sentiment_confidence` array is the negative sentiment score and second element is the positive sentiment score.

 - POST /keywords

 ```
{
  "keywords": [
    {
      "text_id": "abc123",
      "extracted_keywords": [
        {
          "keyword": "love eating nachos",
          "score": 0.016559150827736194
        },
        {
          "keyword": "eating nachos",
          "score": 0.04940384002065631
        }
      ]
    },
    {
      "text_id": "def345",
      "extracted_keywords": [
        {
          "keyword": "hate eating nachos",
          "score": 0.016559150827736194
        },
        {
          "keyword": "eating nachos",
          "score": 0.04940384002065631
        }
      ]
    }
  ]
}
 ```
Note: A lower `score` value means higher relevance.

## Run Locally

This repository uses Git LFS to store weights for models that contain them. Make sure Git LFS is installed with `git lfs install` before cloning and running the follow model(s):

- Sentiment

### With Source
Clone the repo, from the project root, install dependencies with `pip install -r models/<NLP-task>/requirements.txt`, activate venv, then start server with `uvicorn models.<NLP-task>.main:app --host 0.0.0.0 --port 8000`.

### With Docker
Pull the latest build with `docker pull ghcr.io/ericcheung1/wpaas-<NLP-task>:main`, then start container with `docker run -p 8000:8000 ghcr.io/ericcheung1/wpaas-<NLP-task>:main`.

## Model(s)

### Sentiment

- [DistilBERT](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) for binary POSITIVE/NEGATIVE sentiment classification
- Model weights are included in the repository using Git LFS
- Weights have been converted to .onnx format and FP16 precision for improved loading and inference speeds

### Keywords

- [YAKE](https://github.com/INESCTEC/yake) a lightweight unsupervised automatic keyword extraction method
- Non-ML uses text statistical features (like term frequency, word co-occurrence, word position) to calculate a score for individual words