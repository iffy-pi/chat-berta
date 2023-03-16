from rouge import Rouge

def summarizer_evaluator(chosen_summary, abstract_summary):
    rouge = Rouge()
    # Get the average of the rouge scores of the generated summary
    scores = rouge.get_scores(chosen_summary, abstract_summary, avg=True)
    # Use rouge1 for now, as it is easier.
    f1_score = scores["rouge-1"]["f"]
    precision_score = scores["rouge-1"]["p"]
    recall_score = scores["rouge-1"]["r"]

    return f1_score, precision_score, recall_score 
    
    
