import os
from pydantic import BaseModel
from langchain.chat_models import ChatAnthropic,ChatOpenAI
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1, dspf_exampler1,dspf_examplea1,assembly_example1
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2, dspf_exampler2,dspf_examplea2,assembly_example2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3, dspf_exampler3,dspf_examplea3,assembly_example3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4, dspf_exampler4,dspf_examplea4,assembly_example4
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1, dspf_exampler1,dspf_examplea1,rpg_example11,rpg_example12
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2, dspf_exampler2,dspf_examplea2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3, dspf_exampler3,dspf_examplea3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4, dspf_exampler4,dspf_examplea4
import keys
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate





# ChatAnthropic.api_key=keys.anthropic_key

class LLM(BaseModel):
    source: str
    message: str

extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE','.py','.java','.jsx','.tsx','.js','.ts','.sql','.PY','.JAVA','.JSX','.TSX','.JS','.TS','.SQL','.sas','.SAS']

from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from sentence_transformers import SentenceTransformer, util


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
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key = keys.anthropic_key, model = "claude-2.0", max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["business_logic"],partial_variables={"format_instructions":parser.get_format_instructions()}, template=template),
        verbose=True,
    )
    schema_str= llm_chain.predict(business_logic=business_logic)
    
    start_index = schema_str.find('"file": [') + len('"file": [')
    end_index = schema_str.find(']')
    files = [file.strip(' "\n') for file in schema_str[start_index:end_index].split(',')]
    print(files)
    
    dblist=['HSHI12PF', 'RABSTAR', 'AUFSTAR', 'HSKUIPR', 'HSRAZPR','AUFSTAM','RABSTAM','ERLSTAM',"ESZPF",'HSESZPF','TEISTAM','HSPMSL1','HSATBPF','HSPSTLF7','HSBTSLF1','BELSTAM','NUMSTAM']
    
    new_files=[]
    for file_name in files:
        if(file_name in dblist):
            new_files.append(file_name)
    
    return new_files

