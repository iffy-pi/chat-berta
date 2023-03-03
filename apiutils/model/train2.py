import torch
from sklearn.metrics import mean_squared_error
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments, DataCollatorWithPadding
from chat_bert_trainer import CustomTrainer
from transformers.integrations import TensorBoardCallback
from datasets import load_dataset
from samsum import SamSumDataset
from rouge import Rouge
from constants import MAX_LENGTH, BATCH_SIZE
import torch.nn as nn
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
datasets = load_dataset("samsum")

def rouge_score(generated_summary, reference_summary) -> float:
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    rouge_1_f = scores[0]['rouge-1']['f'] # change to rouge L later
    return rouge_1_f

class CustomDataCollator(DataCollatorWithPadding):
    def __init__(self, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __call__(self, examples):
        input_ids = []
        attention_mask = []
        labels = []
        for example in examples:
            sentence = example['sentence']
            label = example['label']
            encoded_sentence = self.tokenizer(sentence, max_length=self.max_length, padding="max_length", truncation=True, return_tensors='pt')
            input_ids.append(encoded_sentence["input_ids"].squeeze(0))
            attention_mask.append(encoded_sentence["attention_mask"].squeeze(0))
            labels.append(label)

        input_ids = torch.stack(input_ids)
        attention_mask = torch.stack(attention_mask)
        labels = torch.tensor(labels)

        return {'input_ids': input_ids, 'attention_mask': attention_mask, 'labels': labels}

data_collator = CustomDataCollator(tokenizer, max_length=512)

train_dataloader = DataLoader(
    train_dataset, 
    batch_size=batch_size, 
    shuffle=True, 
    collate_fn=data_collator,
    pin_memory=True
)

    return new_dataset


#check torch is using GPU
print(f"Is CUDA supported by this system? \n\
      {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
cuda_id = torch.cuda.current_device()
print(f"Name of current CUDA device:\n\
      {torch.cuda.get_device_name(cuda_id)}")


# only use 32 training examples for notebook - DELETE LINE FOR FULL TRAINING
train_dataset = datasets["train"]#.select(range(32))
# only use 32 training examples for notebook - DELETE LINE FOR FULL TRAINING
eval_dataset = datasets["validation"]#.select(range(32))
train_dataset = preprocess_function(train_dataset)
eval_dataset = preprocess_function(eval_dataset)


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.squeeze()

    mse = mean_squared_error(labels, preds)

    return {"mse": mse}

args = TrainingArguments(output_dir=r"C:\Users\rao_h\Documents\GitHub\Chat-Berta\apiutils\model\temp",\
    per_device_train_batch_size=BATCH_SIZE,
     per_device_eval_batch_size= BATCH_SIZE,
     evaluation_strategy="steps")

# dataloaders for pin memory error
train_loader = torch.utils.data.DataLoader(train_dataset, 
                                           batch_size=BATCH_SIZE, 
                                           shuffle=True, 
                                           num_workers=2, 
                                           pin_memory=True)
eval_loader = torch.utils.data.DataLoader(eval_dataset, 
                                          batch_size=BATCH_SIZE, 
                                          shuffle=False, 
                                          num_workers=2, 
                                          pin_memory=True)

trainer = CustomTrainer(model=model, 
                        train_dataset=train_dataset, 
                        eval_dataset=eval_dataset, 
                        train_loader = train_loader,
                        eval_loader = eval_loader,
                        args=args,
                        compute_metrics = compute_metrics,
                        callbacks=[TensorBoardCallback()],
                        )




trainer.train()
print('done')