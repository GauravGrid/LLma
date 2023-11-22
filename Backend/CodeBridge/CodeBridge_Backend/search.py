from langchain.chat_models import ChatAnthropic
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import List
from . import keys
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import GuardrailsOutputParser

import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict
import pickle

def preprocess(text):
    text = text.replace('/',' ')
    text = text.replace('_',' ')
    text = text.replace('-',' ')
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def preprocess_c2_m2(text):
    text = text.replace('/',' ')
    text = text.replace('_',' ')
    text = text.replace('-',' ')
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    weighting_token=[]
    for token in tokens:
        if token == 'customer':
            weighting_token.append('customer')
        if token == 'management':
            weighting_token.append('management')
    tokens = tokens+ weighting_token
    return tokens

def preprocess_c3_m2(text : string):

    text = text.replace('/',' ')
    text = text.replace('_',' ')
    text = text.replace('-',' ')
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    weighting_token=[]
    for token in tokens:
        if token == 'customer':
            weighting_token.append('customer')
            weighting_token.append('customer')
        if token == 'management':
            weighting_token.append('management')
    tokens = tokens+ weighting_token
    return tokens

def preprocess_c3_s2(text : string):

    text = text.replace('/',' ')
    text = text.replace('_',' ')
    text = text.replace('-',' ')
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    weighting_token=[]
    for token in tokens:
        if token == 'customer':
            weighting_token.append('customer')
            weighting_token.append('customer')
        if token == 'search':
            weighting_token.append('search')
    tokens = tokens+ weighting_token
    return tokens


def build_inverted_index(documents):
    inverted_index = defaultdict(list)

    for doc_id, document in enumerate(documents):
        text = document['business_logic']
        tokens = preprocess_c3_m2(text)

        term_frequency = defaultdict(int)
        for position, token in enumerate(tokens):
            term_frequency[token] += 1
            inverted_index[token].append((document['id'], term_frequency[token], position))

    return inverted_index

def search_inverted_index(inverted_index, query_collections):
    search_results = []
    result_dict = {}
    for collection in query_collections:
        collection_id = []
        for token in collection:
            search_ids = defaultdict(int)
            for doc_id, term_freq, position in inverted_index[token]:
                search_ids[doc_id] += term_freq
            collection_id.append(search_ids)
        common_keys_set = set(collection_id[0].keys())

        for dictionary in collection_id[1:]:
            common_keys_set.intersection_update(dictionary.keys())

        common_dict = {}
        for key in common_keys_set:
            common_dict[key] = sum(dictionary[key] for dictionary in collection_id)
        search_results.append(common_dict)
    for dictionary in search_results:
        for key, value in dictionary.items():
            if key in result_dict:
                result_dict[key] = max(result_dict[key], value)
            else:
                result_dict[key] = value
                
    sorted_results = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_results
def search_inverted_index_customer(inverted_index,query):
    search_results = []
    result_dict = {}
    # for collection in query_collections:
    collection_id = []
    for token in query:
        search_ids = defaultdict(int)
        for doc_id, term_freq, position in inverted_index[token]:
            search_ids[doc_id] += term_freq
        collection_id.append(search_ids)
    common_keys_set = set(collection_id[0].keys())

    for dictionary in collection_id[1:]:
        common_keys_set.intersection_update(dictionary.keys())

    common_dict = {}
    for key in common_keys_set:
        common_dict[key] = sum(dictionary[key] for dictionary in collection_id)
    search_results.append(common_dict)

    for dictionary in search_results:
        for key, value in dictionary.items():
            if key in result_dict:
                result_dict[key] = max(result_dict[key], value)
            else:
                result_dict[key] = value
                
    sorted_results = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_results

def save_inverted_index(inverted_index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(inverted_index, file)

def load_inverted_index(filename):
    with open(filename, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index

def getText(tokens):
    text = ""
    for token in tokens:
        text += str(token) + " "
    return text.rstrip(" ")

class Output(BaseModel):
    module_names : List[str] = Field(description="Collection of all the modules mentioned in the list provided")
    functionalities : List[str] = Field(description="Collection of all the functionalities of module/sub-modules")

template = """
Assistant is a large language model trained by Anthropic AI.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. 
As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand. 
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions.  
Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist. 
Assistant is very good at NER i.e Named Entity Recognition.

Context:
In our application, we have 5 main modules/micro-services:
1) Work order 
2) Customer 
3) Chassis 
4) Spare parts 
5) Part + Time import from external systems

Now based on this, user can ask any query on these modules/micro-services and their sub-modules. 
Now we need to get all the named entities or keywords related to these modules/micro-services or their sub-modules from the list(generated from the query) provided by the user.
The keywords/entities returned will be used to do a keyword search and get all the relevant files from the respective modules based on the query. So only return those keywords which will help in filtering out those module/sub-module files.

Standard keyword types :
1. Module/micro-services names
2. Functionalities implemented by the modules

###
Instructions :
1. Identify and return only any module, services, functionality keywords/entities from the list provided.
2. The entities/keywords returned should be only related to the specified modules/micro-services, their sub-modules or functionalities implemented by them.
3. Go through the response generated and if you feel the reponse can be better, go back to step 1 keeping in mind the analysis.
###
Human: {input} Identify and return only any module, services, functionality entities/keywords from the list provided. Take a deep breath and think step by step.

Assistant: 

Response format:
{format_instructions}
"""

parser = PydanticOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()

prompt = PromptTemplate(
    template=template,
    input_variables=["input"],
    partial_variables={"format_instructions": format_instructions}
)




llm =  ChatAnthropic(
        temperature=0,
        model="claude-2.0",
        anthropic_api_key=keys.anthropic_key
)


def getEntities(query):
    _input = prompt.format_prompt(input=query)
    output = llm.predict(_input.to_string())
    output=parser.parse(output)
    try :
        result = []
        print(output.module_names+output.functionalities)
        for a in output.module_names+output.functionalities:
            result = result + preprocess(a)
        return result
    except Exception as e:
        print("Error in identifying named entities")

import sqlite3







import pinecone

pinecone.init(
    api_key=keys.pinecone_key,
    environment="us-east-1-aws"
)

index = pinecone.Index("scania-business-logic")
import os
os.environ['OPENAI_API_KEY'] = keys.openai_key
from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_ids(query):
    connection = sqlite3.connect('/Users/vjain/V2/LLma/Backend/CodeBridge/db2.sqlite3')
    cursor = connection.cursor()
    sql_statement = 'SELECT file_name,logic FROM CodeBridge_Backend_scaniabusinesslogic'
    cursor.execute(sql_statement)
    rows = cursor.fetchall()
    documents = []
    for row in rows:
        document = { 'id': row[0], 'business_logic': row[1] }
        documents.append(document)
    ids=[]
    customer_index = build_inverted_index(documents)
    query = preprocess(query)
    query = getEntities(str(query))
    results = search_inverted_index_customer(customer_index, query)
    for doc_id, score in results:
        if score > 1:
            ids.append(doc_id)
    return ids

def get_search_list(query):
    ids = get_ids(query)
    corpus_embedding_openai = get_embedding(getText(preprocess(query)),model='text-embedding-ada-002')
    matches_preprocessed = index.query(
        vector = corpus_embedding_openai,
        top_k = 2033,
    )
    result = []
    
    for match in matches_preprocessed['matches']:
        # if (match['id'] in ids):
            result.append(match['id'])
            print(match)
            
    return result[:10]