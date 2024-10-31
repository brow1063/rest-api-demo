# Import necessary modules from Flask
# Flask: the core framework for the web app
# jsonify: to convert Python dictionaries to JSON responses
# request: to access incoming request data (e.g., POST data)
# abort: to handle errors and send error status codes
from flask import Flask, jsonify, request, abort

# Initialize the Flask app
app = Flask(__name__)

# In-memory "database" of students
# This dictionary holds a set of student records. 
# In a real-world application, this would be replaced by a database like MySQL, PostgreSQL, or MongoDB.
students = {}

# Define a welcome route to confirm the API is running
@app.route('/')
def index():
    return "Welcome to the Student API! Try accessing /students to see all students."

# Health check route (GET)
# This endpoint returns a 200 OK status and a JSON response to confirm the service is running.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # HTTP status 200 OK

# Route to retrieve all students (GET request)
# This function returns a JSON list of all students when a GET request is sent to /students.
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(students.values())), 200  # 200 is the HTTP status code for 'OK'

# Route to retrieve a single student by their ID (GET request)
# This function returns the student with the specified ID when a GET request is sent to /students/<id>.
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = students.get(student_id)
    if student is None:
        abort(404)  # If the student is not found, return a 404 error (Not Found)
    return jsonify(student), 200  # Return the student as a JSON object with a 200 status code (OK)

# Route to create a new student (POST request)
# This function adds a new student to the list when a POST request is sent to /students with student data.
@app.route('/students', methods=['POST'])
def create_student():
    if not request.json or 'Name' not in request.json:
        abort(400)  # Return a 400 error if the 'Name' field is missing in the request

    # Create a new student with the next available ID, starting from 1
    new_id = max(students.keys(), default=0) + 1
    new_student = {
        'ID': new_id,
        'Name': request.json['Name'],
        'Grade': request.json.get('Grade', 'N/A'),  # Default to 'N/A' if Grade is not provided
        'Email': request.json.get('Email', '')      # Default to an empty string if Email is not provided
    }
    # Add the new student to the dictionary
    students[new_id] = new_student
    return jsonify(new_student), 201  # 201 is the HTTP status code for 'Created'

# Route to update an existing student (PUT request)
# This function updates a student when a PUT request is sent to /students/<id> with updated student data.
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = students.get(student_id)
    if student is None:
        abort(404)  # If the student is not found, return a 404 error (Not Found)
    
    if not request.json:
        abort(400)  # Return a 400 error if the request body is missing or not in JSON format
    
    # Update student's information from the request
    student['Name'] = request.json.get('Name', student['Name'])
    student['Grade'] = request.json.get('Grade', student['Grade'])
    student['Email'] = request.json.get('Email', student['Email'])
    students[student_id] = student
    return jsonify(student), 200  # Return the updated student data with a 200 status code (OK)

# Route to delete a student (DELETE request)
# This function removes the student with the specified ID when a DELETE request is sent to /students/<id>.
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id in students:
        del students[student_id]  # Delete the student from the dictionary
        return '', 204  # 204 is the HTTP status code for 'No Content', indicating the deletion was successful
    else:
        abort(404)  # If the student is not found, return a 404 error (Not Found)

# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
