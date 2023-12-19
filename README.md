# cto-rnd-llm-code-modernization
Welcome to the Code Modernizer repository! This project aims to modernize legacy code, such as RPGLE, and convert it into modern languages like Java using the power of a Language Model.
## Table of Contents

- [📜 Introduction](#introduction)
- [📂 Folder Structure](#folder-structure)
- [🚀 Getting Started](#getting-started)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [🔧 Usage](#usage)
## 📜 Introduction

The Code Modernizer project provides a solution for converting legacy code, such as RPGLE, into modern programming languages like Java. Leveraging a Large Language Model, the backend processes the legacy code and generates its modern equivalent, while the frontend offers an intuitive interface for managing and viewing the transformed code.

## 📂 Folder Structure

The repository is organized into two main folders:

- **Backend**: Contains the Django backend code responsible for code transformation.
- **Frontend**: Contains the React + Vite frontend code for user interaction.


## 🚀 Getting Started

Follow these instructions to set up and run the backend and frontend servers for the first time.

### Backend

1. **Prerequisites**: Make sure you have Python and pip installed on your machine. It's recommended to use a virtual environment for isolating project dependencies.

2. **Setup Virtual Environment (Optional)**: Navigate to the `Backend` folder and create a virtual environment:

   ```bash
   cd Backend
   python -m venv venv
   ```

3. **Activate Virtual Environment (Optional)**: Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**: Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. **Install nltk**: Install the required NLTK Libraries:

   ```bash
   python nltkD.py
   ```
6. **Setup Source Files**: (User Stories and Business Logic):
   * Open the search.py file in your preferred text editor.
   * Change the folder path in ```def get_ner_ids_summary``` function to the path of the Business Logic Folder
   * Open the views.py file in your preferred text editor.
   * Change the folder path in ```class ScaniaBusinessLogic(APIView)``` function to the path of the User Stories Folder

6. **Setup API keys**:
   * Create file named ```keys.py``` in Backend/CodeBridge/CodeBridge_Backend.
   * Add Openai, anthropic, jwt_secret and pinecone key in the following way 
   ```bash
   openai_key = "insert key"
   anthropic_key = "insert key"
   JWT_SECRET = 'griddynamics'
   pinecone_key = "insert key"

   ```

7. **Database Setup**: Set up the database and perform migrations:

   ```bash
   cd CodeBridge
   python manage.py migrate
   ```

8. **Run Server**: Start the Django development server:

   ```bash
   python manage.py runserver
   ```

   The backend server should now be running at `http://127.0.0.1:8000`.

### Frontend

1. **Prerequisites**: Make sure you have Node.js and npm (Node Package Manager) installed on your machine.

2. **Navigate to Frontend Folder**: Open a new terminal window and navigate to the `Frontend` folder:

   ```bash
   cd Frontend
   ```

3. **Install Dependencies**: Install frontend dependencies:

   ```bash
   npm install
   ```

4. **Run Development Server**: Start the development server for the frontend:

   ```bash
   npm run dev
   ```

   The frontend development server should now be running at `http://localhost:5173`.


### 🔧 Usage
1.  Access the frontend interface via a web browser at `http://localhost:5173`. 
2.  Upload your legacy code files through the interface.
3.  The backend will process the legacy code using the Language Model and provide the modernized code as output.
4.  Review and download the modernized code.