java_example3='''
    User=
        1. Initialize left to 0 and right to the length of the array minus one.
        2. Repeat the following steps while left is less than or equal to right:
            i. Calculate mid as the average of left and right.
            ii. If the element at mid is equal to the target, return mid.
            iii. If the element at mid is less than the target, update left to mid + 1.
            iv. Otherwise, update right to mid - 1.
        3. If the loop exits without finding the target, return -1 to indicate that the element is not in the array.
    Mermaid_Flowchart_Code=
        graph TD
            A[Initialize left to 0 and right to the length of the array minus one.] --> B[Repeat the following steps while left is less than or equal to right:]
            B --> C[i. Calculate mid as the average of left and right.]
            C --> D[ii. If the element at mid is equal to the target, return mid.]
            D --> E[iii. If the element at mid is less than the target, update left to mid + 1.]
            E --> B
            D --> F[iv. Otherwise, update right to mid - 1.]
            F --> B
            B --> G[If the loop exits without finding the target, return -1 to indicate that the element is not in the array.]'''

python_example3='''
    User=
        1.Initialize variables to keep track of the current starting point (start), total petrol surplus/deficit (totalPetrol), and current
        petrol surplus/deficit (currentPetrol).
        2.Loop through each petrol pump in the circular route, calculating the surplus/deficit of petrol at each pump and updating the 
        variables accordingly.
        3.If at any point during the loop, currentPetrol becomes negative, reset it to zero and update the start index to the next pump.
        4.After processing all petrol pumps, check if the totalPetrol is greater than or equal to zero. If it is, return the start index as
        the starting point where the car can complete the circular route. If totalPetrol is negative, return -1, indicating that there is
        no valid starting point.
    Mermaid_Flowchart_Code=
        graph TD
            A[Initialize variables]
            B[Loop through each petrol pump]
            C[Calculate surplus/deficit]
            D[Update variables]
            E[Check currentPetrol]
            F[Reset if negative]
            G[Update start index]
            H[Check totalPetrol]
            I[Return start index or -1]
            A --> B
            B --> C
            C --> D
            D --> E
            E --> F
            F --> G
            G --> B
            B --> H
            H --> I
            E --> H'''

sql_example3='''
    User=
        1. Data Sources- The query retrieves data from three main tables: `products`, `order_items`, and `product_categories`. These tables likely represent products, individual sales transactions, and product categories, respectively.
        2. Product Metrics- For each product, the query calculates the average unit price (`avg_price`), total quantity sold (`total_quantity_sold`), and total revenue (`total_revenue`) generated from all sales.
        3. Grouping- The results are grouped by product category (`category_name`) and product name (`product_name`). This grouping allows us to see how products in each category are performing.
        4. Filtering (HAVING clause)- To focus on significant product performance, the query filters out products with total revenue less than or equal to $10,000. This helps identify products that are contributing substantially to revenue.
        5. Sorting (ORDER BY clause)- The final result set is sorted first by product category in ascending order (`pc.category_name`) and then by total revenue in descending order (`total_revenue DESC`). This arrangement provides a clear view of how products within each category rank in terms of revenue generation.
        Overall, this SQL code is designed to provide a meaningful analysis of product performance within different categories, highlighting top-performing products that have generated significant revenue, while also showing average pricing and quantity sold. This information can be valuable for strategic business decisions, inventory management, and marketing efforts.
    Mermaid_Flowchart_Code=
        graph TD
            subgraph "Data Sources"
                A[products]
                B[order_items]
                C[product_categories]
            end
            subgraph "Product Metrics"
                D[avg_price]
                E[total_quantity_sold]
                F[total_revenue]
            end
            subgraph "Grouping"
                G[category_name]
                H[product_name]
            end
            subgraph "Filtering (HAVING clause)"
                I[total_revenue <= $10,000]
            end
            subgraph "Sorting (ORDER BY clause)"
                J[pc.category_name ASC]
                K[total_revenue DESC]
            end
            A --> D
            B --> D
            B --> E
            B --> F
            G --> H
            C --> G
            A --> I
            H --> J
            K --> J'''

mongodb_example3='''
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
    Mermaid_Flowchart_Code=
        graph TD
            subgraph MongoDB
                orders -->|$lookup| products
                products -->|$lookup| product_categories
                products -->|unwind| products_unwound
            end
            subgraph Data Processing
                products_unwound -->|$group| grouped_data
                grouped_data -->|$match| filtered_data
                filtered_data -->|$sort| sorted_data
            end
            subgraph Output
                sorted_data
            end'''

