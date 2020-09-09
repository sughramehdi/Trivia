import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# function to create pagination
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

# creates a dictionary of categories with id as the key and type as the value
def get_category_list():
    categories = {}
    for category in Category.query.all():
        categories[category.id] = category.type
    return categories


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # CORS setup allowing '*' for origins.
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response
  
  # endpoint to handle GET requests for all available categories.
  @app.route('/categories')
  def retrieve_categories():
    try:
      selection = Category.query.order_by(Category.id).all()
      categories = [category.format() for category in selection]

      if len(categories) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'categories': categories,  # this returns categories as a list
        'categoriesasdict': get_category_list()  # this returns categories as a dictionary
      })
    except:
      abort(422)


  # Endpoint to handle GET requests for questions, including pagination
  @app.route('/questions')
  def retrieve_questions():

    try:
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      if len(current_questions) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'categories': get_category_list(),
        'current_category': None
      })

    except:
      abort(422)


  # Endpoint to DELETE question using a question ID.
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'categories': get_category_list(),
        'current_category': None
      })

    except:
      abort(422)

  # Endpoint to create an endpoint to POST a new question, with the question and answer text, category, and difficulty score.
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'categories': get_category_list(),
        'current_category': None
      })

    except:
      abort(422)


  # Endpoint to search questions based on a search term
  @app.route('/questions/search', methods=['POST'])
  def search_questions():

    try:
      searchresults = request.get_json()
      searchterm = searchresults.get('searchTerm')
      selection = Question.query.filter(Question.question.ilike('%' + searchterm + '%')).all()

      current_questions = [question.format() for question in selection]

      # CURRENT ISSUE 1: If I am on page 1, and search results are 14, all 14 will be shown on page 1
      # and clicking on page 2 will show result of GET /questions?page=2     
  
      # CURRENT ISSUE 2: if I am on page 2, and there is only 1 result, then it will show link to page 1
      # but will not navigate there directly.

      return jsonify({
        "questions": current_questions,
        "total_questions": len(selection),
        "current_category": None
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_per_category(category_id):
    try:
      selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      
      if len(current_questions) == 0:
        abort(404)
      
      # CURRENT ISSUE 1: If I am on page 1, and search results are 14, first 10 will be shown on page 1
      # and clicking on page 2 will show result of GET /questions?page=2     
  
      # CURRENT ISSUE 2: if I am on page 2, and there is only 1 result, then it will show link to page 1
      # but will not navigate there directly.
      return jsonify({
        'questions' : current_questions,
        'total_questions' : len(current_questions),
        'current_category' : (Category.query.filter(Category.id==category_id).first()).type
      })

    except:
      abort(422)

  
  # POST endpoint to play the quiz.
  @app.route('/quizzes', methods=['POST'])
  def quiz_questions():
    try:
      body = request.get_json()
      current_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions', None)

      # if 'ALL' is selected in the category selection criteria  
      if current_category['id'] == 0:
        questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
      else: # for a particular category
        questions = Question.query.filter(Question.category==current_category['id']).filter(Question.id.notin_((previous_questions))).all() 
      
      if questions:
        current_question = random.choice(questions)
        return jsonify({
          'success' : True,
          'question' : current_question.format()
        })
      else:
        # once questions finish, this message will be shown
        return jsonify({
          'success' : True,
          'question' : {
            'id': 1000,
            'question': 'No more Questions :)',
            'answer': 'No more Answers',
            'category': 1,
            'difficulty': 1
          }
        })
    except:
      abort(422)


  # Error handlers for Errors in this code
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422
  
  return app

    