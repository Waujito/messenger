from werkzeug.exceptions import HTTPException, BadRequest
from flask import json, jsonify, Flask, Blueprint
from jsonschema.exceptions import ValidationError


def register_errorhandlers(app: Flask | Blueprint):
    @app.errorhandler(HTTPException)
    def handleHttpError(e: HTTPException):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({  # type: ignore
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"

        return response

    @app.errorhandler(ValidationError)
    def handleJsonSchemaError(e: ValidationError):
        """Return BadRequest on json-schema validation error"""

        return jsonify(
            {
                "code": 400,
                "name": "Bad Request. Validation Error",
                "message": e.message,
                "schema": e.schema
            }
        ), 400
