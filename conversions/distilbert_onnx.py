from optimum.onnxruntime import ORTModelForSequenceClassification, ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig
from transformers import AutoTokenizer

model_id = "distilbert-base-uncased-finetuned-sst-2-english"
save_dir = "./dstb_onnx"

model = ORTModelForSequenceClassification.from_pretrained(model_id, export=True)

quantizer = ORTQuantizer.from_pretrained(model)

qconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=True)

tokenizer = AutoTokenizer.from_pretrained(model_id)

quantizer.quantize(save_dir=save_dir, quantization_config=qconfig)

# Save the exported model
# model.save_pretrained("./distilbert_onnx")
tokenizer.save_pretrained(save_dir)
