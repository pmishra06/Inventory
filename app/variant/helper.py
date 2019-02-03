from flask import make_response, jsonify, url_for
from app import app
from app.models import Variant


def response_for_created_variant(variant, status_code):
    """
    Method returning the response when a variant has been successfully created.
    :param status_code:
    :param variant: variant
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': variant.id,
        'name': variant.name,
        'item_id': variant.item_id,
        'sellingPrice': variant.sellingPrice,
        'costPrice': variant.costPrice,
        'quantity': variant.quantity
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


def get_variant_json_list(variant_list):
    """
    Make json objects of the variants and add them to a list.
    :param variant_list: Variant
    :return:
    """
    variants = []
    for variant in variant_list:
        variants.append(variant.json())
    return variants


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


def paginate_variants(page, name, item_id):
    """
    Get the variants and also paginate the results.
    There is also an option to search for a variant name if the query param is set.
    Generate previous and next pagination urls
    :param name: Query name
    :param page: Page number
    :param item_id : Item id
    :return: Pagination next url, previous url and the user items.
    """
    if item_id :
        pagination = Variant.query.filter(Variant.name.like("%" + name.lower().strip() + "%")) \
            .filter(Variant.item_id==item_id) \
            .paginate(page=page, per_page=app.config['VARIANTS_AND_ITEMS_PER_PAGE'], error_out=False)
    else:
        pagination = Variant.query.filter(Variant.name.like("%" + name.lower().strip() + "%")) \
            .paginate(page=page, per_page=app.config['VARIANTS_AND_ITEMS_PER_PAGE'], error_out=False)

    previous = None
    if pagination.has_prev:
        previous = url_for('vaiant.vaiantlist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        nex = url_for('vaiant.vaiantlist', page=page + 1, _external=True)
    vaiants = pagination.items
    return vaiants, nex, pagination, previous
