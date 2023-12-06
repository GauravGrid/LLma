from langchain.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from . import keys

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


