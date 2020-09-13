# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks - Completed

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## ENDPOINT DETAILS - TO BE REVIEWED

Endpoints:

GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

# GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: 
    - 'success': A boolean value (True or False) based on the successful execution of the method.
    - 'categories': An object with multiple dictionary objects. Each category has a dictionary. Example:
    [
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ]
    - 'categoriesasdict': An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}

# GET '/questions'
- This endpoint handles GET requests for questions, including pagination (every 10 questions). It returns a list of questions, the number of total questions, current category, and categories. 

- When you start the application, you will see questions and categories generated, ten questions per page and pagination at the bottom of the screen for two pages. Clicking on the page number updates the questions.

- Request Arguments: Page Numbers (auto generated by front-end as Query String Parameter)

- Returns:
    - 'success': A boolean value (True or False) based on the successful execution of the method.
    - 'questions': A list of question objects. Each object contains:
        - 'question': the question string
        - 'answer': the answer string
        - 'difficulty': the difficulty score
        - 'category': the category id the question belongs to. 
    - 'total_questions': The total number of questions present in all categories
    - 'categories': A dictionary of categories with category_id:category_type as the key:value pairs.
    - 'current_category': Null value

# DELETE /questions/<int:question_id>

- This endpoint deletes a question permenantly using a question ID.
- To test this endpoint, you can click the trash icon next to a question, the question will be removed. This removal persists in the database even when the page is refreshed.
- Once the question is deleted, the page is refreshed with the revised list of questions.

Request Arguments: An integer, Question ID

Returns:
- 'success': A boolean value (True or False) based on the successful execution of the method.
- 'question_id': The ID of the deleted question.
- 'questions': A list of question objects. Each object contains:
  - 'question': the question string
  - 'answer': the answer string
  - 'difficulty': the difficulty score
  - 'category': the category id the question belongs to. 
- 'total_questions': The total number of questions present in all categories
- 'categories': A dictionary of categories with category_id:category_type as the key:value pairs.
- 'current_category': Null value

# POST '/questions' to create a new question

- This endpoint creates a new question object in the database.
- When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page of the questions list in the "List" tab.

Request Arguments:
- 'question': the question string
- 'answer': the answer string
- 'difficulty': the difficulty score
- 'category': the category id the question belongs to. 

Returns:
- 'success': A boolean value (True or False) based on the successful execution of the method.
- 'created': The ID of the created question.
- 'questions': A list of question objects. Each object contains:
  - 'question': the question string
  - 'answer': the answer string
  - 'difficulty': the difficulty score
  - 'category': the category id the question belongs to. 
- 'total_questions': The total number of questions present in all categories
- 'categories': A dictionary of categories with category_id:category_type as the key:value pairs.
- 'current_category': Null value


# POST '/questions/search' 

- This endpoint gets questions based on the requested search term.
- It returns any and all questions for whom the search term is a substring of the question. 

- CURRENT ISSUE 1: If I am on page 1, and search results are 14, all 14 will be shown on page 1 and clicking on page 2 will show result of GET /questions?page=2     
  
- CURRENT ISSUE 2: if I am on page 2, and there is only 1 result, then it will show link to page 1 but will not navigate there directly.

Request Arguments:
- 'searchTerm': The string to be searched

Returns:
- 'success': A boolean value (True or False) based on the successful execution of the method.
- 'questions': A list of question objects that contain the 'searchTerm'. Each object contains:
  - 'question': the question string
  - 'answer': the answer string
  - 'difficulty': the difficulty score
  - 'category': the category id the question belongs to. 
- 'total_questions': The total number of questions that contain the 'searchTerm'
- 'current_category': Null Value

# GET '/categories/<int:category_id>/questions'

- This endpoint gets questions based on category. 

- In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. 
  
- CURRENT ISSUE 1: If I am on page 1, and search results are 14, first 10 will be shown on page 1 and clicking on page 2 will show result of GET /questions?page=2     
- CURRENT ISSUE 2: if I am on page 2, and there is only 1 result, then it will show link to page 1 but will not navigate there directly.

Request Parameter:
- category_id : The ID of the required category

Returns:
- 'success': A boolean value (True or False) based on the successful execution of the method.
- 'questions': A list of question objects that belong to the requested category. Each object contains:
  - 'question': the question string
  - 'answer': the answer string
  - 'difficulty': the difficulty score
  - 'category': the category id the question belongs to. 
- 'total_questions': The total number of questions that belong to the requested category
- 'current_category': The requested category name/type.

# POST '/quizzes'

- This endpoint gets questions to play the quiz. 
- It takes the category selected on the 'Play' tab and returns a random question from that category, if provided, and that is not one of the previous questions. 
- One question is displayed at a time, and the user is allowed to answer. They are also shown whether they were correct or not.
- The questions are displayed until there are no more questions in that category.

Request Parameters:
- 'previous_questions': List of IDs of the questions previously asked 
- quiz_category: An object specifying the type and ID of the category selected: For example: {type: "Art", id: "2"}

Returns:
- 'success': A boolean value (True or False) based on the successful execution of the method.
- 'question': A random question object from the selected category that has not been previously asked:
  - 'id': The question ID
  - 'question': the question string
  - 'answer': the answer string
  - 'difficulty': the difficulty score
  - 'category': the category id the question belongs to.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```