mermaid_FlowchartPrompt_new='''I want to generate code for Mermaid Flow chart diagram using business logic.Remember in future anyone can convert this mermaid class diagram code to java code easily so give answer in context of that. Also give code in correct syntax so that it can be rendered by mermaidjs 8.11.0 . Make sure the blocks are properly linked . Here is also an example how to generate mermaid class diagram using the business logic.
Example :
    User:
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
    
    Mermaid Flowchart code:
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
        AF-->AA

Now the User will provide business logic,generate correct and running code for mermaid Flowchart diagram as shown in above example Make sure that the blocks are properly linked in the code.
'''