def updated_business_logic(business_logic):
    
    file=get_file_name(business_logic)
    print(file)
    
    # S1='The Schema of the database file name PMS is PMS'
    # S2='The Schema of the database file name ATB is ATB'
    # S3='The Schema of the database file name PST is PST'
    # S4='The Schema of the database file name RAZ is RAZ'
    # S5='The Schema of the database file name TEI is TEI'
    # S6='The Schema of the database file name ESZPF is ESZPF'

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

    # S9='The Schema of the database file name HSKUKPF is HSKUKPF'
    # S10='The Schema of the database file name HSFZKPF is HSFZKPF'
    # S11='The Schema of the database file name HS0017S1 is HS0017S1'
    # S12='The Schema of the database file name HS0017S2 is HS0017S2'
    # S13='The Schema of the database file name KUDSTAR is KUDSTAR'
    # S14='The Schema of the database file name FARSTAR is FARSTAR'
    # S15='The Schema of the database file name RWADMPF is RWADMPF'

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

    # S21='The Schema of the database file name HSHI12S1 is HSHI12S1'
    # S22='The Schema of the database file name HSHI12S2 is HSHI12S2'
    # S23='The Schema of the database file name HSHI12S3 is HSHI12S3'
    # S24='The Schema of the database file name HSHI12S4 is HSHI12S4'
    # S25='The Schema of the database file name HSBTSLF1 is HSBTSLF1'

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

    S27='''The data defination language of the database file name TEISTAM is 
            -- HDLDKW.TEISTAM definition

-- Drop table

-- DROP TABLE HDLDKW.TEISTAM;

CREATE TABLE HDLDKW.TEISTAM (
	TEI010 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI020 CHAR(14) DEFAULT ' ' NOT NULL,
	TEI030 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI035 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI040 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI050 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI060 CHAR(22) DEFAULT ' ' NOT NULL,
	TEI070 DECIMAL(5,0) DEFAULT 0 NOT NULL,
	TEI080 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI090 CHAR(6) DEFAULT ' ' NOT NULL,
	TEI095 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI100 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI110 CHAR(4) DEFAULT ' ' NOT NULL,
	TEI120 CHAR(3) DEFAULT ' ' NOT NULL,
	TEI130 CHAR(6) DEFAULT ' ' NOT NULL,
	TEI135 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI140 CHAR(14) DEFAULT ' ' NOT NULL,
	TEI150 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI160 CHAR(12) DEFAULT ' ' NOT NULL,
	TEI170 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI180 DECIMAL(3,0) DEFAULT 0 NOT NULL,
	TEI185 DECIMAL(3,0) DEFAULT 0 NOT NULL,
	TEI190 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI195 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI200 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI205 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI210 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	TEI220 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI230 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI240 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI250 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI260 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI270 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI275 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI280 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI290 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI300 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI310 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI320 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI330 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI340 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI350 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI360 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI370 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI380 CHAR(6) DEFAULT ' ' NOT NULL,
	TEI390 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI400 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI410 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI420 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI430 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI440 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI450 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI460 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI470 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI480 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI490 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI500 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI510 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI520 CHAR(9) DEFAULT ' ' NOT NULL,
	TEI530 CHAR(8) DEFAULT ' ' NOT NULL,
	TEI540 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI550 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI560 CHAR(6) DEFAULT ' ' NOT NULL,
	TEI570 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI580 CHAR(6) DEFAULT ' ' NOT NULL,
	TEI590 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI600 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI610 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI620 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI630 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI640 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI650 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI660 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI670 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI680 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI690 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI700 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI710 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI720 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	TEI800 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI810 CHAR(18) DEFAULT ' ' NOT NULL,
	TEI820 CHAR(5) DEFAULT ' ' NOT NULL,
	TEI830 CHAR(4) DEFAULT ' ' NOT NULL,
	TEI840 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI850 CHAR(3) DEFAULT ' ' NOT NULL,
	TEI860 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI870 DECIMAL(7,3) DEFAULT 0 NOT NULL,
	TEI880 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI890 CHAR(11) DEFAULT ' ' NOT NULL,
	TEI900 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI910 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI920 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI930 CHAR(2) DEFAULT ' ' NOT NULL,
	TEI940 CHAR(3) DEFAULT ' ' NOT NULL,
	TEI950 CHAR(1) DEFAULT ' ' NOT NULL,
	TEI960 CHAR(4) DEFAULT ' ' NOT NULL
);
CREATE UNIQUE INDEX TEISTAM ON HDLDKW.TEISTAM (TEI010,TEI020);
CREATE INDEX TEISTLF1 ON HDLDKW.TEISTAM (TEI010,TEI020);
CREATE INDEX TEISTLF2 ON HDLDKW.TEISTAM (TEI090,TEI010,TEI020);
CREATE INDEX TEISTLF3 ON HDLDKW.TEISTAM (TEI010,TEI020);
CREATE INDEX TEISTLF4 ON HDLDKW.TEISTAM (TEI060,TEI010,TEI020);
CREATE INDEX TEISTLF5 ON HDLDKW.TEISTAM (TEI520);
CREATE INDEX TEISTLF6 ON HDLDKW.TEISTAM (TEI020,TEI010);
CREATE INDEX TEISTLF8 ON HDLDKW.TEISTAM (TEI090,TEI120,TEI010,TEI020);
CREATE INDEX TEISTLFPW ON HDLDKW.TEISTAM (TEI090,TEI010,TEI020);
    '''
    S28='''The data defination language of the database file name HSPMSL1 is 
            -- HDLZENTRAL.HSPMSL1 definition

-- Drop table

-- DROP TABLE HDLZENTRAL.HSPMSL1;

CREATE TABLE HDLZENTRAL.HSPMSL1 (
	PMS_LAND CHAR(3) NOT NULL,
	PMS_CDC CHAR(2) NOT NULL,
	PMS_OTP CHAR(2) NOT NULL,
	PMS_FRAN CHAR(2) NOT NULL,
	PMS_PART CHAR(18) NOT NULL,
	PMS_FCODE CHAR(1) NOT NULL,
	PMS_DCPRT CHAR(1) NOT NULL,
	PMS_DESC CHAR(15) NOT NULL,
	PMS_DESC2 CHAR(15) NOT NULL,
	PMS_PARTM CHAR(18) NOT NULL,
	PMS_RET1 DECIMAL(11,2) NOT NULL,
	PMS_FPGRP CHAR(5) NOT NULL,
	PMS_PAG CHAR(4) NOT NULL,
	PMS_ARTGP CHAR(2) NOT NULL,
	PMS_DIS CHAR(3) NOT NULL,
	PMS_DISA CHAR(3) NOT NULL,
	PMS_FPRCD CHAR(2) NOT NULL,
	PMS_SUPP CHAR(10) NOT NULL,
	PMS_WGT DECIMAL(7,3) NOT NULL,
	PMS_PACK DECIMAL(5,0) NOT NULL,
	PMS_COR CHAR(2) NOT NULL,
	PMS_DTYC CHAR(11) NOT NULL,
	PMS_COCCD CHAR(1) NOT NULL,
	PMS_DSMC CHAR(1) NOT NULL,
	PMS_ASGRP CHAR(2) NOT NULL,
	PMS_NFRN CHAR(2) NOT NULL,
	PMS_NPRT CHAR(18) NOT NULL,
	PMS_NFKZ CHAR(1) NOT NULL,
	PMS_NTNR CHAR(14) NOT NULL,
	PMS_DRAT DECIMAL(5,2) NOT NULL,
	PMS_PPRCN DECIMAL(7,2) NOT NULL,
	PMS_FKZ CHAR(1) NOT NULL,
	PMS_TNR CHAR(14) NOT NULL,
	PMS_EC CHAR(2) NOT NULL,
	PMS_AT CHAR(1) NOT NULL,
	PMS_PRD CHAR(2) NOT NULL,
	PMS_NDAT CHAR(8) NOT NULL,
	PMS_NUHR CHAR(6) NOT NULL,
	PMS_ADAT CHAR(8) NOT NULL,
	PMS_AUHR CHAR(6) NOT NULL
);
    '''
    S29='''The data defination language of the database file name HSATBPF is 
            -- HDLDKW.HSATBPF definition

-- Drop table

-- DROP TABLE HDLDKW.HSATBPF;

CREATE TABLE HDLDKW.HSATBPF (
	ATB010 CHAR(5) DEFAULT ' ' NOT NULL,
	ATB020 CHAR(14) DEFAULT ' ' NOT NULL,
	ATB030 DECIMAL(5,0) DEFAULT 0 NOT NULL,
	ATB040 CHAR(1) DEFAULT ' ' NOT NULL,
	ATB050 CHAR(1) DEFAULT ' ' NOT NULL,
	ATB060 CHAR(8) DEFAULT ' ' NOT NULL
);
CREATE UNIQUE INDEX HSATBPF ON HDLDKW.HSATBPF (ATB010,ATB020);
    '''
    S30='''The data defination language of the database file name HSPSTLF7 is 
            -- HDLDKW.HSPSTLF7 definition

-- Drop table

-- DROP TABLE HDLDKW.HSPSTLF7;

CREATE TABLE HDLDKW.HSPSTLF7 (
	PST000 CHAR(3) NOT NULL,
	PST010 CHAR(6) NOT NULL,
	PST020 CHAR(1) NOT NULL,
	PST030 CHAR(14) NOT NULL,
	PST040 DECIMAL(7,2) NOT NULL,
	PST050 CHAR(1) NOT NULL,
	PST060 CHAR(3) NOT NULL,
	PST070 CHAR(7) NOT NULL,
	PST071 CHAR(1) NOT NULL,
	PST072 CHAR(2) NOT NULL,
	PST073 CHAR(2) NOT NULL,
	PST079 DECIMAL(5,2) NOT NULL,
	PST080 DECIMAL(5,2) NOT NULL,
	PST081 DECIMAL(5,0) NOT NULL,
	PST082 DECIMAL(5,2) NOT NULL,
	PST083 DECIMAL(5,0) NOT NULL,
	PST084 DECIMAL(5,2) NOT NULL,
	PST085 DECIMAL(5,0) NOT NULL,
	PST086 DECIMAL(5,2) NOT NULL,
	PST090 CHAR(8) NOT NULL,
	PST100 CHAR(8) NOT NULL,
	PST107 CHAR(50) NOT NULL,
	PST108 CHAR(50) NOT NULL,
	PST110 CHAR(10) NOT NULL,
	PST120 CHAR(10) NOT NULL,
	PST130 CHAR(8) NOT NULL,
	PST140 CHAR(6) NOT NULL,
	PST150 CHAR(10) NOT NULL,
	PST160 CHAR(10) NOT NULL,
	PST170 CHAR(8) NOT NULL,
	PST180 CHAR(6) NOT NULL,
	PST190 CHAR(1) NOT NULL
);
    '''
    S31='''The data defination language of the database file name HSBTSLF1 is 
            -- HDLZENTRAL.HSBTSLF1 definition

-- Drop table

-- DROP TABLE HDLZENTRAL.HSBTSLF1;

CREATE TABLE HDLZENTRAL.HSBTSLF1 (
	BTS010 CHAR(3) NOT NULL,
	BTS020 CHAR(3) NOT NULL,
	BTS030 DECIMAL(3,0) NOT NULL,
	BTS040 CHAR(30) NOT NULL,
	BTS050 CHAR(10) NOT NULL,
	BTS060 CHAR(10) NOT NULL
);
    '''
    S32='''The data defination language of the database file name BELSTAM is 
            -- HDLDKW.BELSTAM definition

-- Drop table

-- DROP TABLE HDLDKW.BELSTAM;

CREATE TABLE HDLDKW.BELSTAM (
	BEL010 CHAR(6) DEFAULT ' ' NOT NULL,
	BEL020 CHAR(40) DEFAULT ' ' NOT NULL,
	BEL030 CHAR(2) DEFAULT ' ' NOT NULL,
	BEL040 CHAR(1) DEFAULT ' ' NOT NULL,
	BEL050 CHAR(3) DEFAULT ' ' NOT NULL,
	BEL060 CHAR(1) DEFAULT ' ' NOT NULL,
	BEL070 CHAR(8) DEFAULT ' ' NOT NULL,
	BEL080 DECIMAL(7,2) DEFAULT 0 NOT NULL,
	BEL090 CHAR(10) DEFAULT ' ' NOT NULL,
	BEL100 CHAR(2) DEFAULT ' ' NOT NULL,
	BEL110 CHAR(1) DEFAULT ' ' NOT NULL
);
CREATE UNIQUE INDEX BELSTAM ON HDLDKW.BELSTAM (BEL010);
    '''
    S33='''The data defination language of the database file name NUMSTAM is 
            -- HDLDKW.NUMSTAM definition

-- Drop table

-- DROP TABLE HDLDKW.NUMSTAM;

CREATE TABLE HDLDKW.NUMSTAM (
	NUM010 CHAR(2) DEFAULT ' ' NOT NULL,
	NUM020 DECIMAL(7,0) DEFAULT 0 NOT NULL,
	NUM030 CHAR(1) DEFAULT ' ' NOT NULL,
	NUM040 CHAR(8) DEFAULT ' ' NOT NULL,
	NUM050 DECIMAL(9,0) DEFAULT 0 NOT NULL
);
CREATE UNIQUE INDEX NUMSTAM ON HDLDKW.NUMSTAM (NUM010);
    '''

    Schema=[S7,S8,S16,S17,S18,S19,S20,S26,S27,S28,S29,S30,S31,S32,S33]

    model = SentenceTransformer("flax-sentence-embeddings/st-codesearch-distilroberta-base")

    code_emb = model.encode(Schema, convert_to_tensor=True)

    for file_name in file:
        query = file_name
        query_emb = model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_emb, code_emb)[0]
        # print(hits,"<-----hits")
        top_hit = hits[0]
        # print(top_hit,"file---->",file_name)
        print("Cossim: {:.2f}".format(top_hit['score']))
        
        if(top_hit['score'] > 0.34):
            business_logic = business_logic +'\n'+ f"{Schema[top_hit['corpus_id']]}"
            # print(business_logic)
        
        # else( file_name == 'HSESZPF' ):
        #     business_logic= business_logic +'\n'+ f"{Schema[top_hit['corpus_id']]}"
        #     print(business_logic)
        # print("\n\n")

    return business_logic

