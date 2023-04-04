import os
from nltk.tokenize import word_tokenize
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import nltk
from dotenv import load_dotenv
import dateparser
from os.path import splitext, exists
import re
from collections import Counter
# import txt 
# import vtt
# from STM import STM
nltk.download("punkt")

load_dotenv()


app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_transcript(transcript):
    action_response = []

    def break_up_file(tokens, chunk_size, overlap_size):
        if len(tokens) <= chunk_size:
            yield tokens
        else:
            chunk = tokens[:chunk_size]
            yield chunk
            yield from break_up_file(
                tokens[chunk_size - overlap_size:], chunk_size, overlap_size
            )

    def break_up_file_to_chunks(transcript, chunk_size=2000, overlap_size=100):
        tokens = word_tokenize(transcript)
        return list(break_up_file(tokens, chunk_size, overlap_size))

    def convert_to_prompt_text(tokenized_text):
        prompt_text = " ".join(tokenized_text)
        prompt_text = prompt_text.replace(" 's", "'s")
        return prompt_text

    prompt_response = []

    chunks = break_up_file_to_chunks(transcript)
    for i, chunk in enumerate(chunks):
        prompt_request = "Summarize this meeting transcript: " + convert_to_prompt_text(
            chunks[i]
        )
        max_tokens = len(convert_to_prompt_text(chunks[i]).split()) // 2
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=0.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        prompt_response.append(response["choices"][0]["text"].strip())

        prompt_request = "Consoloidate these meeting summaries: " + \
            str(prompt_response)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=0.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        meeting_summary = response["choices"][0]["text"].strip()

        model_engine = "text-davinci-003" # Change this to the model you want to use
        temperature = 0.3 # Increase or decrease this to control the creativity of the generated title
        max_tokens = 10 # Increase or decrease this to control the length of the generated title
        
        title = openai.Completion.create(
            engine=model_engine,
            prompt=meeting_summary,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        ).choices[0].text.strip()

        # confidence = title.metadata.confidence

        # get action items from meting transcript
        action_response = []

        chunks = break_up_file_to_chunks(transcript)
        for i, chunk in enumerate(chunks):

            prompt_request = "Provide a list of action items with a due date from the provided meeting transcript text: " + \
                convert_to_prompt_text(chunks[i])
            messages = [
                {"role": "system", "content": "This is text summarization."}]
            messages.append({"role": "user", "content": prompt_request})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=.5,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            action_response.append(
                response["choices"][0]["message"]['content'].strip())

            prompt_request = "Consoloidate these meeting action items: " + \
                str(action_response)
            messages = [
                {"role": "system", "content": "This is text summarization."}]
            messages.append({"role": "user", "content": prompt_request})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=.5,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            meeting_action_items = response["choices"][0]["message"]['content'].strip(
            )
            # string = "meeting_action_items = response[\"choices\"][0][\"message\"]['content'].strip()"
            points = meeting_action_items.split(".")
            print(points)
            action_response = []

        chunks = break_up_file_to_chunks(transcript)
        for i, chunk in enumerate(chunks):

            prompt_request = "Provide a list of action items with a due date from the provided meeting transcript text: " + \
                convert_to_prompt_text(chunks[i])
            messages = [
                {"role": "system", "content": "This is text summarization."}]
            messages.append({"role": "user", "content": prompt_request})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=.5,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

        return jsonify(title=title, summary=meeting_summary, actionItems=points)



def clean_webvtt(filepath):
        """Clean up the content of a subtitle file (vtt) to a string

        Args:
            filepath (str): path to vtt file

        Returns:
            str: clean content
        """
        # read file content
        with open(filepath, "r", encoding="utf-8") as fp:
            content = fp.read()

        # remove header & empty lines
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        lines = lines[1:] if lines[0].upper() == "WEBVTT" else lines

        # remove indexes
        lines = [lines[i] for i in range(len(lines)) if not lines[i].isdigit()]

        # remove tcode
        #pattern = re.compile(r'^[0-9:.]{12} --> [0-9:.]{12}')
        pattern = r'[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}\/\d+-\d'
        lines = [lines[i] for i in range(len(lines))
                if not re.match(pattern, lines[i])]

        # remove timestamps
        pattern = r"^\d{2}:\d{2}:\d{2}.\d{3}.*\d{2}:\d{2}:\d{2}.\d{3}$"
        lines = [lines[i] for i in range(len(lines))
                if not re.match(pattern, lines[i])]

        content = " ".join(lines)

        # remove duplicate spaces
        pattern = r"\s+"
        content = re.sub(pattern, r" ", content)

        # add space after punctuation marks if it doesn't exist
        pattern = r"([\.!?])(\w)"
        content = re.sub(pattern, r"\1 \2", content)

        return content


# def vtt_to_clean_file(file_in: str, file_out=None, **kwargs) -> str:
def vtt_to_clean_file(file_in, file_out=None, **kwargs):

        """Save clean content of a subtitle file to text file

        Args:
            file_in (str): path to vtt file
            file_out (None, optional): path to text file
            **kwargs (optional): arguments for other parameters
                - no_message (bool): do not show message of result.
                                    Default is False

        Returns:
            str: path to text file
        """
        # set default values
        no_message = kwargs.get("no_message", False)
        if not file_out:
            filename = splitext(file_in)[0]
            file_out = "%s.txt" % filename
            i = 0
            while exists(file_out):
                i += 1
                file_out = "%s_%s.txt" % (filename, i)

        content = clean_webvtt(file_in)
        with open(file_out, "w+", encoding="utf-8") as fp:
            fp.write(content)
        if not no_message:
            print("clean content is written to file: %s" % file_out)

        return file_out



# vtt_to_clean_file(filepath)
def count_tokens(filename):
        with open(filename, 'r') as f:
            text = f.read()
        tokens = word_tokenize(text)
        return len(tokens)

@app.route("/summarize_txt", methods=["POST"])
def summarize():
    transcript_file = request.files["file"]
    transcript_text = transcript_file.read().decode("utf-8")
    result = summarize_transcript(transcript_text)
    return result

# @app.route("/summarize_vtt", methods=["POST"])
# def summarize_txt():
#     transcript_file = request.files["file"]
#     vtt_to_clean_file(transcript_file)
#     transcript_text = transcript_file.read().decode("utf-8")
#     result = summarize_transcript(transcript_text)
#     return result

from werkzeug.utils import secure_filename
app.config['UPLOAD_FOLDER'] = "C:/Users/dll/Downloads/stm"

@app.route("/summarize_vtt", methods=["POST"])
def summarize_txt():
    transcript_file = request.files['file']
    filename = secure_filename(transcript_file.filename)
    transcript_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    transcript_file=vtt_to_clean_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # transcript_file = request.files["file"]
    # vtt_to_clean_file(transcript_file)
    # transcript_text = transcript_file.read().decode("utf-8")
    with open(transcript_file, "r", encoding="utf-8") as f:
       transcript_text = f.read()
       result = summarize_transcript(transcript_text)
       return result