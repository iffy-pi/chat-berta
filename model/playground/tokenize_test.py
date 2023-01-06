from transformers import RobertaTokenizer
from datasets import load_dataset
dataset = load_dataset("samsum", split="train")
# Load the tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize the input text
input_text = dataset[0]['dialogue']#.split("\r\n")
#input_text = [line + "\r\n" for line in input_text]
print(input_text)
tokens = tokenizer(input_text)
converted_tokens = tokenizer.convert_ids_to_tokens([0, 10127, 5219, 35, 38, 17241, 1437, 15269, 4, 1832, 47, 236, 103, 116, 2])

print(converted_tokens)