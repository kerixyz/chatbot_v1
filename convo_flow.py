import json

with open('./assets/questions.json', 'r') as fp:
    questions = json.load(fp)

def find_questions():
    output = "```"
    for q in questions.keys():
        output += q + "\n"
    output += "```"
    return output