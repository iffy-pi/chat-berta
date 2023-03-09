import torch
from transformers import Trainer
import torch.nn as nn
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
        labels = inputs.get("labels")
        input_ids = inputs.get("input_ids")
        attention_mask = inputs.get("attention_mask")

        # print(attention_mask.shape)
        # print(input_ids.shape)
        # print(labels.shape)
        outputs = model(input_ids, attention_mask)
        logits = outputs.get('logits')
        loss_fct = nn.MSELoss()
        loss = loss_fct(logits.squeeze(), labels.squeeze())
        return (loss, outputs) if return_outputs else loss