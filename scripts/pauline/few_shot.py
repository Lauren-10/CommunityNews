from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
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
print(few_shot_prompt.format())
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

print(chain.invoke({"input": "What's the square of a triangle?"}))
print(type(final_prompt))