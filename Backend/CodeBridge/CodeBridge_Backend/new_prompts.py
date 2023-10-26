import os
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from .prompt_code_to_business_logic import java_example1,python_example1,sql_example1,mongodb_example1,react_example1,angular_example1,rpg_example1,sas_example1, dspf_exampler1,dspf_examplea1
from .prompt_business_logic_to_mermaid_diagram import java_example2,python_example2,sql_example2,mongodb_example2,react_example2,angular_example2,rpg_example2,sas_example2, dspf_exampler2,dspf_examplea2
from .prompt_business_logic_to_mermaid_flowchart import java_example3,python_example3,sql_example3,mongodb_example3,react_example3,angular_example3,rpg_example3,sas_example3, dspf_exampler3,dspf_examplea3
from .prompt_business_logic_to_code import java_example4,python_example4,sql_example4,mongodb_example4,react_example4,angular_example4,rpg_example4,sas_example4, dspf_exampler4,dspf_examplea4
import keys

load_dotenv()
ChatAnthropic.api_key=os.getenv("ANTHROPIC_API_KEY")
ChatAnthropic.api_key=keys.anthropic_key

class LLM(BaseModel):
    source: str
    message: str

extensions = ['.rpgle', '.sqlrpgle', '.clle', '.RPGLE', '.SQLRPGLE', '.CLLE','.py','.java','.jsx','.tsx','.js','.ts','.sql','.PY','.JAVA','.JSX','.TSX','.JS','.TS','.SQL','.sas','.SAS']

# java to python --java

def code_to_business_logic(code,source):    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa"]:
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
        example_code=rpg_example1
    elif(source.lower()=="sas"):
        example_code=sas_example1
    elif(source.lower()=="dspfr"):
        example_code=dspf_exampler1
    elif(source.lower()=="dspfa"):
        example_code=dspf_examplea1
    
    template='''Task: Extract Comprehensive Business Logic for {destination} Code Conversion

    In this task, your goal is to thoroughly analyze the provided {source} code and extract the complete business logic contained within it. The
    objective is to create a clear, detailed, and high-level representation of the business logic that can be easily transformed into {destination} code. 
    This process involves several essential steps:

    Step 1: Understanding the Source Code
    - Begin by deeply analyzing the {source} code to comprehend its functionality, purpose, and structure.
    - Pay attention to variables, functions, and any data structures used within the code.

    Step 2: Identifying Variables and Functions
    - Identify and list all variables and functions within the code. This includes not only their names but also their data types and any initial 
    values they might have.
    - Distinguish between global and local variables.
    - Note any data dependencies between variables or functions.

    Step 3: Explaining Function Logic
    - For each function found in the code, provide a detailed explanation of its purpose and the logic it implements.
    - Specify the parameter types for each function and describe the significance of these parameters within the function's operation.
    - If a function returns a value, explain the meaning of the returned value and how it relates to the overall business logic.

    Step 4: Expressing the Logic
    - Present the extracted logic in a high-level, language-agnostic format that captures the essence of the business processes.
    - Emphasize the sequential flow of operations, conditional statements, loops, and any exceptional cases.
    - Ensure that the logic is abstracted enough to allow for straightforward translation into {destination} code.

    Step 5: Handling Complexity
    - If the code is particularly intricate or includes complex algorithms, provide comments, explanations, or visual representations that break 
    down the logic into more manageable components.
    - Make any additional notes to clarify the logic, especially for sections that might be challenging to understand.

    The ultimate goal is to deliver a comprehensive and understandable representation of the business logic within the {source} code, making it
    easier for it to be translated into {destination} language. The extracted logic should be designed to minimize the gap between
    the {source} code and the eventual {destination} code, ensuring accuracy and efficiency.

    Please note that you should not provide any initial words or sentences apart from the business logic.I am providing an example how to generate 
    business logic using the {source} code as shown in the following example.
    
    Example:
    {example_code}
    
    Don't give any iniial words and sentence except business logic.
    Now the User will provide {source} code, please generate correct buisness logic as shown in above example.

    User: {input}
    Business_Logic:
    '''

    llm_chain = LLMChain(
        llm = ChatAnthropic(temperature= 0.8,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=100000),
        prompt=PromptTemplate(input_variables=["input","source","example_code","destination"], template=template),
        verbose=True,
    )
    logic= llm_chain.predict(input=code,source=source,example_code=example_code,destination="Java")
    return f"{logic}"

def business_logic_to_mermaid_diagram(logic,source, destination):
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa"]:
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
    
    Now the User will provide business logic, please generate correct and running code for mermaid class diagram as shown in above 
    example without any initial text in a JSON format with "mermaidClassDiagram" as the key.
    
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
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa"]:
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
        prompt=PromptTemplate(input_variables=["input","example_code","destination"],partial_variables={"format_instructions":format_instructions}, template=template),
        verbose=True,
    )
    
    mermaid_flowchart= llm_chain.predict(input=logic,example_code=example_code,destination=destination)
    result=parser.parse(mermaid_flowchart)
    return result['mermaid_flowchart_code']

def business_logic_to_code(logic,source, destination):
    
    if source.lower() not in ["sql", "python", "java","mongodb","react","angular","rpg","sas","dspfr","dspfa"]:
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






















































