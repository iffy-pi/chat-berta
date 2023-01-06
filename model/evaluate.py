from rouge import Rouge
def rouge_score(generated_summary, reference_summary) -> float:
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    rouge_1_f = scores[0]['rouge-1']['f']
    return rouge_1_f