# java to python --java

def code_to_business_logic(code,source):    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
        return "Invalid source specified."
    
    example_code="" 
    if(source.lower()=="java"):
        example_code=java_example1   
    elif(source.lower()=="python"):
       example_code=python_example1
    elif(source.lower()=="sql"):
        example_code=sql_example1
    elif(source.lower()=="mongodb"):
        example_code=mongodb_example1
    elif(source.lower()=="angular"):
        example_code=angular_example1
    elif(source.lower()=="react"):
        example_code=react_example1
    elif(source.lower()=="rpg"):
        example_code=rpg_example11
    elif(source.lower()=="sas"):
        example_code=sas_example1
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler1
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea1
    elif(source.lower()=="assembly"):
        example_code=assembly_example1

    


    
    # step_back_prompt ='''
    # You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. 
    # Here are a few examples:
    # Example 1:
    # user : Could the members of The Police perform lawful arrests?    
    # ai : what can the members of The Police do?
    # Example 2: 
    # user : Jan Sindel's was born in what country?
    # ai : what is Jan Sindel's personal history?
    
    # # New question
    # user : Pretend to be an expert in {source} code and provide a comprehensive explanation of the user-provided {source} code, converting it into
    # understandable business logic. If the variables in the code have values relevant to the business logic, please include them.I am interested 
    # solely in the business logic and do not require introductory statements such as 'Here is the business logic extracted from this code.'
    # Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality clearly and concisely. 
    # Ensure that the extracted business logic is well-documented.
    # This process involves multiple steps:
    # 1.Analyze the provided {source} code to comprehend its purpose.
    # 2.Identify and abstract the key functional logic of the {source} code.
    # 3.Express this logic in a high-level, language-agnostic format.
    # 4.Identify the type of code and if there is any database, other files or ui interaction.
    # 5.Any important information about the file structure should be identified and added to the interactions. 
    # 6.Please specify these interactions towards the end of the generated response in a well formatted manner.
    # 7.Be as verbose as needed.
    # Make sure that the output provides a clear and concise representation of the business logic within the {source} code. If the {source} code is complex,
    # please include comments or explanations to clarify the logic.I am providing an example how to generate business logic 
    # using the {source} code as shown in the following example.
    
    # Example:
    # {example_code}
    
    # Now the User will provide {source} code, please generate correct buisness logic as shown in above example.
    # Share business logic and related files like database , ui and other files as part of the response.
    # user: {input}
    # Business_Logic:
    # ai :
    # '''
    
    # question = f'''
    # Pretend to be an expert in {source} code and provide a comprehensive explanation of the user-provided {source} code, converting it into
    # understandable business logic. If the variables in the code have values relevant to the business logic, please include them.I am interested 
    # solely in the business logic and do not require introductory statements such as 'Here is the business logic extracted from this code.'
    # Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality clearly and concisely. 
    # Ensure that the extracted business logic is well-documented.
    # This process involves multiple steps:
    # 1.Analyze the provided {source} code to comprehend its purpose.
    # 2.Identify and abstract the key algorithmic steps and logic used in the {source} code.
    # 3.Express this logic in a high-level, language-agnostic format.
    # 4.Identify the type of code and if there is any database, other files or ui interaction.
    # 5.Any important information about the file structure should be identified and added to the interactions. 
    # 6.Please specify these interactions towards the end of the generated response in a well formatted manner.
    # 7.Be as verbose as needed.
    # Make sure that the output provides a clear and concise representation of the business logic within the {source} code. If the {source} code is complex,
    # please include comments or explanations to clarify the logic.

    
    # '''

    # step_back_chain = LLMChain(
    #     llm = ChatAnthropic(temperature= 0,anthropic_api_key=keys.anthropic_key,model = "claude-2.0"),
    #     prompt=PromptTemplate(input_variables=["input,source,example_code,"], template=step_back_prompt),
    #     verbose=True,
    # )
    # step_back_question = step_back_chain.predict(input=code,source=source,example_code=example_code)
    # print(step_back_question)

    template='''
    Pretend to be an expert in {source} code and provide a comprehensive explanation of the user-provided {source} code, converting it into
    understandable business logic. If the variables in the code have values relevant to the business logic, please include them.I am interested 
    solely in the business logic and do not require introductory statements such as 'Here is the business logic extracted from this code.'
    Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality clearly and concisely. 
    Ensure that the extracted business logic is well-documented.
    This process involves multiple steps:
    1.Analyze the provided {source} code to comprehend its purpose.
    2.Identify and abstract the key functional logic of the {source} code.
    3.Express this logic in a high-level, language-agnostic format.
    4.Identify the type of code and if there is any database, other files or ui interaction.
    5.Any important information about the file structure should be identified and added to the interactions. 
    6.Please specify these interactions towards the end of the generated response in a well formatted manner.
    7.Be as verbose as needed.
    Make sure that the output provides a clear and concise representation of the business logic within the {source} code. If the {source} code is complex,
    please include comments or explanations to clarify the logic.I am providing an example how to generate business logic 
    using the {source} code as shown in the following example.
    
    Example:
    {example_code}
    
    Now the User will provide {source} code, please generate correct buisness logic as shown in above example.
    Share business logic and related files like database , ui and other files as part of the response.

    Take a deep breath and think step by step to solve this task.

    user: {input}
    Business_Logic:
    '''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","source","example_code"], template=template),
        verbose=True,
    )
    logic= llm_chain.predict(input=code,source=source,example_code=example_code)
    return f"{logic}"

