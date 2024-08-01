from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

def prompt():
    examples = [
        {"input": """"This story was produced by Fresh Take Florida,
    a news service of the University of Florida College of Journalism and Communications.
    The reporter can be reached at vivienneserret@ufl.edu.
    You can donate to support our students here
    """, "output": "Vivienne Serret, True"},
        {"input": "By WVUA 23 Student News Reporter Nick Balenger", "output": "Nick Balenger, True"},
        {"input": "Saman Shafiq is a trending news reporter for USA TODAY. Reach her at sshafiq@gannett.com and follow her on X @saman_shafiq7.", "output": "Saman Shafiq,False"},
        {"input": """Noah Biesiada is a Voice of OC reporter and corps member with Report for America,
    a GroundTruth initiative. 
    Contact him at nbiesiada@voiceofoc.org or on Twitter @NBiesiada.
    """, "output": "Noah Biesada,False"},
        {"input": "Melanie Mendez is a former student reporter at KUNR Public Radio.", "output": "Melanie Mendez, False"},
        {"input": """BY ANGELINA HICKS AND GRETA CIFARELLI...
        This dispatch is part of the Voice of OC Collegiate News Service, 
        working with student journalists to cover public policy issues across Orange County. 
        If you would like to submit your own student media project related to Orange County civics or if you have any response to this work,
        contact admin@voiceofoc.org.""", "output": "Angelina Hicks and Greta Cifarelli,True"},


    ]
    # This is a prompt template used to format each individual example.
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    #want to return final prompt
    #print(few_shot_prompt.format())
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are an AI assistant that can read and digest articles
            and pick up on two variables and place them into a comma seperated list:
            firstly, the author's name, identify the First and Last name
            of the article author.
            second, whether or not the article is student written
            respond false if the author
            is a professional journalist, former student, or ambiguous, 
            true if the author is a university student.
            Second, the author's name, identify the First and/or Last name
            of the article author.
            In the event that two or more authors appear, format the output as so:
            "Name and Name and Name, boolean". if one author on the article is a student, consider
            that article to be student written
            """),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    return final_prompt

chain = prompt() | ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

print(chain.invoke({"input": """Lucia McCallum interns as the Hardwick Gazette’s community resilience reporter
                     with support from the Leahy Institute for Rural Partnerships. She works with editors at Community News Service,
                     a University of Vermont journalism program."""}).content)
