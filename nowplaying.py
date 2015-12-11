#!/usr/bin/env python3
from flask import Flask, jsonify, request
import npscripts
for module in npscripts.__all__:
    print("Loading npscripts." + module)
    globals()["np_" + module] = getattr(__import__("npscripts", fromlist=[module]), module)

app = Flask(__name__)

def jsonify_code(code, *args, **kwargs):
    response = jsonify(*args, **kwargs)
    response.status_code = code
    return response

@app.route("/get")
def get():
    name = request.args.get("name", "")
    if name:
        if "np_" + name in globals():
            return jsonify(globals()["np_" + name].get_data())
        else:
            return jsonify_code(404, {"error": "Name not found", "code": 404})
    else:
        return jsonify_code(400, {"error": "Bad request", "code": 400})

@app.route("/list")
def list():
    data = {"results": [name[3:] for name in __builtins__.globals() if name[:3] == "np_"]}
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=34574)
