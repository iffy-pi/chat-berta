from transformers import RobertaTokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

def process_dataset(dataset): #dialogue, id, summary
    model_inputs = tokenizer.encode_plus(dataset["dialogue"], max_length=512, pad_to_max_length=True, return_tensors='pt')
    #model_inputs = tokenizer(inputs, padding = True, truncation = True)

    # Setup the tokenizer for targets/labels
    labels = tokenizer.encode_plus(dataset["summary"], max_length=512, pad_to_max_length=True, return_tensors='pt')

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

