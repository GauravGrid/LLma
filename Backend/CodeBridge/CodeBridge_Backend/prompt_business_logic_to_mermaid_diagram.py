java_example2='''
    User=
        1. Initialize left to 0 and right to the length of the array minus one.
        2. Repeat the following steps while left is less than or equal to right:
            i. Calculate mid as the average of left and right.
            ii. If the element at mid is equal to the target, return mid.
            iii. If the element at mid is less than the target, update left to mid + 1.
            iv. Otherwise, update right to mid - 1.
        3. If the loop exits without finding the target, return -1 to indicate that the element is not in the array.
    Mermaid_Code=
        classDiagram
            class "BinarySearch" {
                + binarySearch(arr: array, target: int): int
            }
            class "BinarySearch" {
                + left: int
                + right: int
                + mid: int
                - binarySearch(arr: array, target: int): int
            }
            class "Array" {
                + length: int
                + elementAt(index: int): int
            }
            class "Result" {
                + result: int
            }
            "BinarySearch" --|> "Array" : contains
            "BinarySearch" --|> "Result" : returns
            "BinarySearch" : + Initialize left to 0
            "BinarySearch" : + Initialize right to arr.length - 1
            "BinarySearch" : + binarySearch(arr, target)
            "BinarySearch" : binarySearch(arr, target) {
                + Calculate mid as the average of left and right
                + If elementAt(mid) equals target, return mid
                + If elementAt(mid) < target, update left to mid + 1
                + Else, update right to mid - 1
                + If loop exits without finding target, return -1
            }
            "Array" : + length
            "Array" : + elementAt(index)
            "Result" : + result'''

python_example2='''
    User=
        1.Initialize variables to keep track of the current starting point (start), total petrol surplus/deficit (totalPetrol), and current
        petrol surplus/deficit (currentPetrol).
        2.Loop through each petrol pump in the circular route, calculating the surplus/deficit of petrol at each pump and updating the 
        variables accordingly.
        3.If at any point during the loop, currentPetrol becomes negative, reset it to zero and update the start index to the next pump.
        4.After processing all petrol pumps, check if the totalPetrol is greater than or equal to zero. If it is, return the start index as
        the starting point where the car can complete the circular route. If totalPetrol is negative, return -1, indicating that there is
        no valid starting point.
    Mermaid_Code=
        classDiagram
            class "CircularRouteSolver" {
                +InitializeVariables()
                +LoopThroughPumps()
                +CheckCurrentPetrol()
                +CheckTotalPetrol()
            }
            class "CircularRouteSolver" ..> "PetrolPump" : <<uses>>
            class "PetrolPump" {
                -calculateSurplusDeficit()
            }
            class "CircularRouteSolver" -- "CircularRouteSolver" : <<calls>>
            "CircularRouteSolver" --|> "Java Code" : <<converts>>
            class "Java Code" {
                +int start
                +int totalPetrol
                +int currentPetrol
            }'''

sql_example2='''
    User=
        1. Data Sources- The query retrieves data from three main tables: `products`, `order_items`, and `product_categories`. These tables likely represent products, individual sales transactions, and product categories, respectively.
        2. Product Metrics- For each product, the query calculates the average unit price (`avg_price`), total quantity sold (`total_quantity_sold`), and total revenue (`total_revenue`) generated from all sales.
        3. Grouping- The results are grouped by product category (`category_name`) and product name (`product_name`). This grouping allows us to see how products in each category are performing.
        4. Filtering (HAVING clause)- To focus on significant product performance, the query filters out products with total revenue less than or equal to $10,000. This helps identify products that are contributing substantially to revenue.
        5. Sorting (ORDER BY clause)- The final result set is sorted first by product category in ascending order (`pc.category_name`) and then by total revenue in descending order (`total_revenue DESC`). This arrangement provides a clear view of how products within each category rank in terms of revenue generation.
        Overall, this SQL code is designed to provide a meaningful analysis of product performance within different categories, highlighting top-performing products that have generated significant revenue, while also showing average pricing and quantity sold. This information can be valuable for strategic business decisions, inventory management, and marketing efforts.
    Mermaid_Code=
        classDiagram
            classDef table fill:#f9f,stroke:#333,stroke-width:2px;
            class Products {
                `products`
                --
                `product_id: string`
                `product_name: string`
                `product_category_id: string`
                `unit_price: decimal`
                `...other_fields`
            }
            class OrderItems {
                `order_items`
                --
                `order_id: string`
                `product_id: string`
                `quantity_sold: int`
                `...other_fields`
            }
            class ProductCategories {
                `product_categories`
                --
                `category_id: string`
                `category_name: string`
                `...other_fields`
            }
            class Query {
                `SQL Query`
                --
                `SELECT pc.category_name, p.product_name,`
                `AVG(p.unit_price) AS avg_price,`
                `SUM(oi.quantity_sold) AS total_quantity_sold,`
                `SUM(p.unit_price * oi.quantity_sold) AS total_revenue`
                `FROM products p`
                `JOIN order_items oi ON p.product_id = oi.product_id`
                `JOIN product_categories pc ON p.product_category_id = pc.category_id`
                `GROUP BY pc.category_name, p.product_name`
                `HAVING total_revenue > 10000`
                `ORDER BY pc.category_name ASC, total_revenue DESC`
            }
            Products --> OrderItems : `product_id`
            Products --> ProductCategories : `product_category_id`
            Products ..|> table
            OrderItems ..|> table
            ProductCategories ..|> table
            Query --> Products : `products`
            Query --> OrderItems : `order_items`
            Query --> ProductCategories : `product_categories`'''

