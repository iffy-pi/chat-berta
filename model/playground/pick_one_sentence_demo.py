import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, PreTrainedTokenizer
from datasets import load_dataset
tokenizer:PreTrainedTokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
dataset = load_dataset("samsum", split="train")

input_text = dataset[0]['dialogue'].split("\r\n")
inputs = tokenizer(input_text, return_tensors="pt", padding=True)

#inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits

def construct_extractive_summary(logits:torch.tensor, inputs, max_dialogue_len = 2) -> str:
    sentence_scores = logits.tolist()
    print(inputs["input_ids"])
    input_texts = tokenizer.batch_decode(inputs["input_ids"], skip_special_tokens =False)
    input_len = len(sentence_scores)
    summary_len = min(max_dialogue_len, input_len)
    selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
    selected_indexes.sort()
    selected_texts = [input_texts[i] for i in selected_indexes]
    return "\n".join(selected_texts)

print(construct_extractive_summary(logits, inputs))
print('done')