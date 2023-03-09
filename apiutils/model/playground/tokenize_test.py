from transformers import RobertaTokenizer

# Instantiate the tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize the input text
text = "This is a sample paragraph of text that we want to tokenize for fine-tuning a RoBERTa model."
tokenized_text = tokenizer.tokenize(text)
print(tokenized_text)

# Convert the tokens to their corresponding IDs
input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
print(input_ids)

