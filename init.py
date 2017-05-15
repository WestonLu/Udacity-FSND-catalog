from models.items import *
from models.user import *
from models.login import *
from models.jsonfile import *
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
    # app.run(host='127.0.0.1', port=8080)
