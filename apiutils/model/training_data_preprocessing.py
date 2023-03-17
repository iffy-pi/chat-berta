import concurrent.futures
from functools import partial
from rouge import Rouge
from samsum import SamSumDataset
import torch
from constants import MAX_LENGTH

def rouge_score(generated_summary, reference_summary) -> float:
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    rouge_1_f = scores[0]['rouge-1']['f'] # change to rouge L later
    return rouge_1_f

def process_example(example, tokenizer, nlp):
    input_ids = []
    attention_mask = []
    labels = []

    dialogue = example['dialogue']
    turns = dialogue.split("\n")  # split the sentences
    abstractive_label = example['summary']
    for turn in turns:
        sentences = nlp(turn).sents
        for sent_obj in sentences:
            sentence = sent_obj.text
            if sentence == "":
                continue
            # rouge score comparing sentence and abstractive label
            label = rouge_score(sentence, abstractive_label)
            # tokenize the sentence
            encoded_sentence = tokenizer(sentence, max_length=MAX_LENGTH, padding="max_length", truncation=True, return_tensors='pt')

            # add to lists
            input_ids.append(encoded_sentence["input_ids"].squeeze(0))
            attention_mask.append(encoded_sentence["attention_mask"].squeeze(0))
            labels.append(label)

    return input_ids, attention_mask, labels


def preprocess_function(dataset, tokenizer, nlp):
    input_ids = []
    attention_mask = []
    labels = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        partial_process_example = partial(process_example, tokenizer=tokenizer, nlp=nlp)
        results = list(executor.map(partial_process_example, dataset))

    for result in results:
        input_ids.extend(result[0])
        attention_mask.extend(result[1])
        labels.extend(result[2])

    assert len(input_ids) == len(attention_mask) == len(labels)
    new_dataset = SamSumDataset(
        torch.stack(input_ids),
        torch.stack(attention_mask),
        torch.tensor(labels)
    )
    return new_dataset