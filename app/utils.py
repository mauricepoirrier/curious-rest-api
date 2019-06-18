import os


def has_dependencies(request, is_labeled):
    '''
    Check if request has dependencies
    '''
    if 'image' not in request.files or 'token' not in request.values:
        return False
    elif request.values['token'] == "":
        return False
    if is_labeled:
        if 'label' not in request.values:
            return False
    return True

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
