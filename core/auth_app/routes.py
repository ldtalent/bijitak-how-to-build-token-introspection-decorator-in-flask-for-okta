from core.auth_app import bp


@bp.route('/test', methods=['GET'])
def test():
    return "Hello world!", 200