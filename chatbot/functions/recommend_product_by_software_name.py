from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)
from langchain.document_loaders import PyPDFLoader
from langchain.retrievers import BM25Retriever
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
import json

from ..pydanticBaseModel.pydanticBaseModel import SoftwareHardwareRecommendations, Software
from .search_system_requirements import search_system_requirements

from ...db_funcs.product_controller import get_product_local_specs, get_product_by_id

def get_system_requirements(softName):
    get_sys_reqs_model = ChatOpenAI(
        engine="gpt-35-turbo-16k",  # engine = "deployment_name"
    ).bind(functions=[format_tool_to_openai_function(search_system_requirements)])
    get_sys_reqs_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You will be given name of an application or software. You will find system requirements of that software base on provided tool.""",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    preprocess_get_sys_reqs_chain = get_sys_reqs_prompt | get_sys_reqs_model | OpenAIFunctionsAgentOutputParser()
    get_sys_reqs_chain = (
    RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"]),
        )
        | preprocess_get_sys_reqs_chain
    )
    get_sys_reqs_executor = AgentExecutor(agent=get_sys_reqs_chain, tools=[search_system_requirements], verbose=True)

    system_requirements = get_sys_reqs_executor.invoke({"input": softName})

    print("\n 3 --- ", system_requirements, '---\n')
    return system_requirements['output']


def get_relevant_db_response(deviceType, system_requirements):
    response = get_product_local_specs(catergory_name=deviceType)
    print("\n 4.1------", response)

    doc_list = [json.dumps({"product id": id, "product specification": product}) for id, product in response]

    retriever = BM25Retriever.from_texts(doc_list)
    retriever.k = 5
    relevant_db_response = retriever.get_relevant_documents(system_requirements)
    
    print("\n 4------", relevant_db_response)

    return relevant_db_response

def get_recommendation_product(relevant_db_response, system_requirements):
    products = "\n".join(item.page_content for item in relevant_db_response)

    print("\n---6", products)
    print("\n type of", type(products))
    print("\n type of", type(system_requirements))
    

    recommendation_product_prompt = PromptTemplate.from_template("""
    You will be given:
        - A list of 5 products with their ID and specification
        - system requirements for an application
                                                                 
    5 products:
    {products}
                                                                 
    system requirements:
    {system_requirements}
    
    Your task is choose 2 suitable product out of those 5 which most suitable to use that application and give user that 2 product id.
    You must return the answer under python dictionary format with NO additional word, for example: '[id1, id2]'. For example: '[123, 456]'                                      
    """)

    recommendation_product_model = ChatOpenAI(
        engine="gpt-35-turbo-16k",  # engine = "deployment_name"
    )

    recommendation_product_chain = recommendation_product_prompt | recommendation_product_model

    result = recommendation_product_chain.invoke({"products": products, "system_requirements": system_requirements})
    print("\n---5", result)

    return result.content

# @tool(args_schema=SoftwareHardwareRecommendations)
@tool()
def recommend_product_by_software_name(query, softName, deviceType):
    # """Recommending the suitable hardware devices (desktops, laptops, tablets, etc.) for running a software (Photoshop, AutoCAD, MatLAB, etc.) given software's system requirements. Need both hardware type (phone, laptops, etc.), software name and software's system requirements from search_system_requirements tool. """
    """Recommending the suitable hardware devices (desktops, laptops, tablets, etc.) for running a software (Photoshop, AutoCAD, MatLAB, etc.) given software's system requirements. Need 3 inputs are 
    query: key phrase of the question or the query of the customer.
    softName: software name.
    deviceType: hardware devices type (current available choice are: laptop, apple, audio, accessories, games, streams) """

    # system_requirements = search_system_requirements(query.query)
    print("\n --- ", query, '---\n')
    print("\n --- ", softName, '---\n')

    system_requirements = get_system_requirements(softName)
    relevant_db_response = get_relevant_db_response(deviceType, system_requirements)
    id_list_string  = get_recommendation_product(relevant_db_response, system_requirements)
    array_id = [int(product_id) for product_id in id_list_string.strip('[]').split(', ')]
    
    response = [get_product_by_id(product_id) for product_id in array_id]


    print("\n 4.2------", response)
    print("\n tpe of", type(response[0]))
    result = [json.dumps({"product name": name, "product specification": product}) for name, product in response]


    return "\n".join([system_requirements, "Suitable product: \n"] + result)
