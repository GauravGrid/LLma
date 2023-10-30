java_example1='''   
    User=   
        public class BinarySearch {{
                public static int binarySearch(int[] arr, int target) {{
                    int left = 0;
                    int right = arr.length - 1;
                    while (left <= right) {{
                        int mid = left + (right - left) / 2;
                        if (arr[mid] == target) {{
                            return mid;
                        }} else if (arr[mid] < target) {{
                            left = mid + 1;
                        }} else {{
                            right = mid - 1;
                        }}
                    }}
                    return -1; // Element not found
                }}
            }}
    Business_Logic=
            1. Initialize two pointers, left and right, to the start and end of the array.
            2. Enter a loop that continues as long as left is less than or equal to right.
            3. Calculate the middle index mid of the current search range.
            4. Check if the element at index mid in the array is equal to the target:
            a. If it is equal, return mid as the result, indicating that the target is found.
            b. If it is not equal:
                i. If the element at index mid is less than the target, update left to mid + 1 to search in the right half of the current range.
                ii. If the element at index mid is greater than the target, update right to mid - 1 to search in the left half of the current range.
            5. If the loop completes without finding the target, return -1 as the result, indicating that the target is not in the array.'''
    
python_example1='''
    User=    
        class PetrolPump:
            def __init__(self, petrol, distance):
                self.petrol = petrol
                self.distance = distance
            def findStartingPoint(pumps):
                n = len(pumps)
                start = 0
                totalPetrol = 0
                currentPetrol = 0
                for i in range(n):
                    totalPetrol += pumps[i].petrol - pumps[i].distance
                    currentPetrol += pumps[i].petrol - pumps[i].distance
                    if currentPetrol < 0:
                        currentPetrol = 0
                        start = i + 1
                if totalPetrol >= 0:
                    return start
                else:
                    return -1
    Business_Logic=
            1.Initialize variables to keep track of the current starting point (start), total petrol surplus/deficit (totalPetrol), and current
            petrol surplus/deficit (currentPetrol).
            2.Loop through each petrol pump in the circular route, calculating the surplus/deficit of petrol at each pump and updating the 
            variables accordingly.
            3.If at any point during the loop, currentPetrol becomes negative, reset it to zero and update the start index to the next pump.
            4.After processing all petrol pumps, check if the totalPetrol is greater than or equal to zero. If it is, return the start index as
            the starting point where the car can complete the circular route. If totalPetrol is negative, return -1, indicating that there is
            no valid starting point.'''
            
sql_example1='''
    User=
        SELECT 
            pc.category_name,
            p.product_name,
            AVG(o.unit_price) AS avg_price,
            SUM(o.quantity) AS total_quantity_sold,
            SUM(o.unit_price * o.quantity) AS total_revenue
        FROM 
            products AS p
        JOIN 
            order_items AS o ON p.product_id = o.product_id
        JOIN 
            product_categories AS pc ON p.category_id = pc.category_id
        GROUP BY 
            pc.category_name, p.product_name
        HAVING 
            SUM(o.unit_price * o.quantity) > 10000
        ORDER BY 
            pc.category_name, total_revenue DESC;
    Business_Logic=
        1. Data Sources- The query retrieves data from three main tables: `products`, `order_items`, and `product_categories`. These tables likely represent products, individual sales transactions, and product categories, respectively.
        2. Product Metrics- For each product, the query calculates the average unit price (`avg_price`), total quantity sold (`total_quantity_sold`), and total revenue (`total_revenue`) generated from all sales.
        3. Grouping- The results are grouped by product category (`category_name`) and product name (`product_name`). This grouping allows us to see how products in each category are performing.
        4. Filtering (HAVING clause)- To focus on significant product performance, the query filters out products with total revenue less than or equal to $10,000. This helps identify products that are contributing substantially to revenue.
        5. Sorting (ORDER BY clause)- The final result set is sorted first by product category in ascending order (`pc.category_name`) and then by total revenue in descending order (`total_revenue DESC`). This arrangement provides a clear view of how products within each category rank in terms of revenue generation.
        Overall, this SQL code is designed to provide a meaningful analysis of product performance within different categories, highlighting top-performing products that have generated significant revenue, while also showing average pricing and quantity sold. This information can be valuable for strategic business decisions, inventory management, and marketing efforts.'''

mongodb_example1='''
    User=
        db.orders.aggregate([
            {{
                $lookup: {{
                    from: "products",
                    localField: "product_id",
                    foreignField: "product_id",
                    as: "product"
                }}
            }},
            {{
                $unwind: "$product"
            }},
            {{
                $lookup: {{
                    from: "product_categories",
                    localField: "product.category_id",
                    foreignField: "category_id",
                    as: "category"
                }}
            }},
            {{
                $unwind: "$category"
            }},
            {{
                $group: {{
                    _id: {{
                        category: "$category.category_name",
                        product: "$product.product_name"
                    }},
                    avg_price: {{ $avg: "$unit_price" }},
                    total_quantity_sold: {{ $sum: "$quantity" }},
                    total_revenue: {{ $sum: {{ $multiply: ["$unit_price", "$quantity"] }} }}
                }}
            }},
            {{
                $match: {{
                    "total_revenue": {{ $gt: 10000 }}
                }}
            }},
            {{
                $sort: {{
                    "_id.category": 1,
                    "total_revenue": -1
                }}
            }}
        ])
    Business_Logic=
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
        the data in a meaningful and organized way, with the highest revenue categories listed first within each category group.'''

