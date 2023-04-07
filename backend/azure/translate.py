#Module for converting the regional lanugage Text to English language for text analysis and classification models

# Add your key and endpoint

import requests, uuid, json
key = "dfd945b69b244a48bd027cfe0ed8e903"
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = "centralindia"
path = '/translate'
constructed_url = endpoint + path

#Automatically Detects the language ofthe text and then converts them into English and Hindi Language

def traslate_language_english(text):
   
    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.

    params = {
        'api-version': '3.0',
        'to': ['hi', 'en']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text':text,
       }        ]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated=json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    translated_eng=response[0]['translations'][0]['text']
    detected_lang=response[0]['detectedLanguage']['language']
    print (translated_eng)
    # print(detected_lang)


    return translated_eng,detected_lang


  