react_example3='''
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
    Mermaid_Flowchart_Code=
        graph TD
        subgraph Initialization
            A[Initialize State]
        end
        subgraph Core Functionality
            B[Define increment Function]
            C[Define decrement Function]
        end
        subgraph Rendering
            D[Render Function]
            E[Return JSX]
            F[Display "Counter"]
            G[Display count]
            H[Display "Increment" Button]
            I[Display "Decrement" Button]
            J[Handle onClick Events]
        end
        subgraph User Interaction
            K[User Clicks "Increment" Button]
            L[User Clicks "Decrement" Button]
        end
        subgraph State Management
            M[Manage count State]
            N[Update count State]
            O[Re-render Component]
        end
        subgraph Displaying Count
            P[Display count Value]
        end
        A --> M
        B --> M
        C --> M
        D --> E
        E --> F
        E --> G
        E --> H
        E --> I
        E --> J
        K --> J
        L --> J
        M --> N
        N --> O
        O --> D
        G --> P
        O --> P
'''

angular_example3='''
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
    Mermaid_Flowchart_Code=
        flowchart
        %% Initialization
        subgraph Initialization
            st=>start: Start
            op1=>operation: Initialize count to 0
            e=>end: End
            st->op1->e
        end
        %% User Interface
        subgraph UserInterface
            op2=>operation: Display current count
            op3=>operation: Click "Increment" button
            op4=>operation: Increment count by 1
            op2->op3->op4
        end
        %% Decision
        subgraph Decision
            cond=>condition: Is the button clicked?
            yes=>operation: Yes
            no=>operation: No
            cond(yes)->yes
            cond(no)->no
        end
        %% Final Output
        subgraph FinalOutput
            op5=>operation: Display updated count
            e2=>end: End
            yes->op4->op5->e2
            no->e2
        end
        %% Annotations
        st->op2->cond
        cond(yes)->op3
        cond(no)->op5'''

rpg_example3='''
    User=
        This Code is used to maintain customer master records. It allows displaying, editing, and adding customer records.
        The program starts by checking if any parameters were passed. If not, it closes the display file MTNCUSTD and ends.
        If parameters were passed, it determines if it should display, edit, or add a record based on the parameters. It then initializes 
        various fields, opens the display file if needed, and builds the function key text to display at the bottom of the screen.
        It then enters a loop to handle the requested function.
        For displaying a record, it reads the record from the database, fills the screen fields, protects all fields, displays the screen, 
        and ends the program.
        For editing a record, it reads the record, fills the screen, and enters a loop to handle screen I/O until the data is valid. It 
        allows updating fields like the active status, name, address, phone numbers, etc. If F12 is pressed, the program ends. If Enter 
        is pressed, it updates the database record. If F5 is pressed, it rereads the record in case it was changed by another user.
        For adding a record, it clears the record and screen fields, fills default values, and enters a loop to handle screen I/O until the 
        data is valid. It allows entering all fields to add a new record. If F12 is pressed, the program ends. If Enter is pressed, it adds 
        the new record to the database.
        The program uses various subprocedures to handle specific functions like building the function key text, clearing the screen, 
        protecting/unprotecting fields, handling screen I/O, editing specific fields, adding/updating records, etc.
        It uses a data structure called dfIndDS to keep track of indicators for the display file. It uses named constants for function keys 
        and other values. It has error handling using a subfile for messages and the SndSflMsg subprocedure.
        In summary, this RPG program allows basic maintenance of customer master records including displaying, editing, and adding records.
    Mermaid_Flowchart_Code=
        graph TD
            A[Start]
            B[Check parameters passed]
            C{Parameters?}
            D[Close display file End program]
            E[Determine function Initialize fields]
            F[Open display file]
            G[Build function key text]
            H{Display?}
            I[Read record from DB]
            J[Fill screen fields]
            K[Protect all fields]
            L[Display screen]
            M[End program]
            N{Edit?}
            O[Read record from DB]
            P[Fill screen fields]
            Q[Loop until valid data]
            R[Allow editing fields]
            S{F12 pressed?}
            T[End program]
            U{Enter pressed?}
            V[Update record in DB]
            W[Reread record if changed]
            X{Add?}
            Y[Clear record and fields]
            Z[Fill default values]
            AA[Loop until valid data]
            AB[Allow entering fields]
            AC{F12 pressed?}
            AD[End program]
            AE{Enter pressed?}
            AF[Add record to DB]
            A-->B
            B-->C
            C-- No -->D
            C-- Yes -->E
            E-->F
            E-->G
            G-->H
            H---->I
            I-->J
            J-->K
            K-->L
            L-->M
            G-->N
            N-->O
            O-->P
            P-->Q
            Q-->R
            R-->S
            S-- Yes -->T
            S-- No -->U
            U-- Yes -->V
            V-->W
            W-->Q
            G---->X
            X-->Y
            Y-->Z
            Z-->AA
            AA-->AB
            AB-->AC
            AC-- Yes -->AD
            AC-- No -->AE
            AE-- Yes -->AF
            AF-->AA'''

