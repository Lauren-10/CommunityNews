
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI

#schema is a list of dictionaries which is the metadata we want to scrape and pull
#extract is an object
def extract(content: str, schema: dict,llm):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

#chromium is a class of the object loader. This uses chromium to get through to scraping and go past barriers
#load is a method of putting the extracted data into a document
#using BSTransformer to get BS objects, BS transformer is a class
#transform documents goes into the HTML and takes the tags to extract
def load_docs(urls,tags_to_extract = ["span",'p','a','li']): 
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p", "li", "div", "a"]
    )
    
    return docs_transformed 
#docs transformed is a variable that will become our dataframe, our output in the format we want it in
    
#chunk size is the amount of tokens we take, so that we have an appropriate context window and chatgpt knows what it is doing
def extract_metadata(doc,schema,llm):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4097, chunk_overlap=0
    )
    splits = splitter.split_documents([doc])
    extracted_content = extract(schema=schema, content=splits[0],llm = llm)
    return extracted_content

#this appends the extracted metadata into a list that is created above
#the try/except loop goes through while the for loop is scraping each website and telling us its progress,
# and the try/except loop makes sure it doesn't get blocked at each url that doesn't work and gives us an error message for each one 
def extract_all_metadata(urls,llm,schema,tags_to_extract = ['p','span','a','div']):
        docs = load_docs(urls,tags_to_extract=tags_to_extract)
        extracted_content_list = []
        for i,doc in enumerate(docs): 
            try:
                print(f"extracting document: {i}")
                extracted_content_list.append(extract_metadata(doc,schema,llm))
            except: 
                print(f"Error accessing {doc}")
        return extracted_content_list
        
    
    
