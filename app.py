from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask, jsonify, request
from main import *


app = Flask(__name__)
app.config.from_object(Config)
print(app)

db = SQLAlchemy(app)



@app.route("/create_item/",methods=['POST']) # создание 
def creat_item_rq():
    data = request.get_json()
    item = ItemPydantic(
        title=data.get('title','no title'),
        author=data.get('author','no author'),
        genre=data.get('genre','no genre'),
        created_at=data.get('created_at','no date')
    )
    create_item(item)
    return jsonify({'message':'created successfully'})


@app.route("/get_items/", methods=['GET'])
def get_items():
    items = get_item() #list
    return jsonify({'data':items})


@app.route('/update_item/<int:id_>/', methods=['PUT'])
def update_items(id_):
    try:
        data = request.get_json()
        item = ItemPydantic(
        title=data.get('title','no title'),
        author=data.get('author','no author'),
        genre=data.get('genre','no genre'),
        created_at=data.get('created_at','no date')
    )
        update_item(id_, item)
        return 'Update Successfully'
    except:
        return "Data was a uncoorrect"


@app.route('/delete_item/<int:id_>/', methods=['DELETE'])
def delete_items(id_):
    items = delete_item(id_)
    return f'Столбец под идентификатором {id_} успешно удалился.'


@app.route('/',methods=['GET'])  #html
def hello():
    return '<h1>Web site with CRUD</h1>'



@app.route("/retrieve_item/<int:item_id>/", methods=['GET'])
def get_one_item(item_id):
    item = retrieve(item_id)
    
    if not item:
        return jsonify({'message':'not found'})

    return jsonify({'data':item})

# if __name__ == '__main__':
#     app.run()
app.run(host="localhost", port=8000)