
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
import asyncio
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
import pandas as pd

def extract(content: str, schema: dict,llm):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

def load_docs(urls,tags_to_extract = ["span",'p','a','li']): 
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract= tags_to_extract
    )
    
    return docs_transformed 
    
def extract_metadata(doc,schema,llm):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4097, chunk_overlap=0
    )
    splits = splitter.split_documents([doc])
    if splits == []:
        print("URL doesnt work")
    elif splits != []:
        extracted_content = extract(schema=schema, content=splits[0],llm = llm)
        print("extracted content", extracted_content)
        return extracted_content[0]

def extract_all_metadata(urls,llm,schema,tags_to_extract = ['p','span','a','div']):
    docs = load_docs(urls,tags_to_extract=tags_to_extract)
    extracted_content_list = []
    for i,doc in enumerate(docs): 
        print(f"extracting document: {i}")
        print(urls[i])
        #print(docs)
        #print(type(docs))
        metadata = extract_metadata(doc,schema,llm)
        if metadata is None:
            continue
        metadata["urls"] = urls[i]
        extracted_content_list.append(metadata)
        #extracted_content_list.append(extract_metadata(doc,schema,llm))
    return extracted_content_list
    
    
