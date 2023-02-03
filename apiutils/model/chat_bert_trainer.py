import torch
from transformers import Trainer
from evaluate import rouge_score
from transformers import RobertaTokenizer, RobertaForSequenceClassification, PreTrainedTokenizer
tokenizer:PreTrainedTokenizer = RobertaTokenizer.from_pretrained("roberta-base")

def construct_extractive_summary(logits:torch.tensor, inputs, max_dialogue_len = 4) -> str:
    sentence_scores = logits.tolist()
    input_texts = tokenizer.decode(inputs, skip_special_tokens =True)
    input_len = len(sentence_scores)
    summary_len = min(max_dialogue_len, input_len)
    selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
    selected_indexes.sort()
    selected_texts = [input_texts[i] for i in selected_indexes]
    return "\n".join(selected_texts)


class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        #labels = inputs.pop("labels")
        input_ids = torch.tensor(inputs["input_ids"]).long()
        #print(input_ids.shape)
        attention_mask = torch.tensor(inputs["attention_mask"]).long()
        #print(attention_mask.shape)
        labels = torch.tensor(inputs["labels"]).long()
        #print(model(input_ids=input_ids, attention_mask=attention_mask))
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.get("logits") 

        loss = 0
        for i in range(input_ids.shape[0]):
            reference_summary = tokenizer.decode(labels[i], skip_special_tokens = True)
            extractive_summary = construct_extractive_summary(logits[i], inputs["input_ids"][i])
            loss += -rouge_score(extractive_summary, reference_summary)

        loss /= input_ids.shape[0]
        return (loss, outputs) if return_outputs else torch.tensor(loss, requires_grad = True)