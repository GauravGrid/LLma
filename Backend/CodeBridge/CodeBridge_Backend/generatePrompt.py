from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chat_models import ChatAnthropic
from langchain.memory import ConversationBufferWindowMemory
from langchain.output_parsers import GuardrailsOutputParser
import keys

def initialize_chain(instructions, memory=None):

    mermaidCode = """
    classDiagram
        class Families {
            - address: string
            - numPeople: int
            - people: People[]
            + setAddress(address: string)
            + setNumPeople(numPeople: int)
        }

        class People {
            - name: string
            - age: int
            + setName(name: string)
            + setAge(age: int)
        }

        class Main {
            - numFamilies: int
            - i: int
            - j: int
            + main()
        }

        Families --> People
        Main --> Families

        Families "1" o-- "*" People : contains
    """

    template = f"""
    I want to generate code with backtick for Mermaid Class diagram using business logic of rpg code.Remember in future anyone can convert this mermaid class diagram code to java code easily so give answer in context of that. I am providing an example how to generate mermaid class diagram using the business logic
    shown in the following example.
    Example :
        User:
            The following piece of code declares two data structures, families and people, and then sets up a family with two people. The families data structure is qualified, meaning that it is an array of structures, with each element of the array being a structure. The families data structure has three fields: address, numPeople, and people. The address field is a character field of length 50, and is used to store the address of the family. The numPeople field is an unsigned integer field of length 3, and is used to store the number of people in the family. The people field is an array of structures, with each element of the array being a structure. The people data structure has two fields: name and age. The name field is a character field of length 25, and is used to store the name of the person. The age field is a packed decimal field of length 5, and is used to store the age of the person.
            The code then sets up a family with two people. The address of the family is set to '10 Mockingbird Lane', and the two people are named 'Alice' and 'Bill', with ages of 3 and 15 respectively. The number of people in the family is set to 2. The number of families is set to 1.
            The code then uses a for loop to iterate through the families array. For each family, the address is displayed, and then a nested for loop is used to iterate through the people array. For each person, the name and age are displayed.
            Finally, the return statement indicates the end of the program.
        Mermaid code:
            {mermaidCode}

    Now the User will provide business logic, please generate correct and running code for mermaid class diagram as given in above example without any initial text.
    User : {input}
     """


    prompt = PromptTemplate(
        input_variables=["input"], template=template
    )

    chain = LLMChain(
        # llm=OpenAI(temperature=0),
        llm = ChatAnthropic(temperature= 0 ,anthropic_api_key=keys.anthropic_key,model = "claude-2.0",max_tokens_to_sample=1000),
        prompt=prompt,
        verbose=True
    )
    return chain


def initialize_meta_chain():
    meta_template = """
    --------------------------------
    Assistant has just had the below interactions with a Human. Assistant followed their "Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.

    ####

    {chat_history}

    ####

    Please reflect on these interactions.

    You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".

    You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
    """

    meta_prompt = PromptTemplate(
        input_variables=["chat_history"], template=meta_template
    )

    meta_chain = LLMChain(
        llm=ChatAnthropic(temperature= 0 , model = "claude-2.0",max_tokens_to_sample=1000),
        prompt=meta_prompt,
        verbose=True,
    )
    return meta_chain


def get_chat_history(chain_memory):
    memory_key = chain_memory.memory_key
    chat_history = chain_memory.load_memory_variables(memory_key)[memory_key]
    return chat_history


def get_new_instructions(meta_output):
    delimiter = "Instructions: "
    new_instructions = meta_output[meta_output.find(delimiter) + len(delimiter) :]
    return new_instructions


def main(logic,max_iters=3, max_meta_iters=5):
    failed_phrase = "fail"
    success_phrase = "success"
    key_phrases = [success_phrase, failed_phrase]

    instructions = "None"
    for i in range(max_meta_iters):
        print(f"[Episode {i+1}/{max_meta_iters}]")
        chain = initialize_chain(instructions,memory=None)
        output = chain.predict(input=logic)
        for j in range(max_iters):
            print("<---------------------->")
            print(f"New Instructions: {instructions}")
            print(f"(Step {j+1}/{max_iters})")
            print(f"Assistant: {output}")
            print(f"Human: ")
            human_input = input()
            if any(phrase in human_input.lower() for phrase in key_phrases):
                break
            output = chain.predict(input=logic)
        if success_phrase in human_input.lower():
            print(f"You succeeded! Thanks for playing!")
            return
        meta_chain = initialize_meta_chain()
        meta_output = meta_chain.predict(chat_history=get_chat_history(chain.memory))
        print(f"Feedback: {meta_output}")
        instructions = get_new_instructions(meta_output)
        print("\n" + "#" * 80 + "\n")
    print(f"You failed! Thanks for playing!")


logic = """Here is the logic for the given RPG code:
This code defines a prototype for the QUSROBJD API, which retrieves object description information. The parameters are:
- receiver: A variable-length character string that will receive the object description. 
- receiverLength: A 10-digit integer that specifies the length of the receiver parameter.
- formatName: An 8-character constant that specifies the format of the object description.
- qualifiedObjectName: A 20-character constant that specifies the qualified name of the object.
- objectType: A 10-character constant that specifies the type of object.
- apiError: A variable-length character string that will receive any error messages.
- aspControl: A variable-length character string for ASP control info.
This prototype defines the call interface for the QUSROBJD API so that an RPG program can call it. The constants specify the format and name of the object to retrieve a description for. The receiver parameter will contain the actual object description, and apiError can be checked for any error messages.
The code is defining an external prototype (extpgm) for the QUSROBJD API, which is a system API to retrieve object description details. By defining this prototype, an RPG program can call the API, pass it the required parameters like object name and type, and receive the description details and any error messages.
So in summary, this code is setting up the ability to call an API that returns object description details, which could then be used in the RPG program for various purposes. The constants in the prototype are used to specify details about the object you want to retrieve information for."
"""
def generatePrompt(logic) :
    return main(logic)

generatePrompt(logic)