def business_logic_to_mermaid_diagram(logic,source, destination):
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
        return "Invalid source specified."

    example_code="" 
    if(source.lower()=="java"):
        example_code=java_example2   
    elif(source.lower()=="python"):
       example_code=python_example2
    elif(source.lower()=="sql"):
        example_code=sql_example2
    elif(source.lower()=="mongodb"):
        example_code=mongodb_example2
    elif(source.lower()=="angular"):
        example_code=angular_example2
    elif(source.lower()=="react"):
        example_code=react_example2
    elif(source.lower()=="rpg"):
        example_code=rpg_example2
    elif(source.lower()=="sas"):
        example_code=sas_example2
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler2
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea2
    elif(source.lower()=="assembly"):
        example_code=assembly_example2

    
    classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code', description='This schema represents the Mermaid class diagram code, which is compatible with MermaidJS version 8.11.0. The code should be represented as a valid JSON string with new lines replaced with "\\n".')
    classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description', description='This schema represents the description of the class diagram code generated by MermaidJS.')

    response_schema = (classDiagram_schema,classDiagram_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    print(format_instructions)
    
    template='''
    I want to generate code with backtick for Mermaid Class diagram using business logic. Remember in future
    anyone can convert this mermaid class diagram code to {destination} code easily so give answer in context of that. Also give code 
    in correct syntax so that it can be rendered by mermaidjs 8.11.0. . I am providing an example how to generate mermaid 
    class diagram using the business logic shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic as well as associated files, please generate correct and running code for mermaid class diagram as shown in above 
    example without any initial text in a JSON format with "mermaid_class_diagram_code" as the key.
    
    User: {input}
    Mermaid_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","destination"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_diagram= llm_chain.predict(input=logic,example_code=example_code,destination=destination)
    result=parser.parse(mermaid_diagram)
    return result['mermaid_class_diagram_code']

def business_logic_to_mermaid_flowchart(logic,source, destination):
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
        return "Invalid source specified."

    example_code="" 
    if(source.lower()=="java"):
        example_code=java_example3   
    elif(source.lower()=="python"):
       example_code=python_example3
    elif(source.lower()=="sql"):
        example_code=sql_example3
    elif(source.lower()=="mongodb"):
        example_code=mongodb_example3
    elif(source.lower()=="angular"):
        example_code=angular_example3
    elif(source.lower()=="react"):
        example_code=react_example3
    elif(source.lower()=="rpg"):
        example_code=rpg_example3
    elif(source.lower()=="sas"):
        example_code=sas_example3
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler3
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea3
    elif(source.lower()=="assembly"):
        example_code=assembly_example3
    

        
    flowchart_schema = ResponseSchema(name='mermaid_flowchart_code', description='This schema represents the Mermaid flowchart code, designed to generate properly linked nodes that can be rendered by MermaidJS version 8.11.0. The code must be formatted as a valid JSON string, with newline characters replaced by "\\n". All nodes within the code should contain strings to ensure compatibility and avoid issues with special characters.')
    flowchart_description_schema = ResponseSchema(name='flowchart_code_description', description='This schema provides a description of the flowchart code generated by MermaidJS. It includes details about the structure and relationships of the nodes within the flowchart, as well as any additional information relevant to understanding the flowchart.')

    response_schema = (flowchart_schema,flowchart_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    print(format_instructions) 
    
    template='''
    Convert Business Logic to Mermaid Flow chart Diagram
    I want to generate code for Mermaid Flow chart diagram using business logic and Remember in future anyone can convert 
    this mermaid class diagram code to {destination} code easily so give answer in context of that. Also give code in correct syntax
    so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked . Here is also an example how
    to generate mermaid class diagram using the business logic. and remember also don't give any inital word and sentence 
    like here is mermaid flow chart diagram of this business logic.Mermaid flow chart diagram that visually represents this
    logic.The Mermaid flow chart diagram also should visually represent the flow and sequence of the business logic,
    including key decision points and data dependencies. Ensure that the resulting diagram is comprehensive and 
    self-explanatory. Follow these steps:
        1. Review the provided business logic.
        2. Identify key components, decisions, and flow control in the logic.
        3. Create a Mermaid flow chart diagram that illustrates the flow of logic, including decisions, loops, and data flow.
        4. Ensure that the files , databases and other UI elements which might be present are properly shown.
        5. Ensure the Mermaid flow chartdiagram is clear, well-structured, and accurately represents the business logic.
    I am providing an example how to generate mermaid flow chart diagram using the business logic as shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic,generate correct and running code for mermaid Flowchart diagram as shown in 
    above example without any initial text in a JSON format with "mermaid_flowchart_code" as the key and make sure that the 
    blocks areproperly linked in the code.
    
    User: {input}
    Mermaid_Flowchart_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","destination"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_flowchart= llm_chain.predict(input=logic,example_code=example_code,destination=destination)
    result=parser.parse(mermaid_flowchart)
    return result['mermaid_flowchart_code']

def business_logic_to_code(logic,source, destination,srccode):
    
    logic = updated_business_logic(logic)
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa","assembly"]:
        return "Invalid source specified."

    example_code="" 
    if(source.lower()=="java"):
        example_code=java_example4   
    elif(source.lower()=="python"):
       example_code=python_example4
    elif(source.lower()=="sql"):
        example_code=sql_example4
    elif(source.lower()=="mongodb"):
        example_code=mongodb_example4
    elif(source.lower()=="angular"):
        example_code=angular_example4
    elif(source.lower()=="react"):
        example_code=react_example4
    elif(source.lower()=="rpg"):
        example_code=rpg_example4
    elif(source.lower()=="sas"):
        example_code=sas_example4
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler4
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea4
    elif(source.lower()=="assembly"):
        example_code=assembly_example4
     
    
    code_schema = ResponseSchema(name='code',description=f'This is the {destination} code generated compatible with latest java version converted to a correct json string without {destination} backticks with new line replaced with \\n.')
    code_description_schema = ResponseSchema(name='code_description',description=f'This is the description of the {destination} code generated')

    response_schema = (code_schema, code_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    template='''
    Convert Business logic to {destination} Code:
    I want to generate a {destination} code from a Business Logic of {source} code which is given in plain text and I don't want any initial 
    words and sentence like here is {destination} code from business logic of {source} code. The {destination} code should faithfully implement the same 
    logic as depicted in the Business logic.Ensure that the generated {destination} code is syntactically correct and adheres to best 
    coding practices.Ensure that the resulting code is comprehensive and self-explanatory.Follow these steps:
        1. Review the provided business logic.
        2. Identify key components, decisions, and flow control in the logic.
        3. Translate the Business logic into clear and functional {destination} code.
        4. Make sure that the function refered to in the generated code exists or create it in full.
        5. Create unit tests for every function created.
        6. Assume any files that we interact with are database tables.
        7. Make smart assumptions of the file structure in order to output more complete code.
        8. Do not return any TODOs and actually write code based on assumptions.
        9. Return all the methods created in a comment.
        10. Use the provided data defination language(DDL) of the database files to understand how the code will interact with the database.
    
    Please ensure that the generated {destination} code is well-commented and adheres to best practices for readability and functionality.
    I am providing an example how to generate {destination} code using the business logic of {source} code as shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic , please generate correct {destination} code for business logic as shown in above 
    example without any initial text. Also include proper comments in the code. 
    
    User: {input}
    Code:

    {format_instructions}
    ''',
      input_variables=["input","destination","example_code","source"],
      partial_variables={"format_instructions":format_instructions},
    )
    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
        prompt = prompt,
        verbose = True
    )
    
    code= llm_chain.predict(input=logic,destination=destination,example_code=example_code,source=source)
    try:
        print(code)
        result = parser.parse(code)
        print(result)
        return result['code']
    except:
        return 'Error Parsing Output'  

















