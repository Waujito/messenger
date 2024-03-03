chatCreationRequestSchema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
        }

    },
    "required": ["name"]
}
