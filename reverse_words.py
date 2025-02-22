def reverse_words(sentence):
    return ' '.join([''.join(reversed(i)) for i in str(sentence).split()])