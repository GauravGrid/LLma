from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain.chat_models import ChatAnthropic
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from sentence_transformers import SentenceTransformer, util

business_logic='''Based on the provided RPG code, here is my attempt to extract and explain the key business logic:

The code appears to be for some kind of sales/customer discount system. There are procedures for:

1. Converting strings to uppercase (toUppercase) and lowercase (toLowercase).

2. Allocating and deallocating memory for a pointer variable (allocSpace, deallocSpace).

3. Filling an array/file (HSHI12PF) with old discount codes (RCALT) from customer and order data.

4. Converting old discount codes (RCALT) to new codes (RCNEU) and updating data. This seems to be the core logic:

- It checks if discount code selection is made and only processes selected codes. 

- It gets old code (RCALT) and chains to find matching record.

- If old code not found, sets indicator that code was converted.

- If new code (RCNEU) exists, moves it to old code field and updates.

5. Building up old discount codes (RABAUF) by reading discount master file (RABSTAR).

6. Getting customers (KUNDEN) for old and new discount codes by chaining between customer and order files.

7. Displaying overview of new discount codes (UEBNEU) by reading discount mapping file (HSRAZPR):

- Again checks for code selection. 

- Evaluates discount code (RAZ012) to get description/purpose (ZWECK).

- Moves new code (RAZ010) and gets discount percentages (FUELWG). 

- Writes details to display file.


So in summary, it involves:

- String manipulation 

- Memory allocation

- File handling and chaining between customer, order and master files

- Discount code conversion and mapping 

- Generating displays/reports for users

The code interacts with these files:

- HSHI12PF: Internal array/file with old discount codes

- RABSTAR: Discount code master file

- AUFSTAR: Order file

- HSKUIPR: Customer file 

- HSRAZPR: Discount code mapping file

- HSHI12S1-S4: Display files

Let me know if any part needs more explanation!'''

def get_file_name(business_logic):

    class Par(BaseModel):
        file: List[str] = Field(description="A list of files names that interact with the database through associated code.")

    parser = PydanticOutputParser(pydantic_object=Par) 
    
    template='''
        Give me only a list of all file names and database files that are involved in the given business logic.

        Business Logic:
        {business_logic}

        Please provide the file names and database files in a formatted list.

        Response:
        {format_instructions}
    '''
    
    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key = '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', model = "claude-2.0", max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["business_logic"],partial_variables={"format_instructions":parser.get_format_instructions()}, template=template),
        verbose=True,
    )
    schema_str= llm_chain.predict(business_logic=business_logic)
    
    start_index = schema_str.find('"file": [') + len('"file": [')
    end_index = schema_str.find(']')
    files = [file.strip(' "\n') for file in schema_str[start_index:end_index].split(',')]
    print(files)
    
    dblist=['HSHI12PF', 'RABSTAR', 'AUFSTAR', 'HSKUIPR', 'HSRAZPR','AUFSTAM','RABSTAM','ERLSTAM',"ESZPF",'HSESZPF']
    
    new_files=[]
    for file_name in files:
        if(file_name in dblist):
            new_files.append(file_name)
    
    return new_files

