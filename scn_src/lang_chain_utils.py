from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
import asyncio
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
import pandas as pd
from scn_src.prompt_draft import prompt

def extract(content: str, schema, llm, prompt):
    '''
    called by text_splitter. executes ChatGPT query on split tokens

    parameters:
    content (str): split tokens
    schema (Article(BaseModel) class object): specifies structure of llm output
    llm (ChatOpenAI class object): specifies temperature and model name 
    prompts (list of strs): defined in prompt_draft.py

    returns:
    dict: contains ChatGPT response, 
    '''

    chain=prompt|llm.with_structured_output(schema=schema)
    final_chain=chain.invoke({"input":content})
    return vars(final_chain)
    
#ASK WILL ABOUT THIS
def load_docs(urls,tags_to_extract = ["span",'p','a','li']): 
    '''
    called by extract_all_metadata. Locates portion of HTML in each url and converts it into legible datatype.

    Parameters:
    urls (list of strs): contains each url contained in chunk
    tags_to_extract (list of strs): locates portions of HTML for scraper to process
    
    Returns:
    Sequence of Documents: stored in extract_all_metadata as docs varaible.
 '''
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract= tags_to_extract
    )
    
    return docs_transformed 
    
def text_splitter(doc, schema, llm, prompts):
    '''
    called by extract_all_metadata. Uses a text splitter on each doc to create tokens, then sends each to ChatGPT with extract function.

    Parameters:
    doc (Document): contains transformed HTML data
    schema (Article(BaseModel) class object): specifies structure of llm output
    llm (ChatOpenAI class object): specifies temperature and model name 
    prompts (list of strs): defined in prompt_draft.py

    Returns:
    Dict: stored in extract_all_metadata as metadata variable
    '''
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4097, chunk_overlap=0
    )
    splits = splitter.split_documents([doc])
    if splits == []:
        print("URL doesnt work")
    elif splits != []:
        extracted_content = extract(content=splits[0], schema=schema, llm = llm, prompt=prompts)
        print("extracted content", extracted_content)
        return extracted_content


def extract_all_metadata(urls, llm, prompts, schema, tags_to_extract=['p','span','a','div']):
    '''
    called by run_llm_scraper in llm_scraper_function.py. 
    extracts the relevant portions of each url's HTML (docs), then runs extract_metadata on each doc to get author and is_student data

    Parameters:
    urls (list of strs): contains each url contained in chunk
    llm (ChatOpenAI class object): specifies temperature and model name
    prompts (list of strs): defined in prompt_draft.py
    schema (Article(BaseModel) class object): specifies structure of llm output
    tags_to_extract (list of strs): locates portions of HTML for scraper to process

    Returns:
    list of dicts: stored in llm_scraper_function.py as extracted_urls variable
 '''
    docs = load_docs(urls=urls, tags_to_extract=tags_to_extract)
    extracted_content_list = []
    for i,doc in enumerate(docs): 
        print(f"extracting document: {i}")
        metadata = text_splitter(doc,schema=schema,llm=llm, prompts=prompts)
        if metadata is None:
            continue
        metadata["urls"] = urls[i]
        extracted_content_list.append(metadata)
    return extracted_content_list
    
    
