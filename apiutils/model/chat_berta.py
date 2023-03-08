from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments
from chat_bert_trainer import CustomTrainer
import torch
from constants import BATCH_SIZE, MAX_LENGTH
PATH = r"C:\Users\rao_h\Documents\GitHub\Chat-Berta\apiutils\model\temp\checkpoint-61000"
class ChatBerta:
    def __init__(self):
        ## only for initial, replace with actual directory path
        self.model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=1)
        self.tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

    def _select_messages_for_input(self, messages, summary_options):# returns list of message 'id' to use in input
        # returns list of message 'id' to use in input
        message_ids = []
        message_texts = []
        monologue_pid = summary_options["summarize_only_for"] if summary_options["summarize_only_for"] != -1 else None
        for message in messages:
            if monologue_pid is not None and monologue_pid != message["pid"]:
                continue
            message_ids.append(message["id"])
            message_texts.append(message["text"])

        return message_ids, message_texts
            

    def _choose_messages(self, encoded_sentences, message_ids, min_dialogue_len = 4):
        chosen_message_ids = []
        output = self.model(**encoded_sentences)
        logits = output.logits
        sentence_scores = logits.tolist()
        input_len = len(sentence_scores)
       # summary_len = min(min_dialogue_len, input_len)
        summary_len = input_len//2 + 1

        #sort the list by highest score, slice top k. the list values are the relative message ordering
        selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
        #sort list back into message order
        selected_indexes.sort()

        for index in selected_indexes:
            # the message id of the index is located at the index of the message_ids
            chosen_message_ids.append(message_ids[index])
        return chosen_message_ids

    def _reconstruct(self, chosen_message_ids, messages):
        ids = set(chosen_message_ids)
        texts = []
        for message in messages:
            if message["id"] in ids:
                texts.append(message["text"])
        return "\n".join(texts)

    def summarize(self, messages, summary_options):
        """
        The summarize function to be called by network component.
        params:
        messages: a list of message objects(pid, id, text)
        summary_options: current one we have is "summarize_only_for"
        """
        message_ids, message_texts = self._select_messages_for_input(messages, summary_options)
        document = "".join(message_texts)
        #create inputs, which are a dialogue-turn + full conversation appended
        input_texts = [message + '[SEP]' + document for  message in message_texts] # remove this document thing next training
        encoded_sentences = self.tokenizer(input_texts, max_length=MAX_LENGTH, padding="max_length", truncation=True, return_tensors='pt')

        chosen_message_ids = self._choose_messages(encoded_sentences, message_ids)

        summary  = self._reconstruct(chosen_message_ids, messages)

        return chosen_message_ids, summary


if __name__ == "__main__":
    messages = {
"messages": [
{
"id": 0,
"pid": 0,
"text": "Apples are my favourite fruit, what are yours?"
},
{
"id": 1,
"pid": 1,
"text": "I like oranges better, apples be gross sometimes"
},
{
"id": 2,
"pid": 0,
"text": "Oh really? I think apples are superior."
},
{
"id": 3,
"pid": 1,
"text": "Interesting."
},
{
"id": 4,
"pid": 0,
"text": "Why do you think oranges are better than apples?"
},
{
"id": 5,
"pid": 1,
"text": "I think oranges are sweeter and juicier than apples."
},
{
"id": 6,
"pid": 0,
"text": "But apples have a wider variety of flavors and textures."
},
{
"id": 7,
"pid": 1,
"text": "I guess that's true, but I just prefer oranges."
},
{
"id": 8,
"pid": 0,
"text": "Have you ever tried a Honeycrisp apple? They're amazing."
},
{
"id": 9,
"pid": 1,
"text": "No, I haven't. I'll have to try one sometime."
},
{
"id": 10,
"pid": 0,
"text": "Definitely do. They're the perfect combination of sweet and tart."
},
{
"id": 11,
"pid": 1,
"text": "I'll keep that in mind. Thanks for the recommendation."
}
]
}
    messages = messages["messages"]
    summary_options = {
 "basic_options": [],
 "summarize_only_for": -1 
 }
    chat_berta = ChatBerta()
    chosen_message_ids, summary = chat_berta.summarize(messages=messages, summary_options = summary_options)

    print(summary)
    print(chosen_message_ids)