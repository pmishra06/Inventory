from flask import make_response, jsonify, url_for
from app import app
from app.models import UserAction


def create_userAction(user, item, variant, action, timestamp):
    """
    Create a user action.
    :return:
    """
    if variant :
        userAction = UserAction(user.email, item.name, variant.name, action, timestamp)
    else :
        userAction = UserAction(user.email, item.name, None, action, timestamp)
    userAction.save()
    return True

def response_for_created_userAction(userAction, status_code):
    """
    Method returning the response when a userAction has been successfully created.
    :param status_code:
    :param variant: variant
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': userAction.id,
        'username': userAction.username,
        'item_name': userAction.item_name,
        'variant_name': userAction.variant_name,
        'action': userAction.action,
        'timestamp': userAction.timestamp
    })), status_code


def response(status, message, code):
    """
    Helper method to make a http response
    :param status: Status message
    :param message: Response message
    :param code: Response status code
    :return: Http Response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code


def get_userAction_json_list(userAction_list):
    """
    Make json objects of the userActions and add them to a list.
    :param variant_list: Variant
    :return:
    """
    userActions = []
    for userAction in userAction_list:
        userActions.append(userAction.json())
    return userActions


def response_with_pagination(variants, previous, nex, count):
    """
    Make a http response for variantList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param variants: variants
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'variants': variants
    })), 200


def paginate_userAction(page, user_name):
    """
    Get the variants and also paginate the results.
    There is also an option to search for a variant name if the query param is set.
    Generate previous and next pagination urls
    :param name: Query name
    :param page: Page number
    :param item_id : Item id
    :return: Pagination next url, previous url and the user items.
    """
    if user_name:
        pagination = UserAction.query.filter(UserAction.username==user_name) \
            .paginate(page=page, per_page=app.config['VARIANTS_AND_ITEMS_PER_PAGE'], error_out=False)
    else :
        pagination = UserAction.query.filter() \
            .paginate(page=page, per_page=app.config['VARIANTS_AND_ITEMS_PER_PAGE'], error_out=False)


    previous = None
    if pagination.has_prev:
        previous = url_for('useraction.userActionlist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        nex = url_for('useraction.userActionlist', page=page + 1, _external=True)
    userActions = pagination.items
    return userActions, nex, pagination, previous
