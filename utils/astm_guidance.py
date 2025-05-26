def validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if not data.get(field)]
    return missing