# Higher Level Business Logic

def file_business_logic(file_path):
    with open(file_path, 'rb') as file:
        code = file.read() 
    
    source=""
    logic= code_to_business_logic(code,source)
    return logic

def combine_business_logic(folder_name,
                           folder_structure,
                           previous_business_logic,
                           current_directory_name,
                           current_directory_business_logic):
    
    
    template='''
    I'd like to generate comprehensive business logic documentation for a specific directory named '{folder_name}' with the following 
    folder structure: '{folder_structure}'. 

    To accomplish this, I will aggregate business logic from each directory within this folder one by one. Specifically, I will merge the business 
    logic from selected directories within the folder structure with the business logic from the current directory named '{current_directory_name}' 
    within the same folder structure. This process will result in a combined business logic document, which includes the accumulated logic up to the
    specified directory and the business logic of the current directory. The goal is to create an all-encompassing report that includes any imported
    statements from other files and all significant statements originating from these files. Additionally, this report will list the names of all
    files and folders involved and the business logic report for the specified directory and its subdirectories will also include specific variable
    values relevant to the overall business logic. It will indicate functions imported from other files and specify their sources, maintain consistency
    in variable and function names, and provide function parameter types for each function.

    In cases where the previous file's business logic is empty, it signifies that the current file is the first file, and there is no previous file's
    business logic.
    
    Now give me only Combined Business Logic of  Previous and Current Directory Logic given below: 
    
    Previous Business Logic: {previous_business_logic}
    Current Directory Business Logic: {current_directory_business_logic}
    
    '''

    llm_chain = LLMChain(
        llm=ChatAnthropic(
            temperature=0.8,
            model="claude-2.0",
            max_tokens_to_sample=100000
        ),
        prompt=PromptTemplate(
            input_variables=[
                "folder_name",
                "folder_structure",
                "previous_business_logic",
                "current_directory_name",
                "current_directory_business_logic"
            ],
            template=template
        ),
        verbose=True,
    )

    logic= llm_chain.predict(folder_name=folder_name,
                             folder_structure=folder_structure,
                             previous_business_logic=previous_business_logic,
                             current_directory_name=current_directory_name,
                             current_directory_business_logic=current_directory_business_logic)
    return f"{logic}"

