import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_by_id(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    print(body)
    if not body:
        return jsonify({"msg": "Invalid input"}), 400

    new_member = {
        "first_name": body.get("first_name"),
        "age": body.get("age"),
        "lucky_numbers": body.get("lucky_numbers"),
    }

    if "id" in body:
        new_member["id"] = body.get("id")

    all_members = jackson_family.add_member(new_member)
    return jsonify({"msg": "Person Added", "members": all_members}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_person(id):
    result = jackson_family.delete_member(id)
    if result[1] == 404:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
