from rouge import Rouge
def rouge_score(generated_summary, reference_summaries):
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summaries)
    rouge_1_f = scores[0]['rouge-1']['f']
    return rouge_1_f

### test 
extractive = "john: I'm heading to the market. \n DO you need anything? Alice: Get me some milk \n"
reference = "Milk is something that alice and john both love. \nMarket value of milk is rising.\n"

print(rouge_score(extractive, reference))