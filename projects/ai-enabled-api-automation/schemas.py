# JSON Schemas for PokéAPI response validation

POKEMON_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "height", "weight", "abilities", "types"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "height": {"type": "integer"},
        "weight": {"type": "integer"},
        "abilities": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["ability", "is_hidden", "slot"],
                "properties": {
                    "ability": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    },
                    "is_hidden": {"type": "boolean"},
                    "slot": {"type": "integer"}
                }
            }
        },
        "types": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["slot", "type"],
                "properties": {
                    "slot": {"type": "integer"},
                    "type": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
}

ABILITY_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "is_main_series"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "is_main_series": {"type": "boolean"},
        "generation": {
            "type": "object",
            "required": ["name", "url"],
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string"}
            }
        }
    }
}

POKEMON_LIST_SCHEMA = {
    "type": "object",
    "required": ["count", "results"],
    "properties": {
        "count": {"type": "integer"},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        }
    }
}