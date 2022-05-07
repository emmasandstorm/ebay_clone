ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    """Checks for exact match to an approved image file extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False
