from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS

from models.database import db_session
from modules.schema import schema

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/api/hello')
def hello():
    return { 'hello': 'world' }

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True    
    )
)

if __name__ == '__main__':
    app.run()