mongodb_example2='''
    User=
        The provided code appears to be an aggregation pipeline for querying and aggregating data from a MongoDB database, likely related to orders, products, and product categories.
        Here's a breakdown of the business logic behind this code:
        1. $lookup Stages (Joins): The code starts by performing two `$lookup` stages. These stages essentially perform left outer joins between the `orders` collection and 
        the `products` collection, as well as between the `products` collection and the `product_categories` collection. It links documents based on common fields 
        (`product_id` and `category_id`) to combine data from different collections into a single document.
        2. $unwind Stages: After the `$lookup` stages, the `$unwind` stages are used to deconstruct the arrays created by the `$lookup` operations. This is done to flatten the 
        arrays and work with individual documents for further processing.
        3. $group Stage: The `$group` stage groups the documents by a composite key, consisting of `category_name` from the `product_categories` collection and `product_name`
        from the `products` collection. This step effectively groups orders by product categories and product names. Within each group, it calculates the following metrics:
        - `avg_price`: The average unit price for the products in each category and product combination.
        - `total_quantity_sold`: The total quantity of products sold in each category and product combination.
        - `total_revenue`: The total revenue generated for each category and product combination, calculated as the sum of the product of `unit_price` and `quantity` for each order.
        4. $match Stage: The `$match` stage filters the results to include only those documents where `total_revenue` is greater than 10,000. This step effectively filters out 
        categories and products that haven't generated substantial revenue.
        5. $sort Stage: Finally, the `$sort` stage sorts the results in ascending order of `category_name` and descending order of `total_revenue`. This sorting helps in presenting
        the data in a meaningful and organized way, with the highest revenue categories listed first within each category group.
    Mermaid_Code=
        classDiagram
            classDef aggregationPipeline fill:#F9EBB2,stroke:#E7C065,stroke-width:2px;
            classDef stage fill:#C2FACC,stroke:#5ED36F,stroke-width:2px;
            classDef operation fill:#B4D8E7,stroke:#40A9FF,stroke-width:2px;
            class aggregationPipeline << (A,aggregationPipeline) >>;
            class stage << (S,stage) >>;
            class operation << (O,operation) >>;
            aggregationPipeline --> stage : $lookup Stage
            stage --> operation : $lookup (orders to products)
            stage --> operation : $lookup (products to product_categories)
            stage --> operation : $unwind (deconstruct arrays)
            stage --> operation : $group
            stage --> operation : $match (filter)
            stage --> operation : $sort
            stage --> aggregationPipeline : Result
            Note over aggregationPipeline: MongoDB Aggregation Pipeline
            Note over operation: MongoDB Aggregation Operation
            aggregationPipeline --|> stage
            stage --|> operation'''

react_example2='''
    User=
        The provided React code defines a functional component called `Counter` that implements a simple counter application. The core functionality 
        of this code can be broken down into the following steps:
        1. Initializing State= The component uses the `useState` hook to initialize a state variable `count` with an initial value of 0.
        2. Increment and Decrement Functions=
            - Two functions, `increment` and `decrement`, are defined within the component.
            - `increment` increases the `count` state by 1 when called.
            - `decrement` decreases the `count` state by 1 when called.
        3. Rendering:
        - In the render function, the component returns JSX that displays the following elements:
            - An `<h1>` element with the text "Counter".
            - A `<p>` element that displays the current value of `count`.
            - Two `<button>` elements labeled "Increment" and "Decrement."
            - Each button has an `onClick` event handler that calls either `increment` or `decrement` function when clicked.
        4. User Interface:
            - The user interacts with the application by clicking the "Increment" and "Decrement" buttons.
            - Clicking "Increment" increases the displayed count by 1.
            - Clicking "Decrement" decreases the displayed count by 1.
        5. State Management:
                - The `count` state is managed by React. When `increment` or `decrement` is called, it updates the `count` state, which triggers a re-render of the component with the new value.
        6. Displaying Count:
                - The current value of `count` is displayed within the `<p>` element in the JSX.
        In summary, this React code creates a simple counter application with buttons to increment and decrement a counter value. It uses React's
        state management to keep track of the count and re-renders the component when the count changes, ensuring the UI reflects the current count 
        value.
    Mermaid_Code=
        classDiagram
        class Counter {
            - count: Number = 0
            + increment(): void
            + decrement(): void
        }
        class ReactComponent {
            + render(): JSX
        }
        Counter --|> ReactComponent : extends
'''

