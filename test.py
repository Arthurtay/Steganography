import bpcs

alpha = 0.45
vslfile = "image.jpg"
msgfile = "message.txt"
encfile = "output.jpeg"
# msgfile_decoded = "tmp.txt"

bpcs.encode(vslfile, msgfile, encfile, alpha)
# embed msgfile in vslfile, write to encfile
# bpcs.decode(encfile, msgfile_decoded, alpha)  # recover message from encfile


# app.py
from flask import Flask, request, jsonify, render_template, send_file
import os
import bpcs

app = Flask(__name__)


@app.route("/encode", methods=["POST"])
def encode():
    file = request.files["file"]
    message = request.form.get("name")
    if file.filename != "":
        extension = file.filename.split(".")[1]
        filename = "original." + extension

        file.save(filename)  # save file
        alpha = 0.45
        vslfile = filename
        msgfile = "message.txt"
        encfile = "encoded.jpeg"
        bpcs.encode(vslfile, msgfile, encfile, alpha)

        return send_file("encoded.jpeg", mimetype="image/jpeg")
    else:
        return jsonify(
            {"ERROR": "Please contact the administrator for more information"}
        )


@app.route("/decode", methods=["POST"])
def decode():
    file = request.files["file"]
    if file.filename != "":
        extension = file.filename.split(".")[1]
        filename = "encoded." + extension

        file.save(filename)  # save file
        alpha = 0.45
        vslfile = filename
        msgfile = "message.txt"
        encfile = filename
        bpcs.decode(encfile, msgfile, alpha)

        with open(msgfile, "r") as file:
            data = file.read().replace("\n", "")
            return jsonify({"MESSAGE": data})
    else:
        return jsonify(
            {"ERROR": "Please contact the administrator for more information"}
        )


# A welcome message to test our server
@app.route("/")
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
