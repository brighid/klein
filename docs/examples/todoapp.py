from json import dumps, loads
from os import environ
from uuid import uuid4

from collections import OrderedDict
from exceptions import Exception
from klein import Klein
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

tier = environ.get('tier', 'production')


def parse_error(failure):
    """
    An error handler that turns a Python exception object into a JSON string
    that describes the error.
    """
    error = str(failure.type)
    error_content = '.'.join(
        error[error.find("'"):error.rfind("'")].split('.')[1:])
    error_message = failure.getErrorMessage()
    error_stack = failure.getTraceback() if tier == 'debug' else {}

    return dumps({'error': error_content,
                  'error_message': error_message,
                  'stack': error_stack})


class HTTPError(Exception):
    def __init__(self, message, status):
        super(HTTPError, self).__init__(message)
        self.status = status


class UniqueKeyError(HTTPError):
    def __init__(self, message):
        super(self.__class__, self).__init__(message, 400)


class NotFoundError(HTTPError):
    def __init__(self, message):
        super(self.__class__, self).__init__(message, 404)


class ValidationError(HTTPError):
    def __init__(self, message):
        super(self.__class__, self).__init__(message, 400)


class CustomerStore(object):
    app = Klein()

    def __init__(self):
        # This would be a good place to connect to a database that stores
        # information about customers.
        self.customers = OrderedDict(dict())

    @app.route('/', methods=['GET', 'POST'])
    def create_customer(self, request):
        request.setHeader('Content-Type', 'application/json')

        if request.method == 'POST':
            body = loads(request.content.read())

            if body.keys() != ['first_name', 'last_name', 'country']:
                raise ValidationError(
                    'You must include `first_name` and `last_name` keys')
            # It's always a good day to re-read
            # http://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
            pk = '{first_name} {last_name}'.format(
                first_name=body['first_name'],
                last_name=body['last_name'])

            if pk in self.customers:
                raise UniqueKeyError(
                    'First name + last_name combination must be unique')

            body['id'] = uuid4().get_hex()
            self.customers[pk] = body
            return dumps({'created': body})

        else:
            if not request.args or 'limit' in request.args:
                if not self.customers:
                    raise NotFoundError('No customers in collection')
                # Show only two records by default
                return dumps(self.customers[:request.args.get('limit', 2)])

            elif request.args.keys() != ['first_name', 'last_name']:
                raise ValidationError(
                    'You must include `first_name` and `last_name` keys')
            pk = '{first_name} {last_name}'.format(
                first_name=request.args['first_name'][0],
                last_name=request.args['last_name'][0])
            if pk not in self.customers:
                raise NotFoundError(
                    'Name {!r} not found in collection'.format(pk))
            return dumps(self.customers[pk])

    @app.route('/<string:name>', methods=['PUT'])
    def save_customer(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        body = loads(request.content.read())
        # You can also edit the pk here, which might not be a good idea
        # Allow you to edit `id` here
        if {'first_name', 'last_name', 'id'}.issubset(set(body.keys())):
            raise ValidationError(
                ('You must include `first_name`, `last_name`, '
                 '`country` and/or `id` key(s).'))
        if name not in self.customers:
            raise NotFoundError(
                '"{name}" not found in customer collection.'.format(name=name))

        self.customers[name].update(body)
        return dumps(self.customers[name])

    @app.route('/<string:name>', methods=['GET'])
    def retrieve_customer(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        if name not in self.customers:
            raise NotFoundError(
                '"{name}" not found in customer collection.'.format(name=name))
        return dumps(self.customers[name])

    @app.route('/<string:name>', methods=['DELETE'])
    def delete_customer(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        if name not in self.customers:
            raise NotFoundError(
                '"{name}" not found in customer collection.'.format(name=name))
        return dumps({'deleted': self.customers.pop(name)})

    @app.handle_errors(HTTPError)
    def error_handler(self, request, failure):
        request.setResponseCode(failure.value.status)
        return parse_error(failure)


if __name__ == '__main__':
    store = CustomerStore()
    store.app.run('0.0.0.0', 8080)