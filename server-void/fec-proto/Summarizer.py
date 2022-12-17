import random


# prototype summarizer neural network model
# just pulls random words from the given sample
# degree is float (percentage) 0-1 (e.g. 0.9, 0.8, 0.2 etc)'
# the higher the degree, the stronger the 'summarization'
class SummarizerNN:
    def __init__(self):
        pass

    # sample summarizer, implemented by random word selector from each sentence
    # degree is float (percentage) 0-1 (e.g. 0.9, 0.8, 0.2 etc)'
    # the higher the degree, the stronger the summarization
    def summarize(self, text_sample, degree):
        text_word_count = len(text_sample.split())

        sentences = text_sample.split('.') # split by different sentences
        summary = []

        # the higher the degree, the rougher the summarization
        # use degree as a measure of how many words should be in 'summary'
        for sent in sentences:
            # how many words are in the current line
            words = sent.split()
            sent_word_count = len(words)
            num_words_pulled = int ( (1-degree)*sent_word_count)

            random_word_indcs = random.sample(range(0, sent_word_count), num_words_pulled)
            summary = summary + [ words[i] for i in random_word_indcs ] + [ '.' ]

        return " ".join(summary)