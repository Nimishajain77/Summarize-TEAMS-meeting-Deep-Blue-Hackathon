from werkzeug.utils import secure_filename
import os
from nltk.tokenize import word_tokenize
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import nltk
from dotenv import load_dotenv
import dateparser
from os.path import splitext, exists
from azure.translate import traslate_language_english
import re
from collections import Counter
nltk.download("punkt")

load_dotenv()


app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_transcript(transcript):

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

    def split_text(text):
        words = text.split()
        word_limit = 1300
        num_parts = len(words) // word_limit + 1
        parts = []
        for i in range(num_parts):
            start_index = i * word_limit
            end_index = (i + 1) * word_limit
            parts.append(' '.join(words[start_index:end_index]))
        return parts

    chunks = split_text(transcript)
    summary_list = []
    for i, chunk in enumerate(chunks):
        prompt = [
            {"role": "system", "content": "Act as a meeting note taker, and summarize this meeting transcript. Highlight to-do lists and important keypoints from each speaker as highly precisely as possible. Make sure not to give any numbering to anything but add a new line after every keypoint. Additionally, add curly brackets around each speaker name."},
            {"role": "user", "content": chunk},
            {"role": "assistant", "content": "Keypoints:"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=300,
            temperature=0.6,
            n=1,
            stop=None
        )
        summary = response.choices[0].message['content'].strip()
        summary_list.append(summary)

        # Join all summaries into one string
        summary = '\n'.join(summary_list)

        model_engine = "text-davinci-003"
        temperature = 0  # Increase or decrease this to control the creativity of the generated title

        prompt_request = "Give a appropriate title for the meeting as accurate and less randomized as possible. If you feel the title accuracy is less than 70% print not sure in brackets. Also make sure the sentence is complete and does not end in conjunctions or prepositions"+summary
        title = openai.Completion.create(
            engine=model_engine,
            prompt=prompt_request,
            temperature=temperature,
            n=1,
            frequency_penalty=0,
            presence_penalty=0
        ).choices[0].text.strip()

        model_engine = "text-davinci-002"

        prompt_request = (f"Given a transcript, extract the date and time in the format \"date: DD/MM/YYYY, time: HH:MM AM/PM\""
                          f" and return it as a string.\n\n"
                          f"Transcript: {chunk}\n"
                          f"Date: "
                          f"Time: "
                          )
        # prompt= (f"Given a transcript, extract the date and time in the format "date: DD/MM/YYYY, time: HH:MM AM/PM" and return it as a string. \n\n{chunk}\n\nDate:\nTime:")
        # response = openai.Completion.create(
        #     engine=model_engine,
        #     prompt=prompt_request,
        #     max_tokens=1024,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )
        # date = response.choices[0].text.split("Date:")[0].split("Time:")[0].strip()
        # time = response.choices[0].text.split("Time:")[0].strip()
        # return date, time
        model_engine = "text-davinci-002"

        prompt_request = (f"Given a transcript, extract the date and time in the format \"date: DD/MM/YYYY, time: HH:MM AM/PM\""
                          f" and return it as a string.\n\n"
                          f"Transcript: {chunk}\n"
                          f"Date: "
                          f"Time: "
                          )
        # prompt= (f"Given a transcript, extract the date and time in the format "date: DD/MM/YYYY, time: HH:MM AM/PM" and return it as a string. \n\n{chunk}\n\nDate:\nTime:")
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt_request,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        date = response.choices[0].text.split(
            "Date:")[0].split("Time:")[0].strip()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract a list of people mentioned in the following transcript and make sure to print name of each attendee on a new line with numbering or bullet points\n{chunk}\n\nAttendees:",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract names from response
        names = re.findall(r'(?i)\b[a-z]+\b', response.choices[0].text)
        # Remove duplicates and return list of attendees

        attendee_list = list(set(names))

    #     # get action items from meting transcript
        action_response = []

        # chunks = break_up_file_to_chunks(transcript)
        for i, chunk in enumerate(chunks):

            prompt_request = "Act as a meeting note taker, and Provide a list of action items with a due date from the provided meeting transcript text . Highlight to-do lists and which person is supposed to complete which task as highly precisely as possible. Make sure to give any numbering to each keypoint print each keypoint on a new line." + \
                chunk
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

            prompt_request = "Provide a list of action items with a due date from the provided meeting transcript text in points with numbering and print each point on new line: " + \
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

            translate,lan=traslate_language_english(summary)
            print(translate)
            # print(lan)

        results = jsonify(summary=summary, title=title, actionItems=points,
                          date=date, meetingAttendees=attendee_list)
        # Save the results in a text file named 'summary.txt'
        # with open("results/summary.txt", "w") as f:
        # f.write(title,date,summary,points)

        return results


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


app.config['UPLOAD_FOLDER'] = "C:/Users/dll/Downloads/stm"


@app.route("/summarize_vtt", methods=["POST"])
def summarize_txt():
    transcript_file = request.files['file']
    filename = secure_filename(transcript_file.filename)
    transcript_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    transcript_file = vtt_to_clean_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # transcript_file = request.files["file"]
    # vtt_to_clean_file(transcript_file)
    # transcript_text = transcript_file.read().decode("utf-8")
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript_text = f.read()
        result = summarize_transcript(transcript_text)
        return result