def updated_business_logic(business_logic):
    
    file=get_file_name(business_logic)
    print(file)
    


    S7='''The data defination language of the database file name ERLSTAM is
                CREATE TABLE HDLDKW.ERLSTAM (
                    ERL010 CHAR(4) DEFAULT ' ' NOT NULL,
                    ERL020 CHAR(1) DEFAULT ' ' NOT NULL,
                    ERL030 CHAR(2) DEFAULT ' ' NOT NULL,
                    ERL040 CHAR(6) DEFAULT ' ' NOT NULL,
                    ERL050 CHAR(6) DEFAULT ' ' NOT NULL,
                    ERL060 CHAR(6) DEFAULT ' ' NOT NULL,
                    ERL070 CHAR(6) DEFAULT ' ' NOT NULL,
                    ERL080 DECIMAL(9,2) DEFAULT 0 NOT NULL
                );
                CREATE UNIQUE INDEX ERLSTAM ON HDLDKW.ERLSTAM (ERL010,ERL020,ERL030);
    '''

    S8='''The data defination language of the database file whose name HSESZPF is
                CREATE TABLE HDLZENTRAL.HSESZPF (
                    ESZ000 CHAR(3) DEFAULT ' ' NOT NULL,
                    ESZ010 CHAR(4) DEFAULT ' ' NOT NULL,
                    ESZ020 CHAR(1) DEFAULT ' ' NOT NULL,
                    ESZ030 CHAR(2) DEFAULT ' ' NOT NULL,
                    ESZ040 CHAR(6) DEFAULT ' ' NOT NULL,
                    ESZ050 CHAR(6) DEFAULT ' ' NOT NULL
                );
                CREATE UNIQUE INDEX HSESZPF ON HDLZENTRAL.HSESZPF (ESZ000,ESZ010,ESZ020,ESZ030);
                
                
    '''



    S16='''The data defination language of the database file name HSHI12PF is 
                CREATE TABLE HDLZENTRAL.HSHI12PF (
                    HI12000 CHAR(3) DEFAULT ' ' NOT NULL,
                    HI12010 CHAR(3) DEFAULT ' ' NOT NULL,
                    HI12020 CHAR(3) DEFAULT ' ' NOT NULL
                );
                CREATE INDEX HSHI12PF ON HDLZENTRAL.HSHI12PF (HI12000,HI12010);
    '''

    S17='''The data defination language of the database file name RABSTAM is 
                CREATE TABLE HDLDKW.RABSTAM (
                    RAB000 CHAR(3) DEFAULT ' ' NOT NULL,
                    RAB010 CHAR(3) DEFAULT ' ' NOT NULL,
                    RAB020 CHAR(1) DEFAULT ' ' NOT NULL,
                    RAB030 CHAR(10) DEFAULT ' ' NOT NULL,
                    RAB040 CHAR(7) DEFAULT ' ' NOT NULL,
                    RAB050 CHAR(30) DEFAULT ' ' NOT NULL,
                    RAB060 DECIMAL(3,0) DEFAULT 0 NOT NULL,
                    RAB070 CHAR(1) DEFAULT ' ' NOT NULL
                );
                CREATE UNIQUE INDEX RABSTAM ON HDLDKW.RABSTAM (RAB000,RAB010,RAB040);
    '''

    S18='''The data defination language of the database file name AUFSTAM is 
                CREATE TABLE HDLDKW.AUFSTAM (
                    AUF010 CHAR(4) DEFAULT ' ' NOT NULL,
                    AUF020 CHAR(40) DEFAULT ' ' NOT NULL,
                    AUF030 CHAR(5) DEFAULT ' ' NOT NULL,
                    AUF040 CHAR(1) DEFAULT ' ' NOT NULL,
                    AUF050 CHAR(1) DEFAULT ' ' NOT NULL,
                    AUF060 CHAR(8) DEFAULT ' ' NOT NULL,
                    AUF070 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                    AUF080 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                    AUF090 CHAR(8) DEFAULT ' ' NOT NULL,
                    AUF100 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                    AUF110 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                    AUF120 CHAR(2) DEFAULT ' ' NOT NULL,
                    AUF130 DECIMAL(9,2) DEFAULT 0 NOT NULL,
                    AUF140 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF150 CHAR(3) DEFAULT ' ' NOT NULL,
                    AUF160 CHAR(4) DEFAULT ' ' NOT NULL,
                    AUF170 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF180 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF190 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF200 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF210 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF220 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF230 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF240 CHAR(5) DEFAULT ' ' NOT NULL,
                    AUF250 CHAR(5) DEFAULT ' ' NOT NULL,
                    AUF260 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF270 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF280 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF290 CHAR(8) DEFAULT ' ' NOT NULL,
                    AUF300 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF310 CHAR(6) DEFAULT ' ' NOT NULL,
                    AUF320 CHAR(1) DEFAULT ' ' NOT NULL
                );
                CREATE UNIQUE INDEX AUFSTAM ON HDLDKW.AUFSTAM (AUF010);
    '''

    S19='''The data defination language of the database file name HSKUIPF is 
                    CREATE TABLE HDLZENTRAL.HSKUIPF (
                        KUI000 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI010 CHAR(6) DEFAULT ' ' NOT NULL,
                        KUI020 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI030 CHAR(6) DEFAULT ' ' NOT NULL,
                        KUI040 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI050 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI060 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI070 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI080 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI090 CHAR(2) DEFAULT ' ' NOT NULL,
                        KUI100 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI110 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI120 CHAR(20) DEFAULT ' ' NOT NULL,
                        KUI130 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI140 CHAR(2) DEFAULT ' ' NOT NULL,
                        KUI150 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI160 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI170 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI180 CHAR(10) DEFAULT ' ' NOT NULL,
                        KUI190 CHAR(10) DEFAULT ' ' NOT NULL,
                        KUI200 CHAR(10) DEFAULT ' ' NOT NULL,
                        KUI210 CHAR(10) DEFAULT ' ' NOT NULL,
                        KUI220 CHAR(2) DEFAULT ' ' NOT NULL,
                        KUI230 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI240 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI250 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI260 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI270 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI271 CHAR(1) DEFAULT ' ' NOT NULL,
                        KUI272 CHAR(3) DEFAULT ' ' NOT NULL,
                        KUI273 CHAR(5) DEFAULT ' ' NOT NULL,
                        KUI274 CHAR(8) DEFAULT ' ' NOT NULL,
                        KUI275 CHAR(10) DEFAULT ' ' NOT NULL,
                        KUI276 CHAR(30) DEFAULT ' ' NOT NULL,
                        KUI277 DECIMAL(11,2) DEFAULT 0 NOT NULL,
                        KUI278 DECIMAL(11,2) DEFAULT 0 NOT NULL,
                        KUI279 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        KUI280 DECIMAL(5,0) DEFAULT 0 NOT NULL,
                        KUI290 CHAR(4) DEFAULT ' ' NOT NULL,
                        KUI300 CHAR(4) DEFAULT ' ' NOT NULL
                    );
                    CREATE INDEX HSKUILF1 ON HDLZENTRAL.HSKUIPF (KUI020,KUI030);
                    CREATE INDEX HSKUILF2 ON HDLZENTRAL.HSKUIPF (KUI020,KUI030,KUI000);
                    CREATE INDEX HSKUILF3 ON HDLZENTRAL.HSKUIPF (KUI000,KUI010);
                    CREATE INDEX HSKUILF4 ON HDLZENTRAL.HSKUIPF (KUI273,KUI020,KUI030);
                    CREATE INDEX HSKUILF5 ON HDLZENTRAL.HSKUIPF (KUI130,KUI010);
                    CREATE UNIQUE INDEX HSKUIPF ON HDLZENTRAL.HSKUIPF (KUI000,KUI010);
    '''

    S20='''The data defination language of the database file name HSRAZPF is 
            CREATE TABLE HDLZENTRAL.HSRAZPF (
                RAZ000 CHAR(3) DEFAULT ' ' NOT NULL,
                RAZ010 CHAR(3) DEFAULT ' ' NOT NULL,
                RAZ020 CHAR(1) DEFAULT ' ' NOT NULL,
                RAZ030 CHAR(2) DEFAULT ' ' NOT NULL,
                RAZ040 DECIMAL(5,2) DEFAULT 0 NOT NULL
            );
            CREATE UNIQUE INDEX HSRAZPF ON HDLZENTRAL.HSRAZPF (RAZ000,RAZ010,RAZ020,RAZ030);
    '''



    S26='''The data defination language of the database file name HSPSTPF is 
                    CREATE TABLE HDLDKM.HSPSTPF (
                        PST000 CHAR(3) DEFAULT ' ' NOT NULL,
                        PST010 CHAR(6) DEFAULT ' ' NOT NULL,
                        PST020 CHAR(1) DEFAULT ' ' NOT NULL,
                        PST030 CHAR(14) DEFAULT ' ' NOT NULL,
                        PST040 DECIMAL(7,2) DEFAULT 0 NOT NULL,
                        PST050 CHAR(1) DEFAULT ' ' NOT NULL,
                        PST060 CHAR(3) DEFAULT ' ' NOT NULL,
                        PST070 CHAR(7) DEFAULT ' ' NOT NULL,
                        PST071 CHAR(1) DEFAULT ' ' NOT NULL,
                        PST072 CHAR(2) DEFAULT ' ' NOT NULL,
                        PST073 CHAR(2) DEFAULT ' ' NOT NULL,
                        PST079 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        PST080 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        PST081 DECIMAL(5,0) DEFAULT 0 NOT NULL,
                        PST082 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        PST083 DECIMAL(5,0) DEFAULT 0 NOT NULL,
                        PST084 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        PST085 DECIMAL(5,0) DEFAULT 0 NOT NULL,
                        PST086 DECIMAL(5,2) DEFAULT 0 NOT NULL,
                        PST090 CHAR(8) DEFAULT ' ' NOT NULL,
                        PST100 CHAR(8) DEFAULT ' ' NOT NULL,
                        PST107 CHAR(50) DEFAULT ' ' NOT NULL,
                        PST108 CHAR(50) DEFAULT ' ' NOT NULL,
                        PST110 CHAR(10) DEFAULT ' ' NOT NULL,
                        PST120 CHAR(10) DEFAULT ' ' NOT NULL,
                        PST130 CHAR(8) DEFAULT ' ' NOT NULL,
                        PST140 CHAR(6) DEFAULT ' ' NOT NULL,
                        PST150 CHAR(10) DEFAULT ' ' NOT NULL,
                        PST160 CHAR(10) DEFAULT ' ' NOT NULL,
                        PST170 CHAR(8) DEFAULT ' ' NOT NULL,
                        PST180 CHAR(6) DEFAULT ' ' NOT NULL,
                        PST190 CHAR(1) DEFAULT ' ' NOT NULL
                    );
                    CREATE INDEX HSPSTLF1 ON HDLDKM.HSPSTPF (PST000,PST010,PST020,PST030,PST190,PST090,PST100);
                    CREATE INDEX HSPSTLF2 ON HDLDKM.HSPSTPF (PST000,PST010,PST060,PST070,PST190,PST090,PST100);
                    CREATE INDEX HSPSTLF3 ON HDLDKM.HSPSTPF (PST000,PST020,PST030,PST060,PST070,PST090);
                    CREATE INDEX HSPSTLF4 ON HDLDKM.HSPSTPF (PST000,PST090,PST100,PST060,PST010,PST020,PST030,PST060,PST070);
                    CREATE INDEX HSPSTLF5 ON HDLDKM.HSPSTPF (PST000,PST060,PST070,PST090,PST100);
                    CREATE INDEX HSPSTLF6 ON HDLDKM.HSPSTPF (PST000,PST060,PST071,PST072,PST010,PST090,PST100,PST190);
                    CREATE INDEX HSPSTLF7 ON HDLDKM.HSPSTPF (PST000,PST060,PST071,PST072,PST073,PST010,PST090,PST100,PST190);
                    CREATE INDEX HSPSTLF8 ON HDLDKM.HSPSTPF (PST000,PST020,PST030,PST010,PST090,PST100,PST190);
                    CREATE INDEX HSPSTPF ON HDLDKM.HSPSTPF (PST000,PST010,PST020,PST030,PST060,PST070,PST090,PST100);
    '''



    Schema=[S7,S8,S16,S17,S18,S19,S20,S26]

    model = SentenceTransformer("flax-sentence-embeddings/st-codesearch-distilroberta-base")

    code_emb = model.encode(Schema, convert_to_tensor=True)

    for file_name in file:
        query = file_name
        query_emb = model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_emb, code_emb)[0]
        top_hit = hits[0]
        print("Cossim: {:.2f}".format(top_hit['score']))
        
        if(top_hit['score'] > 0.34):
            business_logic = business_logic +'\n'+ f"{Schema[top_hit['corpus_id']]}"

    return business_logic

business = updated_business_logic(business_logic)
print(business)



