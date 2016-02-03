from nltk.corpus import stopwords

ADDITIONAL_STOPWORDS = {'http', 'www', 'com'}
CONJUNCTIONS = set(["she'll", "shouldn't've", "she'll've", "don't", "should've", "won't", "who'll've", "he's", "when's", "we've", "he'd", "ma'am", "y'all're", "he'd've", "how'd'y", "shan't've", "haven't", "who's", "they'd", "oughtn't", "I'd", "you've", "I'm", "she'd've", "we'll", "mayn't", "they've", "wasn't", "could've", "what've", "mustn't", "isn't", "it'll", "y'all", "why's", "you'd", "hasn't", "they'll've", "we'd", "he'll've", "shan't", "y'all'd've", "there'd", "needn't", "o'clock", "hadn't've", "wouldn't've", "there's", "shouldn't", "they'll", "needn't've", "mightn't", "doesn't", "so've", "what'll", "when've", "hadn't", "aren't", "let's", "I'll've", "wouldn't", "mightn't've", "weren't", "would've", "that'd've", "we'd've", "can't", "couldn't", "how'll", "you're", "y'all'd", "how's", "I've", "it's", "how'd", "we're", "I'd've", "it'd", "what're", "oughtn't've", "what's", "ain't", "who'll", "must've", "I'll", "they're", "you'd've", "mustn't've", "it'll've", "couldn't've", "won't've", "so's", "you'll've", "there'd've", "y'all've", "didn't", "where've", "they'd've", "why've", "it'd've", "who've", "sha'n't", "to've", "where'd", "where's", "what'll've", "'cause", "might've", "he'll", "that'd", "we'll've", "she'd", "can't've", "you'll", "will've", "she's", "that's"])


FILTER_SET = set(stowords.words("english"))
FILTER_SET.union(ADDITIONAL_STOPWORDS)
FILTER_SET.union(CONJUNCTIONS)
