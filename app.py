from flask import Flask, render_template, request, redirect, url_for
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.final_software


app = Flask(__name__)


@app.route("/message", methods=["GET"])
def message_get():
    return render_template("message.html")


@app.route("/message", methods=["POST"])
def message_post():
    if request.form.get("get_topic"):
        topic = request.form.get("get_topic")
        return redirect(url_for("get_topic", topic=topic))

    message = request.form.get("message")
    topic = request.form.get("topic")
    new_elem = {"message": message, 
                "topic": topic
    }
    db.messages.insert_one(new_elem)
    return render_template("message.html")


@app.route("/message/<topic>", methods=["GET"])
def get_topic(topic):
    retorno = {"messages": []}
    
    for message in db.messages.find({"topic": topic}, { "_id": 0}):
        retorno["messages"].append(message)
    return retorno

if __name__ == "__main__":
    app.run(port=5000, debug=True)