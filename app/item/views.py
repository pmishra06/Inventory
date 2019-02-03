from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.item.helper import response, response_for_created_item, response_with_pagination, get_item_json_list, paginate_items
from app.userAction.helper import create_userAction
from app.models import Item
import datetime

# Initialize blueprint
item = Blueprint('item', __name__)

@item.route('/item/', methods=['GET'])
@token_required
def itemlist(current_user):
    """
    Return all the items limit them to 10.
    Return an empty items object if no items
    :return:
    """
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '', type=str)

    items, nex, pagination, previous = paginate_items(page, name)

    if items:
        return response_with_pagination(get_item_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)

@item.route('/item/', methods=['POST'])
@token_required
def create_item(current_user):
    """
    Create a item from the sent json data.
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        brand = data.get('brand', None)
        category = data.get('category', None)
        productCode = data.get('productCode', None)
        if name:
            item = Item(name, brand, category, productCode)
            item.save()
            create_userAction(current_user, item, None, 'CREATED', datetime.datetime.utcnow())
            return response_for_created_item(item, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@item.route('/item/', methods=['PUT'])
@token_required
def update_item(current_user):
    """
    Update a item from the sent json data.
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        brand = data.get('brand', None)
        category = data.get('category', None)
        productCode = data.get('productCode', None)

        if not name:
            return response('failed', 'Provide a valid name', 202)

        item = Item.query.filter_by(name=name).first();
        if not item:
            abort(404)
        else:
            item.update(name, brand, category, productCode)
            item.save()
            create_userAction(current_user, item, None, 'UPDATED', datetime.datetime.utcnow())
            return response_for_created_item(item, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@item.route('/item/', methods=['DELETE'])
@token_required
def delete_item(current_user):
    """
    Delete a Item from name sent in json data
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')

        if not name:
            return response('failed', 'Provide a valid name', 202)

        item = Item.query.filter_by(name=name).first();
        if not item:
            abort(404)
        else:
            item.delete()
            create_userAction(current_user, item, None, 'DELETED', datetime.datetime.utcnow())
            return response('success', 'Successfully deleted the item ' + name, 200)



@item.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'item resource cannot be found', 404)


@item.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)