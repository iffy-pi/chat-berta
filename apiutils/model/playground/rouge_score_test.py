from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
scores = scorer.score('The quick brown fox jumps over the lazy dog',
                      'The quick brown dog jumps on the log.')
scores = scorer.score('The quick brown fox jumps over the lazy dog',
                      'The quick brown fox jumps over the lazy dog')

print(scores)