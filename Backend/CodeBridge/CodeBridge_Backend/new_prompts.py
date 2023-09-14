import os
from pydantic import BaseModel
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4
import keys


# ChatAnthropic.api_key=keys.anthropic_key

class LLM(BaseModel):
    role: str
    message: str


# java to python --java

def code_to_business_logic(code,role):    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas"]:
        return "Invalid role specified."
    
    example_code="" 
    if(role.lower()=="java"):
        example_code=java_example1   
    elif(role.lower()=="python"):
       example_code=python_example1
    elif(role.lower()=="sql"):
        example_code=sql_example1
    elif(role.lower()=="mongodb"):
        example_code=mongodb_example1
    elif(role.lower()=="angular"):
        example_code=angular_example1
    elif(role.lower()=="react"):
        example_code=react_example1
    elif(role.lower()=="rpg"):
        example_code=rpg_example1
    elif(role.lower()=="sas"):
        example_code=sas_example1
    
    template='''Pretend to be an expert in {role} code and provide a comprehensive explanation of the user-provided {role} code, converting it into
    understandable business logic. If the variables in the code have values relevant to the business logic, please include them.I am interested 
    solely in the business logic and do not require introductory statements such as 'Here is the business logic extracted from this code.'
    Your task also involves analyzing the code, identifying its core functionality, and presenting this functionality clearly and concisely. 
    Ensure that the extracted business logic is well-documented.
    This process involves multiple steps:
    1.Analyze the provided {role} code to comprehend its purpose.
    2.Identify and abstract the key algorithmic steps and logic used in the {role} code.
    3.Express this logic in a high-level, language-agnostic format.
    Make sure that the output provides a clear and concise representation of the business logic within the {role} code. If the {role} code is complex,
    please include comments or explanations to clarify the logic.I am providing an example how to generate business logic 
    using the {role} code as shown in the following example.
    
    Example:
    {example_code}
    
    Don't give any iniial words and sentence except business logic.
    Now the User will provide {role} code, please generate correct buisness logic as shown in above example.
    
    User: {input}
    Business_Logic:'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","role","example_code"], template=template),
        verbose=True,
    )
    logic= llm_chain.predict(input=code,role=role,example_code=example_code)
    return f"{logic}"

def business_logic_to_mermaid_diagram(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas"]:
        return "Invalid role specified."

    example_code="" 
    if(role.lower()=="java"):
        example_code=java_example2   
    elif(role.lower()=="python"):
       example_code=python_example2
    elif(role.lower()=="sql"):
        example_code=sql_example2
    elif(role.lower()=="mongodb"):
        example_code=mongodb_example2
    elif(role.lower()=="angular"):
        example_code=angular_example2
    elif(role.lower()=="react"):
        example_code=react_example2
    elif(role.lower()=="rpg"):
        example_code=rpg_example2
    elif(role.lower()=="sas"):
        example_code=sas_example2

    var="" 
    if(role.lower()=="java"):
        var == "Python"    
    elif(role.lower()=="python"):
        var="Java"
    elif(role.lower()=="sql"):
        var="Mongodb"
    elif(role.lower()=="mongodb"):
        var="SQL"
    elif(role.lower()=="angular"):
        var="React"
    elif(role.lower()=="react"):
        var="Angular"
    elif(role.lower()=="rpg"):
        var="Java"
    elif(role.lower()=="sas"):
        var="Python"
    
    classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code',description='This is the mermaid class diagram code which can be rendered by mermaidjs 8.11.0. , converted to a correct json string with new line replaced with \\n.')
    classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description',description='This is the description of the class diagram code generated')

    response_schema = (classDiagram_schema,classDiagram_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    print(format_instructions)
    
    template='''
    I want to generate code with backtick for Mermaid Class diagram using business logic. Remember in future
    anyone can convert this mermaid class diagram code to {var} code easily so give answer in context of that. Also give code 
    in correct syntax so that it can be rendered by mermaidjs 8.11.0. . I am providing an example how to generate mermaid 
    class diagram using the business logic shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic, please generate correct and running code for mermaid class diagram as shown in above 
    example without any initial text in a JSON format with "mermaidClassDiagram" as the key.
    
    User: {input}
    Mermaid_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","var"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_diagram= llm_chain.predict(input=logic,example_code=example_code,var=var)
    result=parser.parse(mermaid_diagram)
    return result['mermaid_class_diagram_code']

