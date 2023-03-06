from flask import Flask, jsonify, request

import time

from flask_cors import CORS

import os
os.environ["OPENAI_API_KEY"] = 'OPENAI_API_KEY'

from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex(documents)

# save to disk
index.save_to_disk('index.json')


# print(index.query("What is the mission statement of ttu"))
def generateResponse(query):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    return index.query(query)

app = Flask(__name__)
CORS(app)


@app.route("/chatbot", methods=["POST"])
def response():
    query = dict(request.form)['query']
    
    user_response = query
    user_response = user_response.lower()
        
    print(generateResponse(user_response))
    return jsonify(generateResponse(user_response))    
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
