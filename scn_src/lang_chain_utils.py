
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
    #return create_extraction_chain(schema=schema, llm=llm, prompt=prompt).run(content)
    chain=prompt|llm.with_structured_output(schema=schema)
    final_chain=chain.invoke({"input":content})
    return vars(final_chain)
    

def load_docs(urls,tags_to_extract = ["span",'p','a','li']): 
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract= tags_to_extract
    )
    
    return docs_transformed 
    
def extract_metadata(doc,schema,llm, prompt):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4097, chunk_overlap=0
    )
    splits = splitter.split_documents([doc])
    if splits == []:
        print("URL doesnt work")
    elif splits != []:
        extracted_content = extract(content=splits[0], schema=schema, llm = llm, prompt=prompt)        
        print("extracted content", extracted_content)
        return extracted_content

def extract_all_metadata(urls,llm,prompt,schema,tags_to_extract = ['p','span','a','div']):
    docs = load_docs(urls,tags_to_extract=tags_to_extract)
    extracted_content_list = []
    for i,doc in enumerate(docs): 
        print(f"extracting document: {i}")
        print(urls[i])
        #print(docs)
        #print(type(docs))
        metadata = extract_metadata(doc,schema,llm, prompt=prompt)
        if metadata is None:
            continue
        metadata["urls"] = urls[i]
        extracted_content_list.append(metadata)
        #extracted_content_list.append(extract_metadata(doc,schema,llm))
    breakpoint()
    is_student = []
    for i in extracted_content_list:
       is_student.append(i["is_article_university_collaboration"] or i["is_author_student_journalist"])
    return extracted_content_list
    
    
