from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

import sys

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    query = request.args.get('hobby')
    if query is None:
        return create_response({"contacts": db.get('contacts')})
    else:
        if db.getByHobby('contacts', query) is None:
            return create_response(status=404, message="No contact with that hobby exists")

        return create_response({"contacts": db.getByHobby('contacts', query)})

@app.route("/contacts", methods=['POST'])
def create_contact():
    data = request.json
    num_entries = len(data)

    if num_entries != 3:
        return create_response(status=422, message="Could not create contact, not enough data provided, minimum is: name, nickname, and hobby")
    
    name = data.get("name")
    if name is None:
        return create_response(status=422, message='Could not create contact, no "name" info')

    nickname = data.get("nickname")
    if nickname is None:
        return create_response(status=422, message='Could not create contact, no "nickname" info')

    hobby = data.get("hobby")
    if hobby is None:
        return create_response(status=422, message='Could not create contact, no "hobby" info')

    db.create('contacts', data)

    # Not sure if you can pass an empty json? Got a 404 in testing
    # if name is None or nickname is None or hobby is None:
    #     return create_response(status=422, message="Could not create contact, check the data being passed, something might be empty")

    #TODO figure out how to return the new contact
    return create_response(data=data, status=201)

@app.route("/contacts/<id>", methods=['PUT'])
def update_contact(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message='No contact with id "{0}" exists'.format(id))

    data = request.json 

    name = data.get("name")
    if name is None:
        return create_response(status=422, message='Could not create contact, no "name" info')

    hobby = data.get("hobby")
    if hobby is None:
        return create_response(status=422, message='Could not create contact, no "hobby" info')

    db.updateById('contacts', int(id), {"name": name, "hobby": hobby})

    return create_response({"contacts": db.getById('contacts', int(id))})


@app.route("/contacts/<id>", methods=['DELETE'])
def delete_contact(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message='No contact with id "{0}" exists'.format(id))
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")

# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def get_contact_by_id(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message='No contact with id "{0}" exists'.format(id))
    return create_response({"contacts": db.getById('contacts', int(id))})


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
