import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = "2023-07-01-preview"
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")

from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.agents import tool
from langchain.output_parsers.openai_functions import (
    JsonOutputFunctionsParser,
    JsonKeyOutputFunctionsParser,
)
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)
from langchain.tools.render import format_tool_to_openai_function
from langchain.schema.agent import AgentFinish
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.utilities import SQLDatabase
from langchain.schema import Document
from langchain.agents.agent_toolkits import (
    create_sql_agent,
    SQLDatabaseToolkit,
    create_csv_agent,
)
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory, ConversationSummaryMemory
from langchain.schema import BaseChatMessageHistory, BaseMessage, BaseMemory


# local function
from .pydanticBaseModel.pydanticBaseModel import CustomerInput
from .functions.search_system_requirements import search_system_requirements
from .functions.self_intro import answer_about_yourself
from .functions.store_intro import answer_about_bktechstore
from .functions.db_retrieval import find_product

tools_functions = [
    format_tool_to_openai_function(f)
    for f in [
        answer_about_yourself,
        search_system_requirements,
        answer_about_bktechstore,
        find_product
    ]
]


tools_model = ChatOpenAI(
    engine="gpt-35-turbo-16k",  # engine = "deployment_name"
).bind(functions=tools_functions)



agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You work as an assistant only for the BKTechStore website and your role is to respond to customer inquiries. 
            You will help the customer with their questions about the BKTechStore website which sells computer and related devices.
            If a question is NOT RELEVANT to the BKTechStore website or if there are no matching tools available, you should inform the customer that you are unable to answer their question.
            ONLY USE PROVIDED INFORMATION, MEMMORY INFORMATION AND TOOLS TO ASNWER.
            DO NOT MAKE UP or GUESS any additional information.
            
            Here are something you can do if user ask:
            - Answer questions about the products available on the website.
            - Provide information about the BKTechStore policies such as business information, privacy, transaction terms, online shopping guide, warranty policy, and contact information.
            - Assist with for system requirements of specific applications.
            - Provide general information or guidance about the website and its features.""",
        ),
        MessagesPlaceholder(variable_name="memory"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# memory = ConversationSummaryBufferMemory(human_prefix="user", ai_prefix="system", return_messages=True, memory_key="chat_history")
# memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
memory_llm = ChatOpenAI(
    engine="gpt-35-turbo-16k",  # engine = "deployment_name"
)

preprocess_agent_chain = agent_prompt | tools_model | OpenAIFunctionsAgentOutputParser()
# intermediate_steps = []

agent_chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"]),
        memory=lambda x: x["memory"],
    )
    | preprocess_agent_chain
)

tools = [answer_about_yourself, search_system_requirements, answer_about_bktechstore, find_product]

#invoke test
# print(
#     "\n --- ",
#     agent_executor.invoke({"input": "any ASUS laptop at your store ?"}),
#     " --- \n",
# )


#     agent_executor.invoke({"input": "hi"}),
#     agent_executor.invoke({"input": "what can you do ?"}),
#     agent_executor.invoke({"input": "I want to buy a laptop to use AutoCAD. What is the recommendation system requirements ?"}),
#     agent_executor({"input": "i want to buy a laptop to use minecraft. What is the recommend system requirements ?"}),
#     agent_executor.invoke({"input": "any ASUS laptop at your store ?"}),


class chatbot:
    def __init__(self, mem):
        self.memory = ConversationSummaryMemory(return_messages=True, memory_key="memory", llm=memory_llm)
        self.memory.buffer = mem
        self.agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=self.memory)
    
    def chat_public(self, query):
        try:
            result = self.agent_executor.invoke({"input": query})
            print("--- result: ", result)
            print("--- result: ", self.memory.buffer)
            return result["output"], self.memory.buffer
        except Exception as e:
            print(f"error: {str(e)}")
            return "Error fetching question", ""

