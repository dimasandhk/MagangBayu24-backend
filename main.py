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
            return item
    return {} 

# Dapatkan semua to do
@app.route('/todos', methods=['GET'])
def GetAllTodos():
    return todos

# Post to do
@app.route('/todo', methods=['POST'])
def GetPostTODO():
    data = request.json
    data['status'] = data['status'].lower()

    if 'title' not in data or 'status' not in data or 'subject' not in data or not data['title'] or not data['status'] or not data['subject']:
        return {'error': 'title, status, and subject fields are required and must not be empty'}, 400

    if data['status'] != 'on progress':
        return {'error': 'status must be "on progress"'}, 400

    if 'tags' not in data:
        data['tags'] = []

    data['uid'] = str(uuid.uuid4())
    todos.append(data)
    return todos, 201

# Delete, Centang, dan Dapatkan to do berdasarkan title
@app.route('/todo/<string:title>', methods=['DELETE', 'GET', 'PUT'])
def DeletePutTODO(title):
    if request.method == 'GET':
        result = next(filter(lambda x: x.get('title') == title, todos), None)
        return result if result else [], 404
    
    if request.method == 'DELETE':
        if delete_todo(todos, title):
            return todos
        return todos, 404
    
    updated_todo = update_todo_status(todos, title)
    return updated_todo if updated_todo else updated_todo, 404

# Dapatkan semua to do berdasarkan filter tertentu
@app.route('/todo/filter/<string:type>', methods=['GET'])
def FilterTodoStatus(type):
    query = request.args.get('q')
    if not query: return {'error': 'q query parameter is required'}, 400

    if type != 'subject' or type != 'status' or type != 'tags':
        return {'error': 'todo only filtered by subject, status, and tags'}, 400
    
    if type == 'tags':
        res = [item for item in todos if query in item.get('tags')]
        return res if res else res, 404
    
    res = [item for item in todos if item.get(type) == query]
    return res if res else res, 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)