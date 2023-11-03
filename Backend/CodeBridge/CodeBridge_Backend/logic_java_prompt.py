java_prompt='''I want to generate java code which follow object oriented programming rules of java using logic of rpg code which is given in plain text format.
I am proving some example retated to this task.
User:
The above piece of code declares a data structure named families, which is qualified and has a dimension of 5. It contains three fields: address, numPeople, and people. The address field is a character field of length 50, while numPeople is an unsigned integer field of length 3. The people field is an array of 8 elements, each of which contains two fields: name and age.
The dcl-s statement declares three variables: numFamilies, i, and j. numFamilies is an unsigned integer field of length 5, initialized to 0. i and j are both integer fields of length 10.
The code then sets the address of the first family to '10 Mockingbird Lane', and sets the name and age of the first two people in the family. The numPeople field is also set to 2. The numFamilies variable is then set to 1.
The code then enters a loop, iterating over each family in the families data structure. For each family, the address is displayed using the dsply statement. The code then enters a nested loop, iterating over each person in the family. For each person, the name and age are displayed using the dsply statement.
Finally, the return statement is used to indicate the end of the program.
In summary, this code declares a data structure and three variables, sets the values of the data structure and variables, and then displays the address and name/age of each person in each family. This could be useful for displaying information about a set of families and their members.

Java code:
class Family {
    String address;
    int numPeople;
    Person[] people;
}

class Person {
    String name;
    int age;
}

public class Main {
    public static void main(String[] args) {
        Family[] families = new Family[5];
        for (int i = 0; i < 5; i++) {
            families[i] = new Family();
            families[i].people = new Person[8];
            for (int j = 0; j < 8; j++) {
                families[i].people[j] = new Person();
            }
        }

        int numFamilies = 0;
        int i, j;

        families[0].address = "10 Mockingbird Lane";
        families[0].people[0].name = "Alice";
        families[0].people[0].age = 3;
        families[0].people[1].name = "Bill";
        families[0].people[1].age = 15;
        families[0].numPeople = 2;
        numFamilies = 1;

        for (i = 0; i < numFamilies; i++) {
            System.out.println(families[i].address);
            for (j = 0; j < families[i].numPeople; j++) {
                System.out.println(families[i].people[j].name
                        + " is "
                        + Integer.toString(families[i].people[j].age)
                        + " years old.");
            }
        }
    }
}
Now the User will come and will provide business logic, please generate correct and running Java code as shown in above example without any initial text in a JSON format with "javaCode" as the key. Also include proper comments in the code. 
'''
