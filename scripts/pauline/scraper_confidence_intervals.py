from langchain_openai import ChatOpenAI
from scn_src.confidence_intervals import auto_precision_recall


if __name__ =="__main__":
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    schema = {
        "properties": {
            "news_article_title": {"type": "string"},
            "news_article_author": {"type": "string"},
            "news_article_publication_date": {"type": "string"},
            "is_author_student_college_student": {"type":"boolean"},
            "is_author_student_journalist": {"type":"boolean"},
            "is_article_university_collaboration": {"type":"boolean"}
        },
        "required": ["news_article_title","news_article_summary", "news_article_author",'is_author_student_journalist','is_article_university_collaboration','is_author_college_student'],
    }
    tags_to_extract = ['p','span','a','div']
    print(auto_precision_recall(10, llm, schema, tags_to_extract))