def process_folder_business_logic(folder_path):
    business_logic = ""
    folder_name = os.path.basename(folder_path)
    folder_structure = os.listdir(folder_path)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            Business_logic = process_folder_business_logic(item_path)
        else:
            if item_path.endswith(tuple(extensions)):
                Business_logic = file_business_logic(item_path)
            else:
                continue 
            
        business_logic = combine_business_logic(folder_name, folder_structure, business_logic, item, Business_logic)

    return business_logic

# Higher Level Mermaid Diagram

def file_mermaid_diagram(file_path):
    with open(file_path, 'rb') as file:
        code = file.read() 
        
    source=""
    destination=""    
    logic=code_to_business_logic(code,source)
    mermaid_diagram = business_logic_to_mermaid_diagram(logic,source,destination)
    return mermaid_diagram

def combine_mermaid_diagram(folder_name,
                           folder_structure,
                           previous_mermaid_diagram,
                           current_directory_name,
                           current_directory_mermaid_diagram):
    
    
    classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code',description='This is the mermaid class diagram code which can be rendered by mermaidjs 8.11.0. , converted to a correct json string with new line replaced with \\n.')
    classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description',description='This is the description of the class diagram code generated')

    response_schema = (classDiagram_schema,classDiagram_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    
    template='''
    I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
    To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
    from some directories within the folder structure with the current directory's Mermaid Diagram named 
    '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
    the current directory.Remember, in the future, anyone can convert this Mermaid Class diagram code to another language code easily, so provide the 
    answer in the context of that. Also, give code in the correct syntax so that it can be rendered by MermaidJS 8.11.0. 
    
    Now give me combined Mermaid Diagram of Previous Mermaid Diagram and Curreny Directory Mermaid Diagram given below.
    
    Previous Mermaid Diagram:
     
    {previous_mermaid_diagram}
    
    Current Directory Mermaid Diagram: 
    
    {current_directory_mermaid_diagram}
    
    {format_instructions}

    '''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_diagram",
                                               "current_directory_name","current_directory_mermaid_diagram"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    logic= llm_chain.predict(folder_name=folder_name,
                             folder_structure=folder_structure,
                             previous_mermaid_diagram=previous_mermaid_diagram,
                             current_directory_name=current_directory_name,
                             current_directory_mermaid_diagram=current_directory_mermaid_diagram)
    return f"{logic}"

def process_folder_mermaid_diagram(folder_path):
    mermaid_diagram=""
    folder_name=os.path.basename(folder_path)
    folder_structure=os.listdir(folder_path)
   
    for item in os.listdir(folder_path):   
        item_path = os.path.join(folder_path, item) 
        
        if os.path.isdir(item_path):  
            Mermaid_Diagram = process_folder_mermaid_diagram(item_path) 
        else:
            if item_path.endswith(tuple(extensions)):
                Mermaid_Diagram = file_mermaid_diagram(item_path)
            else:
                continue 
            
        mermaid_diagram= combine_mermaid_diagram(folder_name,folder_structure,mermaid_diagram,
                                                item,Mermaid_Diagram)
    
    return mermaid_diagram

# Higher Level Mermaid Flowchart Diagram
    
def file_mermaid_flowchart(file_path):
    with open(file_path, 'rb') as file:
        code = file.read() 
    
    source=""
    destination=""
    logic=code_to_business_logic(code,source)
    mermaid_flowchart = business_logic_to_mermaid_flowchart(logic,source,destination)
    return mermaid_flowchart
    
def combine_mermaid_flowchart(folder_name,
                           folder_structure,
                           previous_mermaid_flowchart,
                           current_directory_name,
                           current_directory_mermaid_flowchart):
    
    
    flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. ,converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
    flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

    response_schema = (flowchart_schema,flowchart_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()

    
    template='''
    I want to generate the complete Mermaid Diagram for the folder named '{folder_name}'. The folder structure of this folder is '{folder_structure}'.
    To achieve this, I will consolidate the Mermaid Diagram from each directory within it one by one. Specifically, I will merge the Mermaid Diagram
    from directories some within the folder structure with the current directory's Mermaid Diagram named 
    '{current_directory_name}'. This process will result in the combined Mermaid Diagram up to the specified directory and the Mermaid Diagram of 
    the current directory.and the remember in future anyone can convert this mermaid diagram code to business logic easily.Also give code in correct
    syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked .Mermaid flow chart diagram that visually
    represents this logic.Now give me combined Mermaid Flowchart Code using Previous Memaid Flowchart and Current Directory Mermaid Flowchart given below:

    Previous Mermaid Flowchart:
     
    {previous_mermaid_flowchart}
    
    Current Directory Mermaid Flowchart: 
    
    {current_directory_mermaid_flowchart}

    {format_instructions}
    '''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key = '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', model = "claude-2.0", max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["folder_name","folder_structure","previous_mermaid_flowchart",
                                               "current_directory_name","current_directory_mermaid_flowchart"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    mermaid_flowchart= llm_chain.predict(folder_name=folder_name,
                             folder_structure=folder_structure,
                             previous_mermaid_flowchart=previous_mermaid_flowchart,
                             current_directory_name=current_directory_name,
                             current_directory_mermaid_flowchart=current_directory_mermaid_flowchart)
    return f"{mermaid_flowchart}"
             
def process_folder_mermaid_flowchart(folder_path):
    mermaid_flowchart=""
    folder_name=os.path.basename(folder_path)
    folder_structure=os.listdir(folder_path)
    
    for item in os.listdir(folder_path): 
        item_path = os.path.join(folder_path, item) 
        if os.path.isdir(item_path):  
            Mermaid_Flowchart = process_folder_mermaid_flowchart(item_path) 
        else:
            if item_path.endswith(tuple(extensions)):
                Mermaid_Flowchart = file_mermaid_flowchart(item_path) 
            else:
                continue 
            
        mermaid_flowchart= combine_mermaid_flowchart(folder_name,folder_structure,mermaid_flowchart,
                                                item,Mermaid_Flowchart)
    
    return mermaid_flowchart


# Pinecone





















































