# CS4930-project
Terms of Service (TOS) and privacy policy reviewer

## Problem Statement 
Privacy policies are long and difficult to understand, and cause frustrations in the daily lives of most people. Our project is to create a relatively simple and intuitive program to review these documents and provide the user with the information in a format and language that are easier to read and comprehend, so that they can make informed decisions about what they are agreeing to.

## Solution
Our proposed solution is a website that processes privacy policies and provides users with a more approachable summary to read. Users can input a document, paste text, or simply give the URL of a privacy policy and the website will output a natural language summary along with definitions or explanations of confusing terms.

## Tools
### Languages
- Python: Backend, API calls, etc.
- HTML/CSS/JavaScript: frontend UX/UI
### Frameworks and Libraries
- Bootstrap: HTML library
- BeautifulSoup: web scraping

## Demo Instructions
### Mac Instructions 
1. Clone Repository to local machine `git clone <repository_url>`
2. Navigate to repository directory in VS Code Terminal: `cd path/to/directory`
3. Optional, recommended: create a virtual environment `python3 -m venv venv_name` (Must have Python installed)
4. Activate virtual environment `source env_name/bin/activate`
5. Install Django `pip install Django`
6. Install dependencies `pip install requests beautifulsoup4`
7. In the project directory, start development server `python3 manage.py runserver`
8. In web browser, navigate to http://127.0.0.1:8000/home

### Windows Instructons
1. Clone Repository to local machine with `git clone <repository_url>`
2. Navigate to repository directory in VS Code Terminal: `cd path\to\directory`
3. 3. Optional, recommended: create a virtual environment using `python3 -m venv venv_name` (Must have Python installed)
4. Activate virtual environment using `venv_name\Scripts\activate.bat` or with PowerShell: `venv_name\Scripts\Activate.ps1`
5. Install Django `pip install Django`
6. Install dependencies `pip install requests beautifulsoup4`
7. In the project directory, start development server `python3 manage.py runserver`
8. In web browser, navigate to http://127.0.0.1:8000/home
