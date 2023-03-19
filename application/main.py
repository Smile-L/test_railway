#!/usr/bin/env /Users/lisimin/anaconda3/envs/py39/bin/python
# author=simin.li
from flask import Flask, request, Response
import json
from typing import List
import os
from tqdm import tqdm
import time
from llama_index import GPTSimpleVectorIndex#, SimpleDirectoryReader
from llama_index.langchain_helpers.chain_wrapper import LLMPredictor
from langchain.llms import OpenAI
print('package loaded')
INDEX_PATH = 'index_vector_urls.json'


class Indexer(object):
    llm = OpenAI(model_name='gpt-3.5-turbo', temperature=0)
    llmp = LLMPredictor(llm)

    index = GPTSimpleVectorIndex.load_from_disk(INDEX_PATH)
    index._llm_predictor = llmp
    print('index loaded')

    def query(self, query):
        response = self.index.query(query, similarity_top_k=1)
        source = '//'.join([n.extra_info.get('filename', '')
                              + f"({n.node_info.get('start', '')}-{n.node_info.get('end', '')})"
                              for n in response.source_nodes])
        return response.response+f'({source})'

indexer = Indexer()
print(indexer.query(query='test'))

print(__name__)
app = Flask(__name__)

@app.route('/test')
def test():
    return "Hello, World!"


@app.route('/chat-process', methods=['POST'])
# @auth.login_required
def chat_process():
    """"
    {
      "role": "assistant",
      "id": "chatcmpl-6uYrek3uKuA59Sx9OJIFyrLKhkK4Y",
      "parentMessageId": "d4acab1f-5f3b-41f0-8bce-ffab0b8ede56",
      "text": "This is a response to your third test. Please let me know if you have any questions or if there's anything I can help you with.",
      "detail": {
        "id": "chatcmpl-6uYrek3uKuA59Sx9OJIFyrLKhkK4Y",
        "object": "chat.completion.chunk",
        "created": 1678938406,
        "model": "gpt-3.5-turbo-0301",
        "choices": [
          {
            "delta": {},
            "index": 0,
            "finish_reason": "stop"
          }
        ]
      }
    }
    """
    req_data = request.get_json()
    prompt = req_data['prompt']
    options = req_data.get('options', {})
    # first_chunk = True
    #
    # def gen(chat_messages: List[ChatMessage]) -> str:
    #     nonlocal first_chunk
    #     output = ''
    #     for message in chat_messages:
    #         output += (json.dumps(message) if first_chunk else f"\n{json.dumps(message)}")
    #         first_chunk = False
    #     return output
    #
    # response = Response(gen(chatReplyProcess(prompt, options)), mimetype='application/octet-stream')
    response = indexer.query(prompt)
    return Response(json.dumps({
      "role": "assistant",
      "id": "chatcmpl-6uYrek3uKuA59Sx9OJIFyrLKhkK4Y",
      "parentMessageId": "d4acab1f-5f3b-41f0-8bce-ffab0b8ede56",
      "text": response,
      "detail": {
        "id": "chatcmpl-6uYrek3uKuA59Sx9OJIFyrLKhkK4Y",
        "object": "chat.completion.chunk",
        "created": 1678938406,
        "model": "gpt-3.5-turbo-0301",
        "choices": [
          {
            "delta": {},
            "index": 0,
            "finish_reason": "stop"
          }
        ]
      }
    }))# , mimetype='application/octet-stream'


# @app.route('/config', methods=['POST'])
# def config():
#     try:
#         response = chatConfig()
#         return response
#     except Exception as e:
#         return {
#             "status": "Fail",
#             'error': str(e),
#             "data": None
#         }


@app.route('/session', methods=['POST'])
def session():
    """
    {"status":"Success","message":"","data":{"auth":false}}
    """
    try:
        AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY")
        has_auth = isinstance(AUTH_SECRET_KEY, str) and len(AUTH_SECRET_KEY) > 0
        return {
            "status": "Success",
            "message": "",
            "data": {"auth": has_auth}
        }
    except Exception as e:
        return {
            "status": "Fail",
            "message": str(e),
            "data": None
        }
#
#
# @app.route('/verify', methods=['POST'])
# def verify():
#     try:
#         req_data = request.get_json()
#         token = req_data.get('token')
#         if not token:
#             raise ValueError('Secret key is empty')
#         if os.environ['AUTH_SECRET_KEY'] != token:
#             raise ValueError('密钥无效 | Secret key is invalid')
#         return {
#             "status": "Success",
#             "message": "Verify successfully",
#             "data": None
#         }
#     except Exception as e:
#         return {
#             "status": "Fail",
#             "message": str(e),
#             "data": None
#         }


# if __name__ == '__main__':
#     app.run(port=3002)
