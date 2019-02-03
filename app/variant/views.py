from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.variant.helper import response, response_for_created_variant, response_with_pagination, get_variant_json_list, paginate_variants
from app.userAction.helper import create_userAction
from app.models import Variant, Item
import datetime

# Initialize blueprint
variant = Blueprint('variant', __name__)

@variant.route('/variant/', methods=['GET'])
@token_required
def variantlist(current_user):
    """
    Return all the variants limit them to 10.
    Return an empty variants object if no variant
    :return:
    """
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '', type=str)
    item_id = request.args.get('item_id', '', type=str)

    variants, nex, pagination, previous = paginate_variants(page, name, item_id)

    if variants:
        return response_with_pagination(get_variant_json_list(variants), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)

@variant.route('/variant/', methods=['POST'])
@token_required
def create_variant(current_user):
    """
    Create a variant from the sent json data.
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        item_id = data.get('item_id', None)
        sellingPrice = data.get('sellingPrice', None)
        costPrice = data.get('costPrice', None)
        quantity = data.get('quantity', None)

        item = Item.query.filter_by(id=item_id).first();
        if not item:
            return response('failed', 'unknown item id', 202)

        if name:
            variant = Variant(name, item_id, sellingPrice, costPrice, quantity)
            variant.save()
            create_userAction(current_user, item, variant, 'CREATED', datetime.datetime.utcnow())
            return response_for_created_variant(variant, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@variant.route('/variant/', methods=['PUT'])
@token_required
def update_variant(current_user):
    """
    Update a variant from the sent json data.
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        item_id = data.get('item_id', None)
        sellingPrice = data.get('sellingPrice', None)
        costPrice = data.get('costPrice', None)
        quantity = data.get('quantity', None)

        item = Item.query.filter_by(id=item_id).first();
        if not item:
            return response('failed', 'unknown item id', 202)

        if not name:
            return response('failed', 'Provide a valid name', 202)

        variant = Variant.query.filter_by(name=name).first();
        if not variant:
            abort(404)
        else:
            variant.update(name, item_id, sellingPrice, costPrice, quantity)
            variant.save()
            create_userAction(current_user, item, variant, 'UPDATED', datetime.datetime.utcnow())
            return response_for_created_variant(variant, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)

@variant.route('/variant/', methods=['DELETE'])
@token_required
def delete_variant(current_user):
    """
    Delete a variant from name sent in json data
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')

        if not name:
            return response('failed', 'Provide a valid name', 202)

        variant = Variant.query.filter_by(name=name).first();
        if not variant:
            abort(404)
        else:
            item = Item.query.filter_by(id=variant.item_id).first();
            if not item:
                return response('failed', 'unknown item id', 202)

            variant.delete()
            create_userAction(current_user, item, variant, 'DELETED', datetime.datetime.utcnow())
            return response('success', 'Successfully deleted the variant ' + name, 200)



@variant.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'variant resource cannot be found', 404)


@variant.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)