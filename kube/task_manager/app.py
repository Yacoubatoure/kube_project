from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Data store for tasks (in-memory for simplicity)
tasks = []

# Home route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API to get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# API to create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify(task), 201

# API to update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['done'] = data.get('done', task['done'])
    
    return jsonify(task)

# API to delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
