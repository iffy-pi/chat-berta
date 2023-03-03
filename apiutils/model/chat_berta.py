from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments
from chat_bert_trainer import CustomTrainer
import torch
from constants import BATCH_SIZE, MAX_LENGTH
class ChatBerta:
    def __init__(self):
        ## only for initial, replace with actual directory path
        self.model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
        self.tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        #model = RobertaForSequenceClassification.from_pretrained("/path/to/directory")
    def generate_summary(self, sentences):
        logits = []
        encoded_sentences = self.tokenizer(sentences, max_length=MAX_LENGTH, padding="max_length", truncation=True, return_tensors='pt')
        output = self.model(**encoded_sentences)
        logits = output.logits

        def construct_extractive_summary(logits:torch.tensor, max_dialogue_len = 2) -> str:
            sentence_scores = logits.tolist()
            input_len = len(sentence_scores)
            summary_len = min(max_dialogue_len, input_len)
            selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
            selected_indexes.sort()
            selected_texts = [sentences[i] for i in selected_indexes]
            return "\n".join(selected_texts)
        return construct_extractive_summary(logits)


if __name__ == "__main__":
    example = ["John: I like apples, What is your favourite fruit?",
    "Jane: I like oranges better, apples be gross sometimes",
    "John: Oh really, I think apples are superior","Janet:Interesting"]
    chat_berta = ChatBerta()
    original = '\n'.join(s for s in example)
    print(f"Original: {original}")
    print(f"Summary: {chat_berta.generate_summary(example)}")