def business_logic_to_mermaid_flowchart(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas"]:
        return "Invalid role specified."

    example_code="" 
    if(role.lower()=="java"):
        example_code=java_example3   
    elif(role.lower()=="python"):
       example_code=python_example3
    elif(role.lower()=="sql"):
        example_code=sql_example3
    elif(role.lower()=="mongodb"):
        example_code=mongodb_example3
    elif(role.lower()=="angular"):
        example_code=angular_example3
    elif(role.lower()=="react"):
        example_code=react_example3
    elif(role.lower()=="rpg"):
        example_code=rpg_example3
    elif(role.lower()=="sas"):
        example_code=sas_example3
    
    var="" 
    if(role.lower()=="java"):
        var == "Python"    
    elif(role.lower()=="python"):
        var="Java"
    elif(role.lower()=="sql"):
        var="Mongodb"
    elif(role.lower()=="mongodb"):
        var="SQL"
    elif(role.lower()=="angular"):
        var="React"
    elif(role.lower()=="react"):
        var="Angular"
    elif(role.lower()=="rpg"):
        var="Java"
    elif(role.lower()=="sas"):
        var="Python"
        
    flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. ,converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
    flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

    response_schema = (flowchart_schema,flowchart_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    print(format_instructions) 
    
    template='''
    Convert Business Logic to Mermaid Flow chart Diagram
    I want to generate code for Mermaid Flow chart diagram using business logic and Remember in future anyone can convert 
    this mermaid class diagram code to {var} code easily so give answer in context of that. Also give code in correct syntax
    so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked . Here is also an example how
    to generate mermaid class diagram using the business logic. and remember also don't give any inital word and sentence 
    like here is mermaid flow chart diagram of this business logic.Mermaid flow chart diagram that visually represents this
    logic.The Mermaid flow chart diagram also should visually represent the flow and sequence of the business logic,
    including key decision points and data dependencies. Ensure that the resulting diagram is comprehensive and 
    self-explanatory. Follow these steps:
        1. Review the provided business logic.
        2. Identify key components, decisions, and flow control in the logic.
        3. Create a Mermaid flow chart diagram that illustrates the flow of logic, including decisions, loops, and data flow.
        4. Ensure the Mermaid flow chartdiagram is clear, well-structured, and accurately represents the business logic.
    I am providing an example how to generate mermaid flow chart diagram using the business logic as shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic,generate correct and running code for mermaid Flowchart diagram as shown in 
    above example without any initial text in a JSON format with "mermaidFlowchart" as the key and make sure that the 
    blocks areproperly linked in the code.
    
    User: {input}
    Mermaid_Flowchart_Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","var"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_flowchart= llm_chain.predict(input=logic,example_code=example_code,var=var)
    result=parser.parse(mermaid_flowchart)
    return result['mermaid_flowchart_code']

def business_logic_to_code(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas"]:
        return "Invalid role specified."

    example_code="" 
    if(role.lower()=="java"):
        example_code=java_example4   
    elif(role.lower()=="python"):
       example_code=python_example4
    elif(role.lower()=="sql"):
        example_code=sql_example4
    elif(role.lower()=="mongodb"):
        example_code=mongodb_example4
    elif(role.lower()=="angular"):
        example_code=angular_example4
    elif(role.lower()=="react"):
        example_code=react_example4
    elif(role.lower()=="rpg"):
        example_code=rpg_example4
    elif(role.lower()=="sas"):
        example_code=sas_example4
     
    var="" 
    if(role.lower()=="java"):
        var == "Python"    
    elif(role.lower()=="python"):
        var="Java"
    elif(role.lower()=="sql"):
        var="Mongodb"
    elif(role.lower()=="mongodb"):
        var="SQL"
    elif(role.lower()=="angular"):
        var="React"
    elif(role.lower()=="react"):
        var="Angular"
    elif(role.lower()=="rpg"):
        var="Java"
    elif(role.lower()=="sas"):
        var="Python"
    
    code_schema = ResponseSchema(name='code',description=f'This is the {var} code generated compatible with latest java version converted to a correct json string without {var} backticks with new line replaced with \\n.')
    code_description_schema = ResponseSchema(name='code_description',description=f'This is the description of the {var} code generated')

    response_schema = (code_schema, code_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
    template='''
    Convert Business logic to {var} Code:
    I want to generate a {var} code from a Business Logic of {role} code which is given in plain text and I don't want any initial 
    words and sentence like here is {var} code from business logic of {role} code. The {var} code should faithfully implement the same 
    logic as depicted in the Business logic.Ensure that the generated {var} code is syntactically correct and adheres to best 
    coding practices.Ensure that the resulting code is comprehensive and self-explanatory.Follow these steps:
        1. Review the provided business logic.
        2. Identify key components, decisions, and flow control in the logic.
        3. Translate the Business logic into clear and functional {var} code.

    Please ensure that the generated {var} code is well-commented and adheres to best practices for readability and functionality.
    I am providing an example how to generate {var} code using the business logic of {role} code as shown in the following example.

    Example:
    {example_code}
    
    Now the User will provide business logic , please generate correct {var} code for business logic as shown in above 
    example without any initial text. Also include proper comments in the code. 
    
    User: {input}
    Code:

    {format_instructions}
    ''',
      input_variables=["input","var","example_code","role"],
      partial_variables={"format_instructions":format_instructions},
    )
    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
        prompt = prompt,
        verbose = True
    )
    
    code= llm_chain.predict(input=logic,var=var,example_code=example_code,role=role)
    try:
        print(code)
        result = parser.parse(code)
        print(result)
        return result['code']
    except:
        return 'Error Parsing Output'  























































