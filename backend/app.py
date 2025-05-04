from flask import Flask, request, jsonify, g
from flask_cors import CORS
import traceback
import sys
from search_manager import SearchGS
from review_manager import (
    db_write_review,
    db_edit_review,
    db_delete_review,
    db_view_reviews,
    list_reviews_all,
    game_search_by_id,  # Import this function from review_manager
    valid_userID,
    valid_gameID,
    valid_rating,
    valid_reviewID
)
from recommendation_system import (
    user_top_genres,
    match_ids,
    get_trending_games_by_genres,
    recommend_games_for_user
)

app = Flask(__name__)

CORS(app)

DATABASE = 'reviews.db'
app.config['DATABASE'] = DATABASE

@app.route('/api/search', methods=['GET'])
def search_games():
    game_name = request.args.get('q')
    if not game_name:
        return jsonify({'error': 'Missing query parameter'}), 400

    results = SearchGS(game_name)
    if results is None:
        return jsonify({'error': 'Search failed or returned no results'}), 500

    return jsonify(results)


@app.route('/reviews/make', methods=['POST'])
def write_review():
    try:
        print("Received review submission request")
        data = request.get_json()
        print(f"Request data: {data}")
        
        user_id = data.get('user_id')
        game_id = data.get('game_id')
        rating = data.get('rating')
        review_text = data.get('review_text')

        print(f"Extracted fields - user_id: {user_id}, game_id: {game_id}, rating: {rating}")

        # Input validation
        if not user_id or not game_id or not rating or not review_text:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # Validate user_id format
        if not valid_userID(user_id):
            return jsonify({'status': 'error', 'message': 'Invalid user ID format. Must be 6 digits.'}), 400

        # Validate game_id format
        if not valid_gameID(game_id):
            return jsonify({'status': 'error', 'message': 'Invalid game ID format'}), 400

        # Validate rating
        if not valid_rating(rating):
            return jsonify({'status': 'error', 'message': 'Invalid rating. Must be between 1 and 5.'}), 400

        # Get game name and genre from IGDB
        print(f"Fetching game info for game_id: {game_id}")
        game_name, genre = game_search_by_id(game_id)
        print(f"Game info - name: {game_name}, genre: {genre}")
        
        if not game_name:
            return jsonify({'status': 'error', 'message': 'Failed to fetch game info'}), 500

        # Write review to database
        print("Writing review to database")
        result = db_write_review(user_id, game_id, game_name, genre, rating, review_text)
        print(f"Database result: {result}")
        
        if result == "Review Added!":
            return jsonify({'status': 'success', 'message': 'Review submitted successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': result}), 500
            
    except Exception as e:
        print(f"Exception in write_review: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/reviews/edit', methods=['PUT'])
def edit_review():
    try:
        print("Received edit review request")
        data = request.get_json()
        print(f"Request data: {data}")
        
        user_id = data.get('user_id')  # Try to get user_id if sent
        review_id = data.get('review_id')
        new_rating = data.get('new_rating')
        new_review_text = data.get('new_review_text')

        if not review_id or not new_rating or not new_review_text:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # Validate review_id
        if not valid_reviewID(review_id):
            return jsonify({'status': 'error', 'message': 'Invalid review ID format'}), 400

        # Validate rating
        if not valid_rating(new_rating):
            return jsonify({'status': 'error', 'message': 'Invalid rating. Must be between 1 and 5.'}), 400

        print(f"Editing review - review_id: {review_id}, rating: {new_rating}")
        result = db_edit_review(user_id, review_id, new_rating, new_review_text)
        print(f"Database result: {result}")
        
        if "Error" in result:
            return jsonify({'status': 'error', 'message': result}), 400
        return jsonify({'status': 'success', 'message': 'Review edited successfully'}), 200
    except Exception as e:
        print(f"Exception in edit_review: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/reviews/delete', methods=['DELETE'])
def delete_review():
    try:
        print("Received delete review request")
        data = request.get_json()
        print(f"Request data: {data}")
        
        user_id = data.get('user_id')
        review_id = data.get('review_id')

        if not user_id or not review_id:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
            
        # Validate user_id
        if not valid_userID(user_id):
            return jsonify({'status': 'error', 'message': 'Invalid user ID format'}), 400
            
        # Validate review_id
        if not valid_reviewID(review_id):
            return jsonify({'status': 'error', 'message': 'Invalid review ID format'}), 400

        print(f"Deleting review - user_id: {user_id}, review_id: {review_id}")
        result = db_delete_review(user_id, review_id)
        print(f"Database result: {result}")
        
        if "Error" in result:
            return jsonify({'status': 'error', 'message': result}), 400
        return jsonify({'status': 'success', 'message': 'Review deleted successfully'}), 200
    except Exception as e:
        print(f"Exception in delete_review: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/reviews/view', methods=['GET'])
def view_reviews():
    try:
        print("Received view reviews request")
        user_id = request.args.get('user_id')
        print(f"Request param - user_id: {user_id}")
        
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Missing user_id parameter'}), 400
            
        # Validate user_id
        if not valid_userID(user_id):
            return jsonify({'status': 'error', 'message': 'Invalid user ID format'}), 400

        print(f"Fetching reviews for user_id: {user_id}")
        reviews = db_view_reviews(user_id)
        print(f"Database result type: {type(reviews)}")
        
        if isinstance(reviews, str) and "Error" in reviews:
            return jsonify({'status': 'error', 'message': reviews}), 400
        return jsonify(reviews)
    except Exception as e:
        print(f"Exception in view_reviews: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


@app.route('/reviews/all', methods=['GET'])
def view_all_reviews():
    try:
        print("Received view all reviews request")
        reviews = list_reviews_all()
        return jsonify(reviews)
    except Exception as e:
        print(f"Exception in view_all_reviews: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        print("Received recommendations request")
        user_id = request.json.get('userID') 

        print(f"Request body - user_id: {user_id}")
        
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Missing user_id parameter'}), 400

        if not valid_userID(user_id):  
            return jsonify({'status': 'error', 'message': 'Invalid user ID format'}), 400

        recommendations = recommend_games_for_user(user_id)
        print(f"Recommendations: {recommendations}")

        if not recommendations:
            return jsonify({'status': 'error', 'message': 'No recommendations found for this user'}), 404

        return jsonify({
            'recommendations': recommendations
        })

    except Exception as e:
        print(f"Exception in get_recommendations: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
