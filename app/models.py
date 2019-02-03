from app import app, db, bcrypt
import datetime
import jwt


class User(db.Model):
    """
    Table schema
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        self.registered_on = datetime.datetime.now()

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)

    def encode_auth_token(self, user_id):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                                                                       seconds=app.config.get(
                                                                           'AUTH_TOKEN_EXPIRY_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in 'sub'
        :param token: Auth Token
        :return:
        """
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            is_token_blacklisted = BlackListToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was Blacklisted, Please login In'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
        :param email:
        :return:
        """
        return User.query.filter_by(email=email).first()

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        :param new_password: New User Password
        :return:
        """
        self.password = bcrypt.generate_password_hash(new_password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        db.session.commit()


class BlackListToken(db.Model):
    """
    Table to store blacklisted/invalid auth tokens
    """
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def blacklist(self):
        """
        Persist Blacklisted token in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(token):
        """
        Check to find out whether a token has already been blacklisted.
        :param token: Authorization token
        :return:
        """
        response = BlackListToken.query.filter_by(token=token).first()
        if response:
            return True
        return False

class Item(db.Model):
    """
    Table to store item information
    """
    __tablename__='item'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    brand = db.Column(db.String(255))
    category = db.Column(db.String(255))
    productCode = db.Column(db.String(255))

    def __init__(self, name, brand, category, productCode):
        self.name = name
        self.brand = brand
        self.category = category
        self.productCode = productCode

    def save(self):
        """
        Persist item into the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, name, brand, category, productCode):
        """
        Update the records in the item
        :param name: Name
        :param description: Description
        :return:
        """
        self.name = name
        self.brand = brand
        self.category = category
        self.productCode = productCode
        db.session.commit()

    def delete(self):
        """
        Delete an item
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the model
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'productCode': self.productCode
        }

class Variant(db.Model):
    """
    Table to store variant information
    """
    __tablename__='variant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    sellingPrice = db.Column(db.String(255))
    costPrice = db.Column(db.String(255))
    quantity = db.Column(db.Integer)

    def __init__(self, name, item_id, sellingPrice, costPrice, quantity):
        self.name = name
        self.item_id = item_id
        self.sellingPrice = sellingPrice
        self.costPrice = costPrice
        self.quantity = quantity

    def save(self):
        """
        Persist item into the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, name, item_id, sellingPrice, costPrice, quantity):
        """
        Update the records in the item
        :param name: Name
        :param description: Description
        :return:
        """
        self.name = name
        self.item_id = item_id
        self.sellingPrice = sellingPrice
        self.costPrice = costPrice
        self.quantity = quantity

    def delete(self):
        """
        Delete an item
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the model
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'item_id': self.item_id,
            'sellingPrice': self.sellingPrice,
            'costPrice': self.costPrice,
            'quantity': self.quantity
        }

class UserAction(db.Model):
    """
    Table to store userAction logs
    """
    __tablename__='user_action'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), db.ForeignKey('users.email'),  nullable=False)
    item_name = db.Column(db.String(255), nullable=True)
    variant_name = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, item_name, variant_name, action, timestamp):
        self.username = username
        self.item_name = item_name
        self.variant_name = variant_name
        self.action = action
        self.timestamp = timestamp

    def save(self):
        """
        Persist userActionLog into the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete an userActionLog
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the model
        :return:
        """
        return {
            'id': self.id,
            'username': self.username,
            'item_name': self.item_name,
            'variant_name': self.variant_name,
            'action': self.action,
            'timestamp': self.timestamp
        }
