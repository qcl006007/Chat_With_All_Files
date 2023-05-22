import uuid
from file import (check_index_file_exists,
                  get_index_name_from_file_path, get_index_name_from_compress_filepath)
from llm import get_index_by_index_name, create_index
from string import Template


def check_llama_index_exists(file_name):
    index_name = get_index_name_from_file_path(file_name)
    return check_index_file_exists(index_name)


def create_llama_index(filepath, filename):
    index = create_index(filepath, filename)
    return index


def get_answer_from_index(question, index):
    query_engine = index.as_query_engine()
    question_tmp = Template("Given this information, Please answer my question in the same language that I used to ask you.\n"
    "Please answer the question: ${question}\n")
    question_str = question_tmp.substitute(question = question);
    return query_engine.query(question_str)

