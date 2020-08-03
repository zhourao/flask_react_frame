def to_success(data):
    data['success'] = True
    return data


def to_error(message):
    return {'success': False, "message": message}
