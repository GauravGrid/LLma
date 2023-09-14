from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.output_parsers import GuardrailsOutputParser
import json
import os
from dotenv import load_dotenv
import keys
import openai
from .L2J import java_prompt_new
from .L2MFlow import mermaid_FlowchartPrompt_new
from .L2CDiagram import mermaid_class_diagram_prompt_new
from .javaCompiler import compile_and_execute_java
from .business_logic_prompt import business_prompt
from .mermaid_dia_prompt import mermaid_prompt
from .logic_java_prompt import java_prompt
from .mermaid_Flowchart import mermaid_FlowchartPrompt
from .critiqueModel import Critique
import re 
from .worker import add_code_submission

from langchain.output_parsers import PydanticOutputParser,StructuredOutputParser,ResponseSchema
from typing import List
load_dotenv()

# Access the OpenAI API key
#api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = keys.openai_key
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        #print(f'Spent a total of {cb.total_tokens} tokens')
    return result



def mermaid_dig(business_logic):
      # prompt = f'''
      #   {mermaid_prompt}
      #   User:{business_logic}
      #   mermaid code:
      #   '''

      

      rail_spec = """
        <rail version="0.1">

        <output>
            <string name="mermaidClassDiagram" description = "Contains the code for the Mermaid Class diagram generated from the logic"/>
        </output>
        
        <prompt>

        {{mermaid_prompt}}
        User:{{business_logic}}
        Mermaid code:
        @complete_json_suffix_v2
        </prompt>
        </rail>
      """

      
      # template = """
      # {mermaid_prompt}
      # User:{business_logic}
      # Mermaid code:
      # """

      # prompt = PromptTemplate(
      #   input_variables=["mermaid_prompt","business_logic"], template=template
      # )

      output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)

      prompt = PromptTemplate(
          template=output_parser.guard.base_prompt,
          input_variables=["mermaid_prompt","business_logic"]
      )


      # llm = OpenAI(
      #    temperature=0,
      #    max_tokens=5000,
      #   n=1 )
      # mermaid_code  = llm(prompt)

      mermaid_code = LLMChain(
        llm = ChatAnthropic(temperature= 0.7 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
        prompt = prompt,
        verbose = True
      )
      # dataform = str(mermaid_code.predict(mermaid_prompt = mermaid_prompt, business_logic = business_logic)).strip("'<>() ").replace('\'', '\"')
      result = (mermaid_code.predict(mermaid_prompt = mermaid_prompt, business_logic = business_logic))
      print("result",result)
      match = re.search(r'{[\s\S]*}', result)
      # match = re.search(r'\{[^{}]*\}', result,re.DOTALL)
      try:
        if match:
          substring = match.group(0)
          print(substring)
          return (json.loads(substring)['mermaidClassDiagram'])
      except Exception as e :
        return str(e)

  
      



def business_logic(rpg_code):
      
  # prompt = f'''
  #   {business_prompt}
  #   User2:{rpg_code}
  #   Logic2:
  #   '''
  
  template = """
    {business_prompt}
    User:{rpg_code}
    Logic:
  """

  prompt = PromptTemplate(
    input_variables=["business_prompt","rpg_code"], template=template
  )

  # llm = OpenAI(
  #    temperature=0,
  #    max_tokens=3000,
  #   n=1 )
  
  # llm_fe = ChatAnthropic(
  #   temperature=0.1, 
  #   anthropic_api_key=keys.anthropic_key,
  #   model='claude-1.3-100k',
  #   max_tokens_to_sample=1000  
  # )   
  # business_logic  = llm_fe(prompt)


  business_logic = LLMChain(
    llm = ChatAnthropic(temperature= 0.7 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )
  return business_logic.predict(business_prompt = business_prompt, rpg_code = rpg_code)
       


def convert_rpg_to_java(rpg_code):
     prompt = 'Translate the following RPG code to Java.java code should follow Object-oriented programming format, with proper comments and import related packages and main fuction should be always included:\n\n' + rpg_code + '\n\nJava code:'
    
     llm = OpenAI(
         temperature=0,
         max_tokens=1000,
          n=1 )
     java_code = llm(prompt)
     return java_code




def mermaid_flowchart(business_logic):

  rail_spec = """
  <rail version="0.1">

  <output>
     <string name = "mermaidFlowchart" description = "Contains the code for the Mermaid Flow Chart generated from the logic"/>
  </output>
  
  <prompt>
  {{mermaid_FlowchartPrompt}}
  User:{{business_logic}}
  Mermaid Flowchart code:
  @complete_json_suffix_v2
  </prompt>
  </rail>
  """


  output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)

  

  prompt = PromptTemplate(
      template=output_parser.guard.base_prompt,
      input_variables=["mermaid_FlowchartPrompt","business_logic"]
  )
  # prompt = PromptTemplate(
  #   input_variables=["mermaid_FlowchartPrompt","business_logic"], template=template
  # )

  Flowchart_code = LLMChain(
        llm = ChatAnthropic(temperature= 0.7 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
        prompt = prompt,
        verbose = True
      )
  result = (Flowchart_code.predict(mermaid_FlowchartPrompt = mermaid_FlowchartPrompt, business_logic = business_logic))
  print(result)
  # match = re.search(r'{.*?}', result,re.DOTALL)
  match = re.search(r'{[\s\S]*}', result)
  try:
      if match:
        substring = match.group(0)
        print(substring)
        return (json.loads(substring)['mermaidFlowchart'])
  except Exception as e :
      return str(e)
       
      
  # llm = OpenAI(
  #   temperature=0,
  #   max_tokens=5000,
  # n=1 )
  # Flowchart_code  = llm(prompt)

   


def logic_to_java(business_logic):
  rail_spec = """
    <rail version="0.1">

    <output >
      <string format = "one-line" on_fail = "re-ask" name = "javaCode" description = "Contains the java Code generated from the logic"/>
    </output>
    
    <prompt>
    {{java_prompt}}
    User:{{business_logic}}
    Java code:
    @complete_json_suffix_v2
    </prompt>
    </rail>
    """
  
  output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)

  prompt = PromptTemplate(
      template=output_parser.guard.base_prompt,
      input_variables=["java_prompt","business_logic"]
  )

  java_code = LLMChain(
    llm = ChatAnthropic(temperature= 0.4 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )

  try:
     result = java_code.predict(java_prompt=java_prompt,business_logic=business_logic)
     print('1')
     print(result)
     match = re.search(r'{[\s\S]*}', result)
     if match:
        substring = match.group(0)
        print('2')
        print(substring)
        print('3')
        print(json.loads(substring)['javaCode'])
        return (json.loads(substring)['javaCode'])
  except Exception as e:
     print(Critique(substring,str(e)))
     print(str(e))
     return str(e)


def generateJava(businessLogic): 

  java_code_schema = ResponseSchema(name='java_code',description='This is the java code generated compatible with latest java version converted to a correct json string without java backticks with new line replaced with \\n.')
  java_code_description_schema = ResponseSchema(name='java_code_description',description='This is the description of the java code generated')

  response_schema = (java_code_schema,java_code_description_schema)
  parser = StructuredOutputParser.from_response_schemas(response_schema)
  format_instructions = parser.get_format_instructions()
  print(format_instructions)
  # parser = PydanticOutputParser(pydantic_object=GeneratedJavaCode)

  prompt = PromptTemplate(
      template="""
      {java_prompt}
      User: {businessLogic}
      Code: 
      {format_instructions}
      """,
      input_variables=["java_prompt","businessLogic"],
      partial_variables={"format_instructions":format_instructions},
  )
  java_code = LLMChain(
    llm = ChatAnthropic(temperature= 0.4 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )
  try:
    result = java_code.predict(java_prompt=java_prompt_new,businessLogic=businessLogic)
    print(result)
    code = parser.parse(result)
    return code['java_code']
  except Exception as e:
     print(e)
     return 'Error Generating Java Code'


def generateFlowChart(businessLogic): 

  flowchart_schema = ResponseSchema(name='mermaid_flowchart_code',description='This is the mermaid flowchart code with properly linked nodes which can be rendered by mermaidjs 8.11.0. , converted to a correct json string with new line replaced with \\n. Also all the nodes should contain strings so that any special characters do not cause problems')
  flowchart_description_schema = ResponseSchema(name='flowchart_code_description',description='This is the description of the flowchart code generated')

  response_schema = (flowchart_schema,flowchart_description_schema)
  parser = StructuredOutputParser.from_response_schemas(response_schema)
  format_instructions = parser.get_format_instructions()
  print(format_instructions)
  # parser = PydanticOutputParser(pydantic_object=GeneratedJavaCode)

  prompt = PromptTemplate(
      template="""
      {mermaid_FlowchartPrompt}
      User: {businessLogic}
      Code: 
      {format_instructions}
      """,
      input_variables=["mermaid_FlowchartPrompt","businessLogic"],
      partial_variables={"format_instructions":format_instructions},
  )
  flowchart_code = LLMChain(
    llm = ChatAnthropic(temperature= 0.4 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )
  result = flowchart_code.predict(mermaid_FlowchartPrompt=mermaid_FlowchartPrompt_new,businessLogic=businessLogic)
  code = parser.parse(result)
  print(code)
  return code['mermaid_flowchart_code']

# text="Here is the logic for the provided RPG code:\nThe program is invoked by the DATEADJ command. It allows adding/subtracting days, months or years from a date with specified input and output formats.\nIt declares constants for controlling debug mode and activation group behavior. This ensures a new job date is picked up in an interactive session.\nIt copies message members and declares an external program to retrieve job and system date formats. \nThe Main procedure defines the input and output parameters for date, adjustment, formats etc. \nIt moves input values to work fields and handles special format values like *JOB, *SYSTEM.\nIt converts the input date string to a date using the CvtInDate procedure. This supports various formats like *YMD, *MDY, *ISO etc. \nIt adds/subtracts the adjustment based on the adj type (days, months, years). \nIt converts the calculated date back to a string using the toOutDate procedure. This supports the same formats as input.\nIt handles errors for invalid input date or incompatible output format.\nIn summary, it provides a flexible way to adjust a date by a specified amount and convert between multiple formats. The procedures standardize date handling. It uses proper error handling and activation group control."
# generateFlowChart(businessLogic=text)

def generateClassDiagram(businessLogic): 

  classDiagram_schema = ResponseSchema(name='mermaid_class_diagram_code',description='This is the mermaid class diagram code which can be rendered by mermaidjs 8.11.0. , converted to a correct json string with new line replaced with \\n.')
  classDiagram_description_schema = ResponseSchema(name='mermaid_class_diagram_code_description',description='This is the description of the class diagram code generated')

  response_schema = (classDiagram_schema,classDiagram_description_schema)
  parser = StructuredOutputParser.from_response_schemas(response_schema)
  format_instructions = parser.get_format_instructions()
  print(format_instructions)
  # parser = PydanticOutputParser(pydantic_object=GeneratedJavaCode)

  prompt = PromptTemplate(
      template="""
      {mermaid_class_diagram_prompt}
      User: {businessLogic}
      Code: 
      {format_instructions}
      """,
      input_variables=["mermaid_class_diagram_prompt","businessLogic"],
      partial_variables={"format_instructions":format_instructions},
  )
  flowchart_code = LLMChain(
    llm = ChatAnthropic(temperature= 0.4 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )
  try:
    result = flowchart_code.predict(mermaid_class_diagram_prompt=mermaid_class_diagram_prompt_new,businessLogic=businessLogic)
    print(result)
    code = parser.parse(result)
    print(code)
    print(code['mermaid_class_diagram_code'])
    return code['mermaid_class_diagram_code']
  except Exception as e:
    print(e)
    return 'graph TD\n  A[Error generating Class Diagram]'
  

def detectLanguage(code): 

  prompt = PromptTemplate(
      template="""
      You are building a code converter tool that identifies the language
      of the following code given by user not give explanations only give named among them Python,SQL,Java,RPG,Mongodb,Angular,React
      Example:
        User:
          class _DoublyLinkedList:
            class _Node:
                __slots__  = ("_element", "_previous", "_next")

                def __init__(self, element, previous, next_):
                    self._element = element
                    self._previous = previous
                    self._next = next_
                def __init__(self):
                    self._header = self._Node(None, None, None)
                    self._trailer = self._Node(None, None, None)
                    self._header._next = self._trailer
                    self._trailer._previous = self._header
                    self._size = 0
                def __len__(self):
                    return self._size
                def is_empty(self):
                    return self._size == 0
                def _insert_between(self, element, predecessor, sucessor):
                    newest = self._Node(element, predecessor, sucessor)
                    predecessor._next = newest
                    sucessor._previous = newest
                def _delete_node(self, node):
                    predecessor = node._previous
                    sucessor = node._next
                    predecessor._next = sucessor
                    sucessor._previous = predecessor
                    self._size -= 1
                    element = node._element
                    node._previous = node._next = node._element = None
                    return element
          Languages: Python
          
          User: {code}
          Languages:
        
      """,
      input_variables=["code"],
  )
  language = LLMChain(
    llm = ChatAnthropic(temperature= 0.4 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
    prompt = prompt,
    verbose = True
  )
  try:
    result = language.predict(code=code)
    return f"{result}"
  except Exception as e:
    print(e)
    return 'Error Identifying Code'


def javaCompiler():
  java_code1 = """
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DateAdjuster {

    // Constants for controlling debug mode and activation group
    private static final boolean DEBUG = false;
    private static final boolean NEWJOB = true;
    
    // Copied message members    
    private static final String MSG1 = "Invalid date format";
    private static final String MSG2 = "Incompatible output format";
    
    // External program to retrieve job and system date formats
    private static String getJobFormat() {
        return "MM/dd/yyyy"; 
    }
    
    private static String getSystemFormat() {
        return "yyyy-MM-dd";
    }
    
    public static void main(String[] args) throws ParseException {
        
        // Input parameters        
        String inDate = args[0]; 
        int adjDays = Integer.parseInt(args[1]);
        String inFormat = args[2];
        String outFormat = args[3];
        
        // Work fields
        Date date;
        SimpleDateFormat inFormatter;
        SimpleDateFormat outFormatter;
        
        // Handle special input formats        
        if (inFormat.equals("*JOB")) {
            inFormat = getJobFormat();
        } else if (inFormat.equals("*SYSTEM")) {
            inFormat = getSystemFormat();
        }
        
        // Convert input date to Date object
        inFormatter = new SimpleDateFormat(inFormat);
        date = inFormatter.parse(inDate);
        
        // Adjust date
        if (adjDays != 0) {
            date.setDate(date.getDate() + adjDays);
        }
        
        // Handle special output formats
        if (outFormat.equals("*JOB")) {
            outFormat = getJobFormat();
        } else if (outFormat.equals("*SYSTEM")) {
            outFormat = getSystemFormat();
        }
        
        // Validate compatible output format 
        if (!outFormat.contains("y") && outFormat.contains("M")) {
            throw new RuntimeException(MSG2);
        }
        
        // Convert Date back to String
        outFormatter = new SimpleDateFormat(outFormat);
        String outDate = outFormatter.format(date);
        
        // Print output
        System.out.println(outDate);
        
    }

}
  """

  java_code2 = """
  public class HelloWorld2 {
      public static void main(String[] args) {
          System.out.println("Hello, World from HelloWorld2!");
      }
  }
  """

  add_code_submission(java_code1)
  # compile_and_execute_java(java_code2)