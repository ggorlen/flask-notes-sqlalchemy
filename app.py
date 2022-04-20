from flask import Flask, jsonify, request
from db import Base, Session
from models import Note

app = Flask(__name__)

#@on_request_end
#def remove_session(req):
#    Session.remove()

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    Session.remove()

@app.route("/api/notes", methods=["GET", "POST"])
def notes():
    session = Session()

    if request.method == "POST":
        if "content" in request.json:
            session.add(Note(content=request.json["content"]))
            session.commit()
            return "", 201

        return "", 422

    return jsonify(session.query(Note).all())

@app.route("/api/notes/<int:note_id>", methods=["GET", "PUT", "DELETE"])
def note(note_id):
    session = Session()

    if request.method == "PUT":
        if "content" not in request.json:
            return "", 422
        elif note := session.query(Note).filter(Note.id == note_id):
            note.update(
                {"content": request.json["content"]},
                synchronize_session="evaluate"
            )
            session.commit()
            return "", 200

        return "", 404
    elif request.method == "DELETE":
        if note := session.query(Note).get(note_id):
            session.delete(note)
            session.commit()
            return "", 200

        return "", 404
    elif result := session.query(Note).get(note_id):
        return jsonify(result)

    return "", 404

@app.route("/", methods=["GET"])
def index():
    return "", 200

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)

