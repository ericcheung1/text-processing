import uvicorn
from fastapi import FastAPI, status
from common.schemas import payload
import yake

# ;))

app = FastAPI()

custom_kw_extractor = yake.KeywordExtractor(
    lan="en",              # language
    n=3,                   # ngram size
    dedupLim=0.9,          # deduplication threshold
    dedupFunc='seqm',      # deduplication function
    windowsSize=1,         # context window
    top=10,                # number of keywords to extract
    features=None          # custom features
)

@app.get("/health", status_code=status.HTTP_201_CREATED)
def ping():
    return {"message": "service ok"}

@app.post("/sentiment")
def process_sentiment(input_payload: payload):
    pass

if __name__ == "__main__":
    uvicorn.run("models.sentiment.main:app", reload=True)