mermaid_prompt='''I want to generate code with backtick for Mermaid Class diagram using business logic. Remember in future anyone can convert this mermaid class diagram code to java code easily so give answer in context of that. Also give code in correct syntax so that it can be rendered by mermaidjs 8.11.0. . I am providing an example how to generate mermaid class diagram using the business logic shown in the following example.
Example :
    User:
        The following piece of code declares two data structures, families and people, and then sets up a family with two people. The families data structure is qualified, meaning that it is an array of structures, with each element of the array being a structure. The families data structure has three fields: address, numPeople, and people. The address field is a character field of length 50, and is used to store the address of the family. The numPeople field is an unsigned integer field of length 3, and is used to store the number of people in the family. The people field is an array of structures, with each element of the array being a structure. The people data structure has two fields: name and age. The name field is a character field of length 25, and is used to store the name of the person. The age field is a packed decimal field of length 5, and is used to store the age of the person.
        The code then sets up a family with two people. The address of the family is set to '10 Mockingbird Lane', and the two people are named 'Alice' and 'Bill', with ages of 3 and 15 respectively. The number of people in the family is set to 2. The number of families is set to 1.
        The code then uses a for loop to iterate through the families array. For each family, the address is displayed, and then a nested for loop is used to iterate through the people array. For each person, the name and age are displayed.
        Finally, the return statement indicates the end of the program.
    Mermaid code:
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

Now the User will provide business logic, please generate correct and running code for mermaid class diagram as shown in above example without any initial text in a JSON format with "mermaidClassDiagram" as the key.
'''
