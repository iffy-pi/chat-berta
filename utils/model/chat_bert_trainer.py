import torch
from transformers import Trainer
from evaluate import rouge_score
from transformers import RobertaTokenizer, RobertaForSequenceClassification, PreTrainedTokenizer
tokenizer:PreTrainedTokenizer = RobertaTokenizer.from_pretrained("roberta-base")


def construct_extractive_summary(logits:torch.tensor, inputs, max_dialogue_len = 4) -> str:
    sentence_scores = logits.tolist()
    input_texts = tokenizer.batch_decode(inputs["input_ids"], skip_special_tokens =True)
    input_len = len(sentence_scores)
    summary_len = min(max_dialogue_len, input_len)
    selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
    selected_indexes.sort()
    selected_texts = [input_texts[i] for i in selected_indexes]
    return "\n".join(selected_texts)
    


class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        reference_summary = tokenizer.batch_decode(labels, skip_special_tokens =True)
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get("logits") 
        # build extractive summary
        extractive_summary = construct_extractive_summary(logits, inputs)
        #compute loss using neg rouge score
        loss = -rouge_score(extractive_summary, reference_summary)
        return (loss, outputs) if return_outputs else loss