import os
from nltk.tokenize import word_tokenize
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import nltk
from dotenv import load_dotenv
import dateparser
import re
from STM import STM
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
        return list(STM.break_up_file(tokens, chunk_size, overlap_size))

    def convert_to_prompt_text(tokenized_text):
        prompt_text = " ".join(tokenized_text)
        prompt_text = prompt_text.replace(" 's", "'s")
        return prompt_text

    prompt_response = []

    chunks = STM.break_up_file_to_chunks(transcript)
    for i, chunk in enumerate(chunks):
        prompt_request = "Summarize this meeting transcript: " + STM.convert_to_prompt_text(
            chunks[i]
        )
        max_tokens = len(STM.convert_to_prompt_text(chunks[i]).split()) // 2
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

        title = re.search(
            r"(?i)^(?:the )?(?:minutes|summary|recap|notes) of(?: the)? (.+?(?<!\\))\n", meeting_summary)
        if title:
            title = title.group(1).replace("\\n", "\n")
        # else:
        #     title = "Meeting Summary"

        prompt_request = "Consoloidate these meeting summaries: " + \
            str(prompt_response)
        messages = [
            {"role": "system", "content": "This is text summarization."}]
        messages.append({"role": "user", "content": prompt_request})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # get action items from meting transcript
        action_response = []

        chunks = STM.break_up_file_to_chunks(transcript)
        for i, chunk in enumerate(chunks):

            prompt_request = "Provide a list of action items with a due date from the provided meeting transcript text: " + \
                STM.convert_to_prompt_text(chunks[i])
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

        chunks = STM.break_up_file_to_chunks(transcript)
        for i, chunk in enumerate(chunks):

            prompt_request = "Provide a list of action items with a due date from the provided meeting transcript text: " + \
                STM.convert_to_prompt_text(chunks[i])
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


@app.route("/summarize", methods=["POST"])
def summarize():
    transcript_file = request.files["file"]
    transcript_text = transcript_file.read().decode("utf-8")
    result = summarize_transcript(transcript_text)
    return result
