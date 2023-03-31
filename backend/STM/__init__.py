from STM import break_file
from STM import break_to_chunks
from STM import prompt_to_text

class STM:
    
    def __init__(self):
        pass

    def break_up_file(self,tokens, chunk_size, overlap_size):
        return break_file.break_up_file(tokens, chunk_size, overlap_size)
    
    def break_up_file_to_chunks(self,transcript):
        return break_to_chunks.break_up_file_to_chunks(transcript, chunk_size=2000, overlap_size=100)
    
    def convert_to_prompt_text(self,tokenized_text):
        return prompt_to_text.convert_to_prompt_text(tokenized_text)