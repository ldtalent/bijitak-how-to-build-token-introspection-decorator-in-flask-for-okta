import os
from core import create_app

app = create_app(os.environ.get('FLASK_CONFIG'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)