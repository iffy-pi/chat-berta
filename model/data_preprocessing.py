from transformers import RobertaTokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

def process_dataset(dataset): #dialogue, id, summary
    inputs = [doc for doc in dataset["dialogue"]]
    model_inputs = tokenizer(inputs, padding = True, truncation = True)

    # Setup the tokenizer for targets/labels
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(dataset["summary"],  padding = True, truncation = True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def data_split(dataset):
    texts = dataset["dialogue"]
    labels = dataset["summary"]

    return texts, labels