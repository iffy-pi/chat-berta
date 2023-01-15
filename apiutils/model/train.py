from py import process
import torch
from transformers import PreTrainedTokenizer, RobertaTokenizerFast, RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments,  DataCollatorForSeq2Seq
from chat_bert_trainer import CustomTrainer
from datasets import load_dataset, load_metric
from data_preprocessing import process_dataset, data_split
from samsum import SamSumDataset
#metric = load_metric("rouge")
#train_args = TrainingArguments()
tokenizer:PreTrainedTokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
datasets = load_dataset("samsum")

def tokenization(example):
    return tokenizer(example["dialogue"])
train_dataset, eval_dataset = datasets["test"].map(process_dataset), datasets["validation"].map(process_dataset)


train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
eval_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
# print(train_dataset[0]['input_ids'])
# print(tokenizer.decode(train_dataset[0]['input_ids'], skip_special_tokens =True))
# print(tokenizer.decode(train_dataset[0]['labels'], skip_special_tokens = True))



trainer = CustomTrainer(model=model, train_dataset = train_dataset, eval_dataset = eval_dataset, tokenizer=tokenizer)

trainer.train()
print('done')