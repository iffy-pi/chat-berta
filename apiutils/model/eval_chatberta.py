import sys
from evaluate import summarizer_evaluator
from preprocess import preprocess_dialogues
from datasets import load_dataset
from transformers import RobertaTokenizer
from ChatBerta import ChatBerta
from constants import DEVICE

def main():
    model = ChatBerta()
    datasets = load_dataset("samsum")
    test_dataset = datasets["test"]
    eval_dialogues = preprocess_dialogues(test_dataset)
    dataset_len = len(test_dataset)
    summary_options = {
        "basic_options": [],
        "summarize_only_for": -1 
    }
    message_ids = []
    extractive_summaries = []
    
    for i in range(dataset_len):
        message_id, extractive_summary = model.summarize(eval_dialogues[i], summary_options)
        message_ids.append(message_id)
        extractive_summaries.append(extractive_summary)
        
    avg_f = 0
    avg_p = 0
    avg_r = 0
    for extractive_summary, abstract_summary in zip(extractive_summaries, test_dataset["summary"]):
        f,p,r = summarizer_evaluator(extractive_summary, abstract_summary)
        avg_f += f
        avg_p += p
        avg_r += r
    avg_f /= dataset_len
    avg_p /= dataset_len
    avg_r /= dataset_len
    print("Avg f: %.3f Avg p: %.3f Avg r: %.3f" % (avg_f, avg_p, avg_r))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
    