react_example1='''
    User=
        import React, {{ useState }} from 'react';
        function Counter() {{
        const [count, setCount] = useState(0);
        const increment = () => {{
            setCount(count + 1);
        }};
        const decrement = () => {{
            setCount(count - 1);
        }};
        return (
            <div>
            <h1>Counter</h1>
            <p>Count: {count}</p>
            <button onClick={increment}>Increment</button>
            <button onClick={decrement}>Decrement</button>
            </div>
        );
        }}
        export default Counter;
    Business_Logic=
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
            value.'''

angular_example1='''
    User=
        import {{ Component }} from '@angular/core';
        @Component({{
        selector: 'app-counter',
        template: `
            <div>
            <p>Count: {{{{ count }}}}</p>
            <button (click)="incrementCount()">Increment</button>
            </div>
        `
        }})
        export class CounterComponent {{
        count: number = 0;

        incrementCount() {{
            this.count++;
        }}
        }}
    Business_Logic= 
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
        Overall, this Angular component provides a straightforward counter feature, allowing users to see the current count and increment it with a button click.'''

rpg_example1='''
    User=
        dcl-c MAX_ELEMS 100;
        dcl-c default_city_name 'London';
        dsply max_elems;
        dsply default_city_name;
        return;
    Business_Logic=
        This piece of code declares two constants, MAX_ELEMS and default_city_name, and then displays their values on
        some kind of output screen or device.MAX_ELEMS is declared to have a value of 100, which means it cannot be changed by the
        program. This constant could be used to limit the number of elements in an array or other data structure.default_city_name
        is declared to have a value of 'London'. This constant could be used to set a default value for a variable or parameter
        that represents a city name.The dsply statements are used to display the values of these constants to the user. This could
        be useful for testing or debugging purposes.Finally, the return statement indicates the end of the program.In summary, this
        code sets up two constants and displays their values, which could be useful for setting default values or limiting the
        size of data structures.'''

sas_example1='''
    User=
        /* Sample data for a bar chart */
        data mydata;
        input category $ count;
        datalines;
        A 10
        B 15
        C 20
        D 12
        ;
        run;
        /* Create a bar chart */
        proc sgplot data=mydata;
        vbar category / response=count;
        run;
    Business_logic=
        The high-level business logic of the provided SAS code involves visually representing and analyzing data in the form of a bar chart.
        The data preparation step involves reading in data with two variables: "category" and "count." The "category" variable contains categorical 
        values (in this case, likely words or labels like A, B, C, D), while the "count" variable contains numeric values associated with each category.
        The main objective of the code is to create a vertical bar chart where these categorical values (words or labels) are displayed on the x-axis, 
        and the numeric values (counts) are represented as the heights of the bars on the y-axis. This visual representation allows business users to
        quickly and intuitively compare and analyze the distribution of counts across different categories, aiding in data-driven decision-making.
        In summary, the code's business logic involves transforming data with word-based categories and their corresponding numeric values into a visual
        format (bar chart) to facilitate the easy interpretation and analysis of the data's distribution by business stakeholders.'''
        
dspf_exampler1='''
       User= 
        A                                      A          DSPSIZ(24 80 *DS3)
        A          R MAINRCD
        A                                  2  2'Enter Your Name:'
        A            NAME      30A  B  2 20
        A                                  4  2'Welcome,'
        A                                  4 13 NAME
        A                                      A          CF03(03 'Exit')
       Business_Logic=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
'''  

dspf_examplea1='''
       User= 
        A                                      A          DSPSIZ(24 80 *DS3)
        A          R MAINRCD
        A                                  2  2'Enter Your Name:'
        A            NAME      30A  B  2 20
        A                                  4  2'Welcome,'
        A                                  4 13 NAME
        A                                      A          CF03(03 'Exit')
       Business_Logic=
       The provided DSPF (Display File) code defines a display interface for capturing a user's name and displaying a welcome message. 
       It initializes the display, defines a record format for data organization, prompts the user to enter their name, provides an 
       input field for name input, displays a welcome message that includes the user's name, and allows the user to exit the program
       by pressing PF03. This code's core business logic involves user interaction and data presentation, with the "NAME" variable 
       storing the user's input. The code uses DSPF-specific functions and parameters for display file configuration and interaction.
''' 

assembly_example1='''
        User=
            section .data
                ; No data section needed for this example
            section .text
                global _start
            ; Function to calculate factorial
            calculate_factorial:
                push ebp
                mov ebp, esp
                mov eax, [ebp + 8]  ; Load the argument (n) into EAX
                ; Check for the base case (n <= 1)
                cmp eax, 1
                jle .base_case
                ; Recursive case: n * factorial(n-1)
                dec eax
                push eax            ; Save the decremented value
                call calculate_factorial
                add esp, 4          ; Clean up the argument on the stack
                ; Multiply the result of the recursive call by n
                imul eax, [ebp + 8]
                jmp .done
            .base_case:
                ; Base case: factorial(0) and factorial(1) are both 1
                mov eax, 1
            .done:
                pop ebp
                ret
            _start:
                ; Input: The number for which to calculate the factorial (e.g., 5)
                push 5
                call calculate_factorial
                ; The result (factorial) is now in EAX
                ; Exit the program
                mov ebx, eax
                mov eax, 1           ; syscall number for sys_exit
                int 0x80             ; Call the kernel
        Business_Logic=
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
'''

