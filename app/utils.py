from flask import abort


def has_dependencies(request):
    '''
    Check if request has dependencies
    '''
    if 'image' not in request.files or 'token' not in request.values:
        return False
    elif request.values['token'] == "":
        return False
    return True