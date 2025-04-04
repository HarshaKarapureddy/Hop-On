# Harsha Karapureddy
# CS 3354
# Group 6
# File Description: Write Reviews on games from API and stores into databse via SQL#

#imports
import requests
import _sqlite3



# IGDB credential login and token retrieval
url = "https://id.twitch.tv/oauth2/token"
payload = {
    "client_id": "qormdol4xf3yo2keqyzkd6hjqthz4d",
    "client_secret": "rdob8mbokf683y94kaza01pv9keq2k",
    "grant_type": "client_credentials"
}

token_response = requests.post(url, data=payload)

#review databse 
conn = _sqlite3.connect("reviews.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        gameID INTEGER NOT NULL,
        gameName TEXT NOT NULL,
        rating FLOAT NOT NULL,
        reviewText TEXT NOT NULL
    )
''')
conn.commit()

### DATABASE INTERACTIONS ###

# Inserting Review 
def db_write_review(usrID, gameID, gameName, rating, reviewText):
    
    if not valid_userID(usrID):
        return "Error: Invalid UserID"
    
    if not valid_gameID(gameID):
        return "Error: Invalid gameID"
    
    if not valid_rating(rating):
        return "Error: Invalid rating"

    try:
        cursor.execute('''
            INSERT INTO reviews (userID, gameID, gameName, rating, reviewText)
            VALUES (?, ?, ?, ?, ?)
        ''', (usrID, gameID, gameName, rating, reviewText))
        conn.commit()
        return("Review Added!")
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

# Edit Review
def db_edit_review(usrID, reviewID, rating, reviewText):

    if not valid_userID(usrID):
        return "Error: Invalid UserID"
    
    if not valid_reviewID(reviewID):
        return "Error: Invalid ReviewID"
    
    if not valid_rating(rating):
        return "Error: Invalid rating"

    try:
        cursor.execute(''' 
            UPDATE reviews
            SET rating = ?, reviewText = ?
            WHERE userID = ? AND reviewID = ?
        ''', (rating, reviewText, usrID, reviewID)) 
        conn.commit()
        return("Edit Made!")
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

# Delete Review
def db_delete_review(usrID, reviewID):

    if not valid_userID(usrID):
        return "Error: Invalid UserID"
    
    if not valid_reviewID(reviewID):
        return "Error: Invalid ReviewID"

    try:
        cursor.execute(''' 
        DELETE FROM reviews
        WHERE userID = ? AND reviewID = ?
        ''', (usrID, reviewID))
        conn.commit()
        return("Review Removed!")
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

# User Reviews
def db_view_reviews(usrID):

    if not valid_userID(usrID):
        return "Error: Invalid UserID"

    try:
        cursor.execute('SELECT * FROM reviews WHERE userID = ?', (usrID,))
        reviews = cursor.fetchall()
        return reviews if reviews else "No reviews found"
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

# List all Reviews (FOR TROUBLESHOOTING)
def list_reviews_all():
    try:
        cursor.execute('SELECT * FROM reviews')
        reviews = cursor.fetchall()  # Fetch all matching rows
        return reviews if reviews else "No reviews found"
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

def clear_reviews_all():
    try:
        cursor.execute('DELETE FROM reviews')
        conn.commit()
    except _sqlite3.Error as e:
        return f"Database Error: {e}"

### TESTING ###

def valid_userID(usrID):
    return str(usrID).isdigit() and len(str(usrID)) == 6 and int(usrID) > 0

def valid_gameID(gameID):
    return str(gameID).isdigit() and int(gameID) > 0

def valid_rating(rating):
    try:
        rating = float(rating)
        return 0 < rating <= 5.0
    except ValueError:
        return False

def valid_reviewID(reviewID):
    return reviewID.isdigit() and int(reviewID) > 0


### USER INTERACTION ###

# Write review
def user_write_review():
    usrID = input("Enter your UserID: ")
    gameID = input("Enter game ID: ")
    gameName = input("Enter game name: ")
    rating = input("Enter your rating: ")
    reviewText = input("Enter your Review:\n")

    result = db_write_review(usrID, gameID, gameName, rating, reviewText)

    print("\n")

    print(result)

# Edit review
def user_edit_review():
    usrID = input("Enter your UserID: ")
    reviewID = input("Enter the review number (The one that is corresponding next to it): ")
    rating = input("Enter your rating: ")
    reviewText = input("Enter your Review:\n")

    result = db_edit_review(usrID, reviewID, rating, reviewText)
    print("\n")
    print(result)

# delete review
def user_delete_review():
    usrID = input("Enter your UserID: ")
    reviewID = input("Enter the review number (The one that is corresponding next to it): ")

    result = db_delete_review(usrID, reviewID)
    print("\n")
    print(result)

# view your reviews
def user_view_reviews():
    usrID = input("Enter your UserID: ")
    result = db_view_reviews(usrID)
    print("\n")
    
    if isinstance(result, list):
        for review in result:
            print(review)
    else:
        print(result)

# all reviews
def user_list_reviews_all():
    result = list_reviews_all()
    print("\n")
        
    if isinstance(result, list):
        for review in result:
            print(review)
    else:
            print(result)

def main_menu():
    while True:
        print("\nReview Management System")
        print("1. Write a review")
        print("2. Edit a review")
        print("3. Delete a review")
        print("4. View my reviews")
        print("5. List all reviews (Admin)")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_write_review()
        elif choice == "2":
            user_edit_review()
        elif choice == "3":
            user_delete_review()
        elif choice == "4":
            user_view_reviews()
        elif choice == "5":             # for troubleshooting
            user_list_reviews_all()
        elif choice == "6":
            conn.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    
        

if __name__ == "__main__":
    print("Welcome to Hop On!\n")
    main_menu()
    

    