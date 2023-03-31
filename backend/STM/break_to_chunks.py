import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize
from STM import break_file

def break_up_file_to_chunks(transcript, chunk_size=2000, overlap_size=100):
    tokens = word_tokenize(transcript)
    return list(break_file.break_up_file(tokens, chunk_size, overlap_size))