sas_example3='''
    User=
        The high-level business logic of the provided SAS code involves visually representing and analyzing data in the form of a bar chart.
        The data preparation step involves reading in data with two variables: "category" and "count." The "category" variable contains categorical 
        values (in this case, likely words or labels like A, B, C, D), while the "count" variable contains numeric values associated with each category.
        The main objective of the code is to create a vertical bar chart where these categorical values (words or labels) are displayed on the x-axis, 
        and the numeric values (counts) are represented as the heights of the bars on the y-axis. This visual representation allows business users to
        quickly and intuitively compare and analyze the distribution of counts across different categories, aiding in data-driven decision-making.
        In summary, the code's business logic involves transforming data with word-based categories and their corresponding numeric values into a visual
        format (bar chart) to facilitate the easy interpretation and analysis of the data's distribution by business stakeholders.  
    Mermaid_Flowchart_Code=
        flowchart TB
        subgraph Data_Preparation
            subgraph Read_Data
                rd[Read Data]
            end
            subgraph Data_Transformation
                dt[Data Transformation]
            end
        end
        subgraph Create_Bar_Chart
            cbc[Create Bar Chart]
        end
        subgraph Visualize_Data
            vd[Visualize Data]
        end
        rd --> dt
        dt --> cbc
        cbc --> vd'''

dspf_exampler3='''
     User=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
     Mermaid_Flowchart_Code=
        graph TD
        subgraph Initialization
            A[Initialize Display]
            B[Define Record Format]
            C[Display User Prompt]
        end
        subgraph UserInteraction
            D[User Inputs Name]
            E[Display Welcome Message]
        end
        F[Exit on PF03]
        A --> B
        B --> C
        C --> D
        D --> E
        E --> F
        F -->|Yes| A
        F -->|No| G[End]
        style A fill:#ff9900,stroke:#e68a00
        style B fill:#ff9900,stroke:#e68a00
        style C fill:#ff9900,stroke:#e68a00
        style D fill:#00cc00,stroke:#009900
        style E fill:#00cc00,stroke:#009900
        style F fill:#ff0000,stroke:#cc0000
        style G fill:#cccccc,stroke:#999999
'''  

dspf_examplea3='''
     User=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
     Mermaid_Flowchart_Code=
        graph TD
        subgraph Initialization
            A[Initialize Display]
            B[Define Record Format]
            C[Display User Prompt]
        end
        subgraph UserInteraction
            D[User Inputs Name]
            E[Display Welcome Message]
        end
        F[Exit on PF03]
        A --> B
        B --> C
        C --> D
        D --> E
        E --> F
        F -->|Yes| A
        F -->|No| G[End]
        style A fill:#ff9900,stroke:#e68a00
        style B fill:#ff9900,stroke:#e68a00
        style C fill:#ff9900,stroke:#e68a00
        style D fill:#00cc00,stroke:#009900
        style E fill:#00cc00,stroke:#009900
        style F fill:#ff0000,stroke:#cc0000
        style G fill:#cccccc,stroke:#999999
'''

assembly_example3='''
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
        Mermaid_Flowchart_Code=
            graph TD
                Start((Start))
                DefineFunction[Define Function: calculate_factorial n ]
                PushEBP[Push EBP onto Stack]
                MoveESP[Move ESP into EBP]
                LoadArgument[Load n from Stack]
                CompareN[Compare n with 1]
                BaseCase{Base Case n <= 1?}
                RecursiveCase{Recursive Case n > 1}
                DecrementN[Decrement n by 1]
                PushN[Push n-1 onto Stack]
                CallFunction[Call calculate_factorial n-1]
                CleanupStack[Clean up Stack]
                Multiply[Multiply EAX by original n]
                StoreResult[Store result in EAX]
                Done{Done}
                SetEAXToOne[Set EAX to 1]
                PopEBP[Pop EBP from Stack]
                Start --> DefineFunction
                DefineFunction --> PushEBP
                PushEBP --> MoveESP
                MoveESP --> LoadArgument
                LoadArgument --> CompareN
                CompareN -->|Yes| BaseCase
                CompareN -->|No| RecursiveCase
                BaseCase -->|Yes| SetEAXToOne
                BaseCase -->|No| RecursiveCase
                RecursiveCase --> DecrementN
                DecrementN --> PushN
                PushN --> CallFunction
                CallFunction --> CleanupStack
                CleanupStack --> Multiply
                Multiply --> StoreResult
                StoreResult --> Done
                Done --> PopEBP
'''

