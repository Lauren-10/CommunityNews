from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI


examples = [
    {"input": """"This story was produced by Fresh Take Florida,
a news service of the University of Florida College of Journalism and Communications.
The reporter can be reached at vivienneserret@ufl.edu.
You can donate to support our students here
""", "output": "True"},
    {"input": "By WVUA 23 Student News Reporter Nick Balenger", "output": "True"},
    {"input": "Saman Shafiq is a trending news reporter for USA TODAY. Reach her at sshafiq@gannett.com and follow her on X @saman_shafiq7.", "output": "False"},
    {"input": """Noah Biesiada is a Voice of OC reporter and corps member with Report for America,
a GroundTruth initiative. 
Contact him at nbiesiada@voiceofoc.org or on Twitter @NBiesiada.
""", "output": "False"},
    {"input": "Melanie Mendez is a former student reporter at KUNR Public Radio.", "output": "False"},


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
        ("system", """You are an AI assistant that can classify articles
         as student written or reporter written, respond false if the author
         is a professional journalist or former student, true if the author is a university student"""),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)
chain = final_prompt | ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

print(chain.invoke({"input": """This story is jointly published by nonprofits Amplify Utah and The Salt Lake Tribune,
                     in collaboration with the University of Utah, to elevate diverse perspectives in local media through student journalism."""}))
