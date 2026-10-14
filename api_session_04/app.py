import yaml
from flask import Flask, jsonify, request
from pathlib import Path
from threading import Lock
from uuid import UUID, uuid4
from jsonschema import Draft4Validator, FormatChecker

app = Flask(__name__)
with Path(__file__).with_name('taskapi.yaml').open(encoding='utf-8') as file:
    spec = yaml.safe_load(file)

TOKEN = 'demo-token'
tasks = {}
lock = Lock()
validator = Draft4Validator(spec['components']['schemas']['TaskInput'],
                            format_checker=FormatChecker())


def error(message, code):
    response = jsonify(success=False, message=message)
    response.status_code = code
    if code == 401:
        response.headers['WWW-Authenticate'] = 'Bearer'
    return response


@app.before_request
def check_token():
    if request.path == '/v1/tasks' or request.path.startswith('/v1/tasks/'):
        if request.headers.get('Authorization') != f'Bearer {TOKEN}':
            return error('Thiếu hoặc sai token', 401)


def read_body():
    data = request.get_json(silent=True)
    issue = next(validator.iter_errors(data), None)
    if issue:
        return None, error(issue.message, 422)
    # Chỉ nhận các trường của TaskInput, không cho client thay id.
    fields = spec['components']['schemas']['TaskInput']['properties']
    return {key: value for key, value in data.items() if key in fields}, None


@app.get('/v1/tasks')
def list_tasks():
    try:
        limit = int(request.args.get('limit', '10'))
    except ValueError:
        return error('limit phải là số nguyên', 422)
    status = request.args.get('status')
    if not 1 <= limit <= 100 or status not in (None, 'open', 'done'):
        return error('limit từ 1 đến 100; status là open hoặc done', 422)
    with lock:
        result = [task.copy() for task in tasks.values()
                  if status is None or task['status'] == status]
    return jsonify(success=True, data=result[:limit])


@app.post('/v1/tasks')
def create_task():
    data, failure = read_body()
    if failure is not None:
        return failure
    if 'title' not in data:
        return error('Cần nhập title khi tạo task', 422)
    task = {'id': str(uuid4()), 'status': 'open', 'priority': 'normal', **data}
    with lock:
        tasks[task['id']] = task
    return jsonify(success=True, data=task), 201


@app.route('/v1/tasks/<taskId>', methods=['GET', 'PATCH', 'DELETE'])
def task_detail(taskId):
    try:
        taskId = str(UUID(taskId))
    except ValueError:
        return error('Không tìm thấy task', 404)
    if request.method == 'PATCH':
        data, failure = read_body()
        if failure is not None:
            return failure
    with lock:
        if taskId not in tasks:
            return error('Không tìm thấy task', 404)
        if request.method == 'DELETE':
            del tasks[taskId]
            return '', 204
        if request.method == 'PATCH':
            tasks[taskId].update(data)
        result = tasks[taskId].copy()
    return jsonify(success=True, data=result)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
