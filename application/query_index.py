# author=simin.li

import os
from tqdm import tqdm
import time
from llama_index import GPTSimpleVectorIndex#, SimpleDirectoryReader
from llama_index.langchain_helpers.chain_wrapper import LLMPredictor
from langchain.llms import OpenAI
print('package loaded')
INDEX_PATH = 'index_vector1.json'


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
