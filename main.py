from flask import Flask, request, jsonify
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

def update_todo_tags(todos, title, tags):
    for item in todos:
        if item.get('title') == title:
            item['tags'] += tags
            return item
    return {}     

# Dapatkan semua to do
@app.route('/todos', methods=['GET'])
def GetAllTodos():
    return jsonify(todos), 200

# Post to do
@app.route('/todo', methods=['POST'])
def GetPostTODO():
    data = request.json
    data['status'] = data['status'].lower()

    if 'title' not in data or 'status' not in data or 'subject' not in data or not data['title'] or not data['status'] or not data['subject']:
        return jsonify({'error': 'title, status, and subject fields are required and must not be empty'}), 400

    if data['status'] != 'on progress':
        return jsonify({'error': 'status must be "on progress"'}), 400

    if 'tags' not in data:
        data['tags'] = []

    data['uid'] = str(uuid.uuid4())
    todos.append(data)
    return jsonify(todos), 201

# Delete, Centang, dan Dapatkan to do berdasarkan title
@app.route('/todo/<string:title>', methods=['DELETE', 'GET', 'PUT'])
def DeletePutTODO(title):
    if request.method == 'GET':
        result = next(filter(lambda x: x.get('title') == title, todos), None)
        if result:
            return jsonify(result), 200
        return jsonify([]), 404
    
    if request.method == 'DELETE':
        if delete_todo(todos, title):
            return jsonify(todos), 200
        return jsonify(todos), 404
    
    updated_todo = update_todo_status(todos, title)
    if updated_todo:
        return jsonify(updated_todo), 200
    return jsonify(updated_todo), 404

def is_array_of_strings(arr):
    return isinstance(arr, (list, tuple)) and all(isinstance(item, str) for item in arr)
@app.route('/todo/add-tags/<string:title>', methods=['PUT'])
def AddTags(title):
    data = request.json
    if not is_array_of_strings(data):
        return jsonify({'error': 'please provide an array of tags'}), 400

    res = update_todo_tags(todos, title, data)
    if res:
        return jsonify(res), 200
    return jsonify(res), 404

# Dapatkan semua to do berdasarkan filter tertentu
@app.route('/todo/filter/<string:type>', methods=['GET'])
def FilterTodoStatus(type):
    query = request.args.get('q')

    if not (type != 'subject' or type != 'status' or type != 'tags'):
        return jsonify({'error': 'todo only filtered by subject, status, and tags'}), 400
    
    if not query: return jsonify({'error': 'q query parameter is required'}), 400

    if type == 'tags':
        res = [item for item in todos if query in item.get('tags')]
        if res:
            return jsonify(res), 200
        return jsonify(res), 404
    
    res = [item for item in todos if item.get(type) == query]
    if res:
        return jsonify(res), 200
    return jsonify(res), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)