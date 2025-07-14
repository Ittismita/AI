from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import my_search_tool, wiki_tool, save_to_textfile

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
parser=PydanticOutputParser(pydantic_object=ResearchResponse)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools=[my_search_tool, wiki_tool, save_to_textfile]

agent=create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
agent_executer=AgentExecutor(agent=agent, tools=tools, verbose=True)
query=input("Enter your query")

raw_response=agent_executer.invoke({"query":query})



try:
    structured_response=parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)
