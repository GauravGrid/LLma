from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from . import keys
from langchain.output_parsers import GuardrailsOutputParser



def Critique(response,error):
    rail_spec = """
    <rail version="0.1">

    <output>
        <string name="JavaCritiqueCode" description = "Revisises the json string according to the error"/>
    </output>
    
    <prompt>
    Assistant : {{response}}

    ----------------------------------
    Steps to follow for acting as a critic :
    1. Criticize the following java code json string response : 
    json string : {{response}}
    I get the following error {{error}} when I convert the jsonstring into a JSON object.
    2. Let's think about the problems with the response step by step
    3. After evaluating the steps. Re-generate the response and improve it based on your critic and steps evaluation.
    4. Return the revised json string response with the necessary changes.

    Critic : 
    @complete_json_suffix_v2
    </prompt>
    </rail>
    """
    
    output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)

    prompt = PromptTemplate(
        template=output_parser.guard.base_prompt,
        input_variables=["response","error"]
    )

    critique_response = LLMChain(
        llm = ChatAnthropic(temperature = 0 , anthropic_api_key=keys.anthropic_key, model = "claude-2.0",max_tokens_to_sample=100000),
        prompt = prompt,
        verbose = True
    )

    return critique_response.predict(response = response, error = error)

