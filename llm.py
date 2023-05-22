import os
import openai
from langchain.chat_models import ChatOpenAI
from llama_index import ComposableGraph, GPTListIndex, LLMPredictor, GPTVectorStoreIndex, ServiceContext, \
    SimpleDirectoryReader

from file import check_index_file_exists, get_index_filepath, get_name_with_json_extension
from dotenv import load_dotenv
from util import get_file_extension
from llama_index import download_loader
from pathlib import Path

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.2, model_name="gpt-3.5-turbo"))

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

def create_index(filepath, filename):
    file_type =  get_file_extension(filename)
    documents = None
    if file_type == "pdf":
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(Path(filepath))
    else: 
        documents = SimpleDirectoryReader(input_files=[filepath]).load_data()
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
    return index


def get_index_by_index_name(index_name):
    index_name = get_name_with_json_extension(index_name)
    if check_index_file_exists(index_name) is False:
        return None
    index_filepath = get_index_filepath(index_name)
    index = GPTVectorStoreIndex.load_from_disk(index_filepath, service_context=service_context)
    return index


def create_graph(index_sets, graph_name):
    graph = ComposableGraph.from_indices(GPTListIndex,
                                         [index for _, index in index_sets.items()],
                                         index_summaries=[f"This index contains {indexName}" for indexName, _ in index_sets.items()],
                                         service_context=service_context)
    return graph