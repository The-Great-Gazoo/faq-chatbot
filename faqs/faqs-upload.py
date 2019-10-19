import requests
import json

# a parser that transforms data in faqs.txt for batch uploads to Genesys server
# for model training

json_array = []
external_url = "https://www.mycertifiedservice.ca/auto-maintenance-faqs.html"

with open("faqs.txt") as lines:
    content = lines.read().splitlines()

def build_doc(question, answer):
    doc = {
        "type": "faq",
        "faq": {
            "question": question,
            "answer": answer
        },
        "externalUrl": external_url
    }

    json_array.append(doc)

line_num = 0
question = ""
answer = ""
for line in content:
    # empty line indicates the start of a new question/answer pair (doc)
    if line == "":
        build_doc(question, answer)
        question = ""
        answer = ""
        line_num = 0
    elif line_num == 0:
        question += line
        line_num += 1
    else:
        if line_num > 1:
            answer += "\n"
        answer += line
        line_num += 1

# uncomment for diagnosis
# print(json_array)

def upload_to_genesys():
    global json_array

    payload = json.dumps(json_array)

    url = "https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases/c51a90c1-bb22-48f4-8dde-891fecdfb796/languages/en-US/documents"    
    
    headers = {
        'Content-Type': "application/json",
        'organizationid': "507c6b94-d35a-48ce-9937-c2e4aa69c279",
        'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmdJZCI6IjUwN2M2Yjk0LWQzNWEtNDhjZS05OTM3LWMyZTRhYTY5YzI3OSIsImV4cCI6MTU3MTUyMTE0MSwiaWF0IjoxNTcxNTE3NTQxfQ.MYYchq4mkWqIq4fAWwC-l3wuqJDYVQ1UdT8SqGuoDGE",
        'cache-control': "no-cache",
        'Postman-Token': "7c93c77c-a46f-4b95-bad6-d8e5db646b69"
    }

    response = requests.request("PATCH", url, data=payload, headers=headers)

    print(response.status_code)

upload_to_genesys()
