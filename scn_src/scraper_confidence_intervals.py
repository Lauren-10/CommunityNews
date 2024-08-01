from langchain_openai import ChatOpenAI
from scn_src.confidence_intervals import auto_precision_recall
from prompt_draft import prompt
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class Article(BaseModel):
    news_article_author: str = Field(description="the author's name, identify the First and Last name of the article author.")
    is_author_student_journalist: str = Field(description="""whether or not the article is student written
            respond false if the author
            is a professional journalist, former student, or ambiguous, 
            true if the author is a university student.
            In the event that two or more authors appear, format the output as so:
            "Name and Name and Name, boolean". if one author on the article is a student, consider
            that article to be student written""")

if __name__ =="__main__":
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    #schema = {
        #"properties": {
            #"news_article_author": {"type": "string"},
            #"is_author_student_journalist": {"type":"boolean"}
      #  },
       # "required": ["news_article_author",'is_author_student_journalist'],
    #}
    tags_to_extract = ['p','span','a','div']
    print(auto_precision_recall(10, llm, prompt(), Article, tags_to_extract))
