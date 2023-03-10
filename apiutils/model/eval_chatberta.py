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
    # REMOVE .select()
    eval_dataset = preprocess_dialogues(datasets["test"].select(range(100)))
    summary_options = {
        "basic_options": [],
        "summarize_only_for": -1 
    }
    
    message_ids, extractive_summaries = model.summarize(eval_dataset, summary_options)
    
        
    f,p,r = summarizer_evaluator(extractive_summaries, eval_dataset["summary"])
    print(f)
    print(p)
    print(r)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
    