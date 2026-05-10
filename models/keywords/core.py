from common.schemas import payload

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

