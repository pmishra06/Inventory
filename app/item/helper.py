from flask import make_response, jsonify, url_for
from app import app
from app.models import Item


def response_for_created_item(item, status_code):
    """
    Method returning the response when a item has been successfully created.
    :param status_code:
    :param item: Item
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': item.id,
        'name': item.name,
        'brand': item.brand,
        'category': item.category,
        'productCode': item.productCode
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


def get_item_json_list(item_list):
    """
    Make json objects of the user items and add them to a list.
    :param item_list: Item
    :return:
    """
    items = []
    for item in item_list:
        items.append(item.json())
    return items


def response_with_pagination(items, previous, nex, count):
    """
    Make a http response for ItemList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param items: item
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'items': items
    })), 200


def paginate_items(page, name):
    """
    Get the items and also paginate the results.
    There is also an option to search for a item name if the query param is set.
    Generate previous and next pagination urls
    :param name: Query name
    :param page: Page number
    :return: Pagination next url, previous url and the user items.
    """
    pagination = Item.query.filter(Item.name.like("%" + name.lower().strip() + "%")) \
        .paginate(page=page, per_page=app.config['VARIANTS_AND_ITEMS_PER_PAGE'], error_out=False)

    previous = None
    if pagination.has_prev:
        previous = url_for('item.itemlist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        nex = url_for('item.itemlist', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous
