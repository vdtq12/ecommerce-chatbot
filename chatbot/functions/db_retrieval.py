from langchain.utilities import SQLDatabase
import os
from dotenv import load_dotenv
from langchain.agents import tool
from ..pydanticBaseModel.pydanticBaseModel import CustomerInput
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)

from ...db_funcs.product_data import get_product_data


load_dotenv()
# db = SQLDatabase.from_uri(os.getenv("DATABASE_URI"))


@tool(args_schema=CustomerInput)
def find_product(query: CustomerInput):
    """Answer customer question about finding a product in BKTechStore with customer requirement"""

    input = query

    model = ChatOpenAI(engine="gpt-35-turbo-16k", temperature=0)

    prompt = PromptTemplate.from_template(
        """Given the provided table information and the user's question, you need to generate an SQL query based on the information.
        However, if there is no suitable SQL query that can be adapted to the user's question, you should only respond with the phrase "cannot generate sql"


    Question: {input}
    



    Table Information:
    CREATE TABLE IF NOT EXISTS product_line(
        product_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        category TEXT,
        supplier TEXT NOT NULL ,
        name VARCHAR(30) NOT NULL ,
        description text DEFAULT 'Đang cập nhật',
        CONSTRAINT fk_product_category
            FOREIGN KEY (category) REFERENCES category(category_name)
                ON DELETE set NULL
                ON UPDATE CASCADE,
        CONSTRAINT fk_product_supplier
            FOREIGN KEY (supplier) REFERENCES supplier(code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS product(
        product_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY  ,
        name TEXT not null ,
        sku CHAR(10) UNIQUE ,
        images text[],
        local_specs JSONB,
        quantity QUANTITY DEFAULT 1,
        price PRICE,
        is_standard BOOLEAN DEFAULT FALSE,
        product_line SERIAL NOT NULL ,
        CONSTRAINT fk_productLine
            FOREIGN KEY (product_line) REFERENCES product_line(product_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS supplier(
        code TEXT PRIMARY KEY ,
        name TEXT UNIQUE
    );

    


    Table Sample Insert Data:
    INSERT INTO supplier (code)
        VALUES ('asus'), ('dell'), ('apple'), ('acer'), ('hp'), ('lenovo'), ('msi'), ('kingston'), ('intel'), ('seagate'), ('corsair'), ('adata'), ('sandisk'), ('xigmatek'), ('samsung'), ('gigabyte'), ('wd'), ('deepcool'), ('soundpeats'), ('jbl'), ('dareu'), ('havit'), ('lg'), ('bose'), ('xiaomi'), ('microtek'), ('baseus'),('logitech'), ('hyperx'), ('soundmax'), ('sdrd'), ('razer'), ('segotep'), ('nzxt');
    
    INSERT INTO product_line (category, name, supplier, description) VALUES  ('laptop', 'lenovo ideapad', 'lenovo', 'this is the lenovo idealpad description'),

    INSERT INTO public.product (local_specs, quantity, price, is_standard, product_line, sku, images) VALUES  ('this is example specification list', 18, 15490000, false, 2, '22100234814 ', 'this is place holder for the real images list'),



    Query Instruction:
    Not select attribute `images`, `sku` while in the SQL statements. You are encouraged to join the product_line and product tables together in the SQL query.
    In case need to query N records of data, select limit upto 5.

    


    Some basic example output:
    SELECT * FROM product;
    SELECT product.name, product.price, product_line.description FROM product INNER JOIN product_line ON product.product_line=product_line.product_id;

    


    Please note that you should not make up or guess any additional information or additional newline when generating the SQL query.
    """
    )

    qa_chain = prompt | model | OpenAIFunctionsAgentOutputParser()
    res = qa_chain.invoke({"input": query})
    print(res.return_values['output'])

    get_product_data(res.return_values['output'])
    # return ""
    # input = query
    # find_model = ChatOpenAI(
    #     engine="gpt-35-turbo-16k", temperature=0  # engine = "deployment_name"
    # )

    # chain = create_sql_agent(
    #     llm=find_model,
    #     # toolkit=SQLDatabaseToolkit(db=db, llm=find_model),
    #     verbose=True,
    #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     input_variables=["input", "agent_scratchpad"],
    #     handle_parsing_errors=True,
    # )

    # result = chain.run(
    #     """You are an agent designed to interact with a SQL database.
    #     Please answer the user question base on following instruction:

    #     Instruction:
    #     The `product_line` table has 5 columns: `category`, `name`, `supplier`, `description`, `product_id`.
    #     The `product_line` table represents the information with each record contains information of a product.
    #     The `product` table has 7 columns: `local_specs`, `quantity`, `price`, `is_standard`, `sku`, `images`, `product_line`.
    #     The `product` table represents the information with each record contains specification information of a product.
    #     The `product_line` of the `product` table is REFERENCES to `product_id` of `product_line` table.

    #     Join the `product` table and `product_line` table and just take these attributes / column: `category`, `name`, `supplier`, `local_specs`, `price`,`quantity`.
    #     (join by `product_line` of `product` table and `product_id` of `product_line` table).
    #     In case need to query N records of data, select limit upto 5.
    #     From the join result and user question, generate suitable query to answer user question.

    #     User question: {input}."""
    # )

    return "can not find the result"
