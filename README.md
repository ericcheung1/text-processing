# Word processing-as-a-service - NLP Inference API

A lightweight REST API built using FastAPI for serving natural language processing (NLP) models such as sentiment analysis. The API exposes simple HTTP endpoint(s) that allow external applications to submit data and receive predictions.

This project is a generalization of my earlier Canucks sentiment analysis project [canucks-sentiment](https://github.com/ericcheung1/canucks-sentiment), where sentiment models were used to analyze fan discussions from Reddit and results were hardcoded in a Flask web app.

### Features

- REST API for ML inference
- Sentiment analysis endpoint
- JSON request/response format
- Containerized with Docker
- Model weights included and stored in Git LFS

## Example Request

POST /sentiment

```
Request: # Can also be sent without text_id field

{
  "texts": [
    {
      "text": "I love to eat nachos!",
      "text_id": "abc123"
    },
    {
      "text": "I hate to eat nachos!",
      "text_id": "def345"
    }
  ]
}

Response: 

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
 Note: first index of the `sentiment_confidence` array is confidence of the text having negative sentiment and second index is confidence of text having positive sentiment

## Run Locally

This repository uses Git LFS to store model weights.
Make sure Git LFS is installed with `git lfs install` before cloning.

#### With Source
Clone the repo, install dependencies with `pip install -r models/sentiment/requirements.txt`, activate venv, then start FastAPI development server with `python3 -m models.sentiment.main`.

#### With Docker
Pull the latest build with `docker pull ghcr.io/ericcheung1/wpaas:main`, then start container with `docker run -p 8000:8000 ghcr.io/ericcheung1/wpaas:main`.

## Model

This API serves a fine-tuned DistilBERT model for sentiment classification. Model weights are included in the repository using Git LFS.

## Clients

This API is currently consumed by the following client service(s):

- Website: [word-processor-dot-com](https://github.com/ericcheung1/word-processor-dot-com)