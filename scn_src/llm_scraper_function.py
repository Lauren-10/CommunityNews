from scn_src.lang_chain_utils import extract_all_metadata
import pandas as pd

#done
def run_llm_scraper(df, llm, prompts, schema, tags_to_extract):
    '''
    called by innter_chatgpt_to_sql. for each url in the chunk, run extract_all_metadata to access author and is_student data
    output: dataframe, stored in sql_pipeline.py as chat_gpt_data_df variable

    Parameters:
    df (df): a chunk created in the last step
    llm (ChatOpenAI class object): specifies temperature and model name
    prompts (list of strs): defined in prompt_draft.py
    schema (Article(BaseModel) class object): specifies structure of llm output
    tags_to_extract (list of strs):  locates portions of HTML for scraper to process

    Returns: 
    final_df: author and is_student data for each url in chunk
'''
    urls = df["url"]
    url_list = urls.to_list() 
    extracted_urls = extract_all_metadata(url_list, llm=llm, prompts=prompts, schema=schema, tags_to_extract=tags_to_extract)
    final_df = pd.DataFrame.from_dict(extracted_urls,orient='columns')
    return final_df