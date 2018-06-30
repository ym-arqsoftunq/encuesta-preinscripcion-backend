from core.app import app
from core.log import set_log

if __name__ == "__main__":
    set_log(app)
    app.run(host='0.0.0.0', debug=False)