angular_example2='''
    User=
        Business Logic Extracted from the Angular Code:
        1. Purpose:
        - The provided Angular code defines a `CounterComponent` that represents a simple counter with an initial count value of 0.
        - It offers the functionality to increment the count when a button is clicked.
        2. Key Algorithmic Steps:
        - Initialize the `count` variable to 0 when the `CounterComponent` is created.
        - Provide an HTML template that displays the current count and a button to increment it.
        - Implement the `incrementCount()` method that increases the `count` by 1 when the button is clicked.
        3. High-Level Logic:
        - Upon initialization, the counter starts at 0.
        - The template displays the current count, and when the "Increment" button is clicked, the count increases by 1.
        4. Code Comments (for clarification):
        - The Angular `@Component` decorator is used to define the component's metadata.
        - The `count` variable represents the current count value.
        - The `incrementCount()` method increases the count by 1 when called.
        - The HTML template displays the current count using interpolation: {{ count }}.
        - The button element has a click event binding that triggers the `incrementCount()` method when clicked.
        5. Business-Relevant Variables:
        - `count` (number): Represents the current count value in the business logic.
        Overall, this Angular component provides a straightforward counter feature, allowing users to see the current count and increment it with a button click.
    Mermaid_Code=
        classDiagram
        class CounterComponent {
            +count: number
            +incrementCount(): void
        }
        class Angular {
            +@Component
        }
        CounterComponent --|> Angular'''

rpg_example2='''
    User=
        The following piece of code declares two data structures, families and people, and then sets up a family with two people. The families data structure is qualified, meaning that it is an array of structures, with each element of the array being a structure. The families data structure has three fields: address, numPeople, and people. The address field is a character field of length 50, and is used to store the address of the family. The numPeople field is an unsigned integer field of length 3, and is used to store the number of people in the family. The people field is an array of structures, with each element of the array being a structure. The people data structure has two fields: name and age. The name field is a character field of length 25, and is used to store the name of the person. The age field is a packed decimal field of length 5, and is used to store the age of the person.
        The code then sets up a family with two people. The address of the family is set to '10 Mockingbird Lane', and the two people are named 'Alice' and 'Bill', with ages of 3 and 15 respectively. The number of people in the family is set to 2. The number of families is set to 1.
        The code then uses a for loop to iterate through the families array. For each family, the address is displayed, and then a nested for loop is used to iterate through the people array. For each person, the name and age are displayed.
        Finally, the return statement indicates the end of the program.
    Mermaid_Code=
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
            Families "1" o-- "*" People : contains'''

sas_example2='''
    User=
        The high-level business logic of the provided SAS code involves visually representing and analyzing data in the form of a bar chart.
        The data preparation step involves reading in data with two variables: "category" and "count." The "category" variable contains categorical 
        values (in this case, likely words or labels like A, B, C, D), while the "count" variable contains numeric values associated with each category.
        The main objective of the code is to create a vertical bar chart where these categorical values (words or labels) are displayed on the x-axis, 
        and the numeric values (counts) are represented as the heights of the bars on the y-axis. This visual representation allows business users to
        quickly and intuitively compare and analyze the distribution of counts across different categories, aiding in data-driven decision-making.
        In summary, the code's business logic involves transforming data with word-based categories and their corresponding numeric values into a visual
        format (bar chart) to facilitate the easy interpretation and analysis of the data's distribution by business stakeholders.  
    Mermaid_Code=
    classDiagram
    class Category {
        - value: string
    }
    class Count {
        - value: number
    }
    Category -- Count : 1..* Contains
    class BusinessLogic {
        - description: string
        + generateChart(): void
    }
    Category -- BusinessLogic : 1..1 Has
    Count -- BusinessLogic : 1..1 Has'''

