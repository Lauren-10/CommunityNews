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

