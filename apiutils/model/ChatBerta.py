import sys
import os
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments
from apiutils.model.chat_bert_trainer import CustomTrainer
import spacy
from apiutils.model.constants import MAX_LENGTH, DEVICE, BATCH_SIZE
PATH = 'roberta-base'

class ChatBerta:
    def __init__(self):
        ## only for initial, replace with actual directory path
        self.model = RobertaForSequenceClassification.from_pretrained(PATH, num_labels=1).to(DEVICE)
        self.tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        self.nlp = spacy.load("en_core_web_trf")

    def _select_sentences_for_input(self, messages, summary_options):
        # this function takes the message dict and sententizes using spacy, then assigns each sentence its pid
        # returns list of message 'id' to use in input
        sentences = {
            "id": [],
            "text": []
        }
        monologue_pid = summary_options["summarize_only_for"] if summary_options["summarize_only_for"] != -1 else None
        for message in messages:
            if monologue_pid is not None and monologue_pid != message["pid"]: # filter for specific PID if exist
                continue
            #split into sentences
            segmented_text = [obj.text for obj in self.nlp(message["text"]).sents]
            ids = [message["id"] for i in range(len(segmented_text))] # duplicate label across all 
            sentences["text"].extend(segmented_text)
            sentences["id"].extend(ids)

        return sentences
            

    def _choose_messages(self, sentences, min_dialogue_len = 4):
        chosen_message_ids = []
        chosen_message_text = []
        sentence_scores = []
        for input_text in sentences["text"]:
            encoded_sentence = self.tokenizer(input_text, max_length=MAX_LENGTH, padding="max_length", truncation=True, return_tensors='pt')
            output = self.model(**encoded_sentence.to(DEVICE))
            score = output.logits.tolist()
            sentence_scores.append(score)
        input_len = len(sentence_scores)

       # summary_len = min(min_dialogue_len, input_len)
        summary_len = input_len//2 + 1

        #sort the list by highest score, slice top k. the list values are the relative message ordering
        selected_indexes = list(sorted(range(input_len), key=lambda x: sentence_scores[x], reverse=True))[:summary_len]
        #sort list back into message order
        selected_indexes.sort()

        for index in selected_indexes:
            # the message id of the index is located at the index of the message_ids
            print(f"Selected: sentence = {sentences['text'][index]} id = {sentences['id'][index]}")
            chosen_message_ids.append(sentences['id'][index])
            chosen_message_text.append(sentences['text'][index])
        return chosen_message_ids,chosen_message_text


    def summarize(self, messages, summary_options):
        """
        The summarize function to be called by network component.
        params:
        messages: a list of message objects(pid, id, text)
        summary_options: current one we have is "summarize_only_for"
        """
        print("Summarizing")
        sentences = self._select_sentences_for_input(messages, summary_options)
        
        chosen_message_ids, chosen_message_texts = self._choose_messages(sentences)

        summary = ''.join(chosen_message_texts)

        return chosen_message_ids, summary