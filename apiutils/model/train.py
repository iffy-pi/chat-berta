import torch
from torch.utils.data import TensorDataset, DataLoader
from transformers import PreTrainedTokenizer, RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments,  DataCollatorForSeq2Seq
from chat_bert_trainer import CustomTrainer
from datasets import load_dataset, load_metric
from data_preprocessing import process_dataset
from samsum import SamSumDataset
import logging
tokenizer:PreTrainedTokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
datasets = load_dataset("samsum")

def preprocess_function(dataset, tokenizer, max_length=512):
    encodings = {"input_ids": torch.empty((0, max_length)), "attention_mask": torch.empty((0, max_length))}
    labels = torch.empty((0, max_length))
    for example in dataset:
        # Tokenize the input text
        encoded_input = tokenizer.encode_plus(example["dialogue"], max_length=max_length, pad_to_max_length=True, return_tensors='pt')
        # Concatenate the summaries and tokenize the label
        label = example["summary"]
        encoded_label = tokenizer.encode_plus(label, max_length=max_length, pad_to_max_length=True, return_tensors='pt')

        encodings["input_ids"] = torch.cat((encodings["input_ids"], encoded_input["input_ids"]), dim=0)
        encodings["attention_mask"] = torch.cat((encodings["attention_mask"], encoded_input["attention_mask"]), dim=0)
        labels = torch.cat((labels, encoded_label["input_ids"]), dim=0)
    
    # for example in dataset:
    #     sentences = example['dialogue'].split("\r\n")
    #     encoded_input = tokenizer.encode_plus(sentences, max_length=max_length, pad_to_max_length=True, return_tensors='pt')

    #     # Concatenate the summaries and tokenize the label
    #     label = example["summary"]
    #     encoded_label = tokenizer.encode_plus(label, max_length=max_length, pad_to_max_length=True, return_tensors='pt')

    #     encodings["input_ids"] = torch.cat((encodings["input_ids"], encoded_input["input_ids"]), dim=0)
    #     encodings["attention_mask"] = torch.cat((encodings["attention_mask"], encoded_input["attention_mask"]), dim=0)
    #     labels = torch.cat((labels, encoded_label["input_ids"]), dim=0)

    return SamSumDataset(encodings, labels)

train_dataset = preprocess_function(datasets["test"], tokenizer)
eval_dataset = preprocess_function(datasets["validation"], tokenizer)


#data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

trainer = CustomTrainer(model=model, 
                        train_dataset=train_dataset, 
                        eval_dataset=eval_dataset, 
                        )


trainer.train()
print('done')