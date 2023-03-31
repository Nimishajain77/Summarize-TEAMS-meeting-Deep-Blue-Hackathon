def convert_to_prompt_text(tokenized_text):
        prompt_text = " ".join(tokenized_text)
        prompt_text = prompt_text.replace(" 's", "'s")
        return prompt_text