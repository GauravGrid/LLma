import os
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.output_parsers import StructuredOutputParser,ResponseSchema


load_dotenv()
ChatAnthropic.api_key=os.getenv("ANTHROPIC_API_KEY")

class LLM(BaseModel):
    role: str
    message: str


# java to python --java

def code_to_business_logic(code,role):    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg"]:
        return "Invalid role specified."

    with open('prompt_code_to_business_logic.txt', 'r') as file:
        examples = file.read().split('\n\n')
        
    example_code = ""
    for example in examples:
        if role.lower() in example.lower():
            example_code = example.split(':')[1].strip()
            break
    
    
    template='''Pretend like a {role} code expert and give full code logic of the User given {role} code so convert {role} Code to Business Logic.
    I want only business logic from {role} code and remember don't give initial words and sentence like this here is buinsess logic extracted 
    from this code and i want only buiness logic and your task also is to analyze the code, identify its core functionality, and express this functionality in a
    clear and concise manner. Please ensure that the extracted business logic is well-documented.This is a multi-step process. 
    Please follow these steps:
        1. Analyze the provided {role} code and understand its purpose.
        2. Identify and abstract the key algorithmic steps and logic used in the {role} code.
        3. Represent this logic in a high-level, language-agnostic format.
    Ensure that the output is a clear and concise representation of the business logic from the {role} code. If the {role} code is 
    complex, please provide comments or explanations to clarify the logic.I am providing an example how to generate business logic 
    using the {role} code as shown in the following example.
    
    Example:
    {example_code}
    
    Don't give any iniial words and sentence except business logic.
    Now the User will provide {role} code, please generate correct buisness logic as shown in above example.
    
    User: {input}
    Business_Logic:'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","role","example_code"], template=template),
        verbose=True,
    )
    logic= llm_chain.predict(input=code,role=role,example_code=example_code)
    return f"{logic}"

def business_logic_to_mermaid_diagram(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg"]:
        return "Invalid role specified."

    with open('prompt_business_logic_to_mermaid_diagram.txt', 'r') as file:
        examples = file.read().split('\n\n')
        
    example_code = ""
    for example in examples:
        if role.lower() in example.lower():
            example_code = example.split(':')[1].strip()
            break

    var="" 
    if(role.lower()=="java"):
        var = "Python"    
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
        llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","var"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_diagram= llm_chain.predict(input=logic,example_code=example_code,var=var)
    return f"{mermaid_diagram}"

def business_logic_to_mermaid_flowchart(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg"]:
        return "Invalid role specified."

    with open('prompt_business_logic_to_mermaid_flowchart.txt', 'r') as file:
        examples = file.read().split('\n\n')
        
    example_code = ""
    for example in examples:
        if role.lower() in example.lower():
            example_code = example.split(':')[1].strip()
            break
    
    var="" 
    if(role.lower()=="java"):
        var = "Python"    
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
        llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","example_code","var"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_flowchart= llm_chain.predict(input=logic,example_code=example_code,var=var)
    return f"{mermaid_flowchart}"

def business_logic_to_code(logic,role):
    
    if role.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg"]:
        return "Invalid role specified."

    with open('prompt_business_logic_to_code.txt', 'r') as file:
        examples = file.read().split('\n\n')
        
    example_code = ""
    for example in examples:
        if role.lower() in example.lower():
            example_code = example.split(':')[1].strip()
            break
     
    var="" 
    if(role.lower()=="java"):
        var = "Python"    
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
    
    java_code_schema = ResponseSchema(name='java_code',description='This is the java code generated compatible with latest java version converted to a correct json string without java backticks with new line replaced with \\n.')
    java_code_description_schema = ResponseSchema(name='java_code_description',description='This is the description of the java code generated')

    response_schema = (java_code_schema,java_code_description_schema)
    parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = parser.get_format_instructions()
    print(format_instructions)    
           
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
    example without any initial text. Also include proper comments in the code. Don't give any initial words and sentence except 
    {var} code.
    
    User: {input}
    {var} Code:
    {format_instructions}'''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","var","example_code","role"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )

    code= llm_chain.predict(input=logic,var=var,example_code=example_code,role=role)
    return f"{code}"  

async def process(res: LLM):
    role = res.role
    code = res.message

    logic=code_to_business_logic(code,role)
    diagram=business_logic_to_mermaid_diagram(logic,role)
    flow_chart=business_logic_to_mermaid_flowchart(logic,role)
    code= business_logic_to_code(logic,role)
    return {"Business_logic":logic,"Mermaid_Diagram":diagram,"Mermaid_Flowchart":flow_chart,"Code":code}





















































