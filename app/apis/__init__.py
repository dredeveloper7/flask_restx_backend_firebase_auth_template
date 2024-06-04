from flask_restx import Api
from .auth import auth_ns
from .core import core_ns


api = Api(
    title='magicmenuapi',
    version='1.0',
    description='A description',
    doc='/docs',
    security='Bearer Auth',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your bearer token in the format **Bearer &lt;token&gt;**'
        }
    }
)

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(core_ns, path='/health')