dspf_exampler2='''
    User=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
    Mermaid_Code=
        classDiagram
        class DisplayFile {
            +initializeDisplay()
            +defineRecordFormat()
            +promptUserForName()
            +displayWelcomeMessage(name)
            +exitProgram()
        }
        class RecordFormat {
            -name: String
            -otherFields: String

            +getName(): String
            +setName(name: String)
            +getOtherFields(): String
            +setOtherFields(otherFields: String)
        }
        class User {
            -name: String

            +getName(): String
            +setName(name: String)
        }
        class DisplayFile --|> RecordFormat : contains
        DisplayFile --|> User : interacts with
'''  

dspf_examplea2='''
    User=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
    Mermaid_Code=
        classDiagram
        class DisplayFile {
            +initializeDisplay()
            +defineRecordFormat()
            +promptUserForName()
            +displayWelcomeMessage(name)
            +exitProgram()
        }
        class RecordFormat {
            -name: String
            -otherFields: String

            +getName(): String
            +setName(name: String)
            +getOtherFields(): String
            +setOtherFields(otherFields: String)
        }
        class User {
            -name: String

            +getName(): String
            +setName(name: String)
        }
        class DisplayFile --|> RecordFormat : contains
        DisplayFile --|> User : interacts with
'''  

assembly_example2='''
        User=
            The provided assembly code calculates the factorial of a given number (n) using a recursive approach. I will break down the code into its key algorithmic steps and then express the logic in a high-level format, along with relevant interactions and data structures.
            1. The code defines a function named `calculate_factorial` to calculate the factorial of a given number. The result is stored in the EAX register, which serves as the return value of the function.
            2. The function starts by pushing the base pointer (EBP) onto the stack and moving the stack pointer (ESP) into EBP to set up the function's stack frame.
            3. It loads the argument (n) into the EAX register from the stack by accessing it at `[ebp + 8]`.
            4. The code then checks if the input value (n) is less than or equal to 1 by comparing it with 1 (`cmp eax, 1`). If n is less than or equal to 1, the code jumps to the `.base_case` label.
            5. In the recursive case (when n > 1), it decrements n by one (`dec eax`), pushes the decremented value onto the stack to save it for the recursive call, and then calls itself (`calculate_factorial`) recursively. After the recursive call, it cleans up the argument from the stack by adjusting the stack pointer (`add esp, 4`).
            6. After returning from the recursive call, it multiplies the result of the recursive call (in EAX) by the original n value, which is still stored on the stack.
            7. The result is stored in EAX, and the code jumps to the `.done` label.
            8. In the base case (n = 0 or n = 1), it sets EAX to 1 because the factorial of 0 and 1 is 1.
            9. Finally, the code pops the base pointer (EBP) from the stack and returns from the function.
            10. In the `_start` section, the code initiates the calculation by pushing the number 5 onto the stack and calling the `calculate_factorial` function.
            11. The result (factorial of 5) is stored in the EAX register.
            12. It sets the result in EAX to EBX for later use, preparing to exit the program.
            13. The program exits by setting EAX to 1 (syscall number for `sys_exit`) and making a system call (`int 0x80`) to the kernel.
            Interactions and Data Structures:
            - The code uses the stack to pass arguments and save the state during recursive calls.
            - The main interaction involves the recursive function calls within `calculate_factorial`, which allows it to calculate the factorial of a number by breaking it down into smaller subproblems.
            - There are no interactions with a database, files, or a user interface in this code. It's a self-contained program that computes the factorial of a number.
            This assembly code is a concise and efficient implementation of a recursive factorial calculation algorithm. It uses the stack for managing function calls and recursion to calculate the result, making it a fundamental example of a recursive algorithm in assembly language.
        Mermaid_Diagram=
            classDiagram
                class Assembly Code {
                    + calculate_factorial()
                }
                class EAX {
                    + value
                }
                class ESP {
                    + value
                }
                class EBP {
                    + value
                }
                class Recursive Call {
                    + decrement()
                    + pushOntoStack()
                    + calculate_factorial()
                    + cleanUp()
                    + multiplyResult()
                }
                class base_case {
                    + setEAXToOne()
                }
                class done {
                    + storeResultInEAX()
                }
                class start {
                    + pushNumber5()
                    + callCalculateFactorial()
                }
                class Kernel {
                    + makeSyscall()
                }
                Assembly Code --|> EAX
                Assembly Code --|> ESP
                Assembly Code --|> EBP
                Assembly Code --> Recursive Call
                Assembly Code --> base_case
                Assembly Code --> done
                Assembly Code --> start
                start --> Assembly Code
                Kernel--> Assembly Code
'''