from common.schemas import payload, texts
import yake

text_idx, pred_result_idx = 0, 0
id_idx = 1

def process_inputs(in_payload: payload) -> list[dict]:
    """
    Takes payload object and returns a list of dicts with 
    the input texts and if applicable, the text ids
    """
    input_texts = []

    for item in in_payload.texts:

        if in_payload.contains_id == False:
            input_texts.append({"text": item.text.lower().strip(),
                          "text_id": None})
            
        elif in_payload.contains_id == True:
            input_texts.append({"text": item.text.lower().strip(),
                          "text_id": item.text_id})

    return input_texts


def extract_keywords(custom_yake, input_texts):
    """
    Takes a custom yake keyword extractor and input texts
    and performs keyword extraction on texts. Then formats
    the output.
    """
    output = {"keywords": []}

    for text in input_texts:
        
        keywords = custom_yake.extract_keywords(text["text"])
        
        formatted_kw = []
        for kw, score in keywords:
            formatted_kw.append({
                "keyword": kw,
                "score": float(score)
            })

        output["keywords"].append({
            "text_id": text["text_id"],
            "extracted_keywords": formatted_kw
        })

    return output

if __name__ == "__main__":
    from common.schemas import texts

    text1 = texts(text="I love to eat nachos")
    text2 = texts(text="I hate to eat nachos")
    text3 = texts(text="This is just for dev ;)")

    pl = payload(texts=[text1, text2, text3])

    custom_kw_extractor = yake.KeywordExtractor(
    lan="en",              # language
    n=3,                   # ngram size
    dedupLim=0.9,          # deduplication threshold
    dedupFunc='seqm',      # deduplication function
    windowsSize=1,         # context window
    top=10,                # number of keywords to extract
    features=None          # custom features
    )

    txs = process_inputs(pl)
    raw_kws = extract_keywords(custom_kw_extractor, txs)

    print(raw_kws)