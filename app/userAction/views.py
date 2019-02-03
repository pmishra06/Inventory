from flask import Blueprint, request
from app.auth.helper import token_required
from app.userAction.helper import response, response_with_pagination, get_userAction_json_list, paginate_userAction

# Initialize blueprint
useraction = Blueprint('useraction', __name__)


@useraction.route('/useraction/', methods=['GET'])
@token_required
def userActionlist(current_user, user_id=None):
    """
    Return all the user action limit them to 10.
    Return an empty user action object if no user action
    :return:
    """
    page = request.args.get('page', 1, type=int)
    user_name = request.args.get('user_name', None, type=str)

    userActions, nex, pagination, previous = paginate_userAction(page, user_name)

    if userActions:
        return response_with_pagination(get_userAction_json_list(userActions), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)

@useraction.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'variant resource cannot be found', 404)


@useraction.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
