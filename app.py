# app.py
from flask import Flask, request, jsonify, render_template, send_file
import os, shutil
import bpcs
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)


def deleteContents():
    folder = "tempfiles"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


@app.route("/encode", methods=["POST"])
def encode():
    # clear folder
    deleteContents()

    # receive image and secret message
    file = request.files["file"]
    message = request.form.get("message")

    # save image
    file.save("tempfiles/vessel.png")

    # setting up for later
    alpha = 0.45
    vslfile = "tempfiles/vessel.png"
    msgfile = "tempfiles/message.txt"
    encfile = "tempfiles/encoded.png"

    # save message file
    messageFile = open(msgfile, "w")
    messageFile.write(message)
    messageFile.close()

    # begin encode
    bpcs.encode(vslfile, msgfile, encfile, alpha)
    with open(encfile, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return jsonify({"status": str(encoded_string)})

    # return send_file("tempfiles/encoded.png", mimetype="image/png")


@app.route("/decode", methods=["POST"])
def decode():
    # clear folder
    deleteContents()

    # receive image
    file = request.files["file"]

    # save image
    file.save("tempfiles/encoded.png")

    # setting up for later
    alpha = 0.45
    msgfile = "tempfiles/d_message.txt"
    encfile = "tempfiles/encoded.png"

    # begin decode
    bpcs.decode(encfile, msgfile, alpha)

    # read secret message and return
    with open(msgfile, "r") as file:
        data = file.read().replace("\n", "")
        return jsonify({"MESSAGE": data})


# A welcome message to test our server
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True, port=5000)
