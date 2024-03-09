from flask import Flask, request
import uuid
app = Flask(__name__)

todos = [{
    'uid': str(uuid.uuid4()),
    'title': 'tugas tka',
    'description': 'blablabla',
    'subject': 'tka',
    'status': 'done',
    'tags': ['a', 'b', 'c']
}]

def delete_todo(todos, title):
    for item in todos:
        if item.get('title') == title:
            todos.remove(item)
            return True 
    return False  

def update_todo_status(todos, title):
    for item in todos:
        if item.get('title') == title:
            status = item['status'] 
            item['status'] = 'done' if status == 'on progress' else 'on progress' 
            return True 
    return False 

@app.route('/todos', methods=['GET'])
def GetAllTodos():
    return todos

@app.route('/todo', methods=['POST'])
def GetPostTODO():
    data = request.json

    if 'title' not in data or 'status' not in data or 'subject' not in data or not data['title'] or not data['status'] or not data['subject']:
        return {'error': 'title, status, and subject fields are required and must not be empty'}, 400

    if data['status'] != 'on progress':
        return {'error': 'status must be "on progress"'}, 400

    if 'tags' not in data:
        data['tags'] = []

    data['uid'] = str(uuid.uuid4())
    todos.append(data)
    return todos, 201

@app.route('/todo/<string:title>', methods=['DELETE', 'PUT', 'GET'])
def DeletePutTODO(title):
    if request.method == 'GET':
        result = next(filter(lambda x: x.get('title') == title, todos), None)
        return result if result else [], 404
    
    if request.method == 'DELETE':
        if delete_todo(todos, title):
            return todos
        return todos, 404
    
    if update_todo_status(todos, title):
        return todos

    return todos, 404    


if __name__ == '__main__':
    app.run(debug=True, port=3000)