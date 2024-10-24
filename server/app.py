from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.order_by(Message.created_at).all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            messages,
            200,
            {'content_type':'application/json'}
        )
        return response

    elif request.method == 'POST':
        if 'body' in request.json and 'username' in request.json:
            newmessage = Message(
                body=request.json.get("body"),
                username=request.json.get("username")
            )
            db.session.add(newmessage)
            db.session.commit()


        message_dict = newmessage.to_dict()

        response = make_response(
            message_dict,
            201,
            {'content_type':'application/json'}
        )
        return response

    return make_response({'error': 'Invalid request method'}, 400)


@app.route('/messages/<int:id>', methods = ['GET','PATCH','DELETE'])
def messages_by_id(id):
    message_id = Message.query.filter_by(id=id).first()
    

    if request.method == 'GET':
        message_id_serialized = message_id.to_dict()
        return make_response( message_id_serialized, 200)

    elif request.method == 'PATCH':
        if 'body' in request.json:
            message_id.body = request.json.get("body")
            db.session.add(message_id)
            db.session.commit()

            message_by_id_dict = message_id.to_dict()

            response = make_response(
                message_by_id_dict,
                200,
                {'content_type':'application/json'}
            )
            return response
        else:
            response = make_response({'error': 'Invalid request body'}, 400)
            return response

    elif request.method == 'DELETE':
        
        db.session.delete(message_id)
        db.session.commit()

        response_body = {
                "delete_successful": True,
                "message": "record deleted successfully."
            }

        response = make_response(
            response_body,
            200
        )

        return response

           
    

if __name__ == '__main__':
    app.run(port=5555)