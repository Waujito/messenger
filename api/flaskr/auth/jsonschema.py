userRegisterSchema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
        },
        "password": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
        }
    },
    "required": ["username", "password"]
}

userLoginSchema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
        },
        "password": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255,
        }
    },
    "required": ["username", "password"]
}
