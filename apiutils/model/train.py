import torch
from sklearn.metrics import mean_squared_error
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments
from chat_bert_trainer import CustomTrainer
from transformers.integrations import TensorBoardCallback
from datasets import load_dataset
from constants import GRAD_ACCUMULATION, BATCH_SIZE, DEVICE
import spacy
import time
from training_data_preprocessing import preprocess_function

tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
model.to(DEVICE)
nlp = spacy.load("en_core_web_sm", exclude=["parser"])
nlp.enable_pipe("senter")
datasets = load_dataset("samsum")



# def preprocess_function(dataset):
#     input_ids = []
#     attention_mask = []
#     labels = []
#     for index, example in enumerate(dataset):
#         if index % 100 ==0:
#             print(f"Finished example {index+1} of {len(dataset)}")
#         dialogue = example['dialogue']
#         turns = dialogue.split("\n") # split the sentences
#         abstractive_label =  example['summary']
#         for turn in turns:
#             sentences = nlp(turn).sents
#             for sent_obj in sentences:
#                 sentence = sent_obj.text
#                 if sentence == "":
#                     continue
#                 # rouge score comparing sentence and abstractive label
#                 label = rouge_score(sentence, abstractive_label)
#                 # tokenize the sentence
#                 encoded_sentence = tokenizer(sentence, max_length=MAX_LENGTH, padding="max_length", truncation=True, return_tensors='pt')

#                 #add to lists
#                 input_ids.append(encoded_sentence["input_ids"].squeeze(0))
#                 attention_mask.append(encoded_sentence["attention_mask"].squeeze(0))
#                 labels.append(label)

#     assert len(input_ids) == len(attention_mask) == len(labels)
#     new_dataset = SamSumDataset(
#     torch.stack(input_ids),
#     torch.stack(attention_mask),
#     torch.tensor(labels)
#     )
#     return new_dataset


#check torch is using GPU
print(torch.backends.cudnn.enabled)
print("torch device:")
print(torch.cuda.current_device())
print("model device")
print(model.device)
print(f"number of devics: {torch.cuda.device_count()}")
print(f"Is CUDA supported by this  system? \n\
      {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
cuda_id = torch.cuda.current_device()
print(cuda_id)
print(f"Name of current CUDA device:\n\
      {torch.cuda.get_device_name(cuda_id)}")

print(f"fast tokenizer: {tokenizer.is_fast}")


# only use 32 training examples for notebook - DELETE LINE FOR FULL TRAINING
train_dataset = datasets["train"].select(range(32))
# only use 32 training examples for notebook - DELETE LINE FOR FULL TRAINING
eval_dataset = datasets["validation"].select(range(32))

start1 = time.time()
train_dataset = preprocess_function(train_dataset, tokenizer, nlp)
eval_dataset = preprocess_function(eval_dataset, tokenizer, nlp)
end1 = time.time()
print(f'preprocessing took: {end1-start1} seconds')

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.squeeze()

    mse = mean_squared_error(labels, preds)

    return {"mse": mse}

args = TrainingArguments(output_dir=r"C:\Users\rao_h\Documents\GitHub\Chat-Berta\apiutils\model\temp",\
    per_device_train_batch_size=BATCH_SIZE,
     per_device_eval_batch_size= BATCH_SIZE,
     gradient_accumulation_steps= GRAD_ACCUMULATION,
     fp16=True,
     evaluation_strategy="steps",
     eval_steps= 1000,
     save_steps = 10000)


trainer = CustomTrainer(model=model, 
                        train_dataset=train_dataset, 
                        eval_dataset=eval_dataset, 
                        args=args,
                        compute_metrics = compute_metrics,
                        callbacks=[TensorBoardCallback()],
                        )




trainer.train()
print('done')