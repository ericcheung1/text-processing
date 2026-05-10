import uvicorn
from fastapi import FastAPI, status
from common.schemas import payload
from models.keywords.core import process_inputs, extract_keywords
import yake

app = FastAPI(docs_url=None, redoc_url=None)

kw_extractor = yake.KeywordExtractor(
    lan="en",              # language
    n=3,                   # ngram size
    dedupLim=0.9,          # deduplication threshold
    dedupFunc='seqm',      # deduplication function
    windowsSize=1,         # context window
    top=10,                # number of keywords to extract
    features=None,         # custom features
)

@app.get("/health", status_code=status.HTTP_201_CREATED)
def ping():
    return {"message": "service ok"}

@app.post("/keywords")
def keywords(input_payload: payload):  

    processed_inputs = process_inputs(input_payload)
    kws = extract_keywords(kw_extractor, processed_inputs)
    
    return kws

if __name__ == "__main__":
    uvicorn.run("models.keywords.main:app", reload=True)