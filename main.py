from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo


app = Flask(__name__)
app.url_map.strict_slashes = False 
app.config['DEBUG'] = True 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2011@localhost:3306/todolistapi' 
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/') 
def main():
    return render_template('index.html')
@app.route('/todos/username', methods=['GET', 'POST'])
@app.route('/todos/username/<username>', methods=['GET', 'PUT', 'POST', 'DELETE'])

def todos(username = None):
    
            
    if request.method == 'GET':
        if username is not None:
            
            todos = Todo.query.filter_by(username=str(username))
            todos = list(map(lambda todo: todo.handleTasks(), todos))
            if todos:
                return jsonify(todos), 200
            else:
                return jsonify({"msg": "User not found"})
        else:
            todos = Todo.query.all()
            todos = list(map(lambda todo: todo.serialize(), todos))
        return jsonify(todos), 200
       
            
    if request.method == 'POST':
        username = request.json.get('username')
        tasks = request.json.get('tasks')
        
        todo = Todo()
        todo.username = username
        todo.tasks = tasks
        todo.save()
        return jsonify(todo.serialize()), 201
        
    if request.method == 'PUT':
        username = request.json.get('username')
        tasks = request.json.get('tasks')
        
        todo = Todo.query.filter_by(username = username).first()
        
        if not todo:
            return jsonify({"msg": "User not found"}), 404
                
        todo.username = username
        todo.tasks = tasks
        todo.update()
        return jsonify(todo.serialize()), 201
    if request.method == 'DELETE':        
        todo = Todo.query.filter_by(username = username).first()
        #todo = todo.serialize()
       
        if not todo:
            return jsonify({"msg": "User not found"}), 404
        todo.delete()
        return jsonify({"success": "User deleted"}), 200

if __name__ == '__main__':
    manager.run()