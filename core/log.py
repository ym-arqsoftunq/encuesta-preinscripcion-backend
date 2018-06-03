import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from logging import Formatter

def set_log(app):
    create_file_handler(app)
    create_mail_handler(app)

def create_file_handler(app):
    handler = RotatingFileHandler('logs/encuesta.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)

def create_mail_handler(app):
    mail_handler = SMTPHandler(
        mailhost=(app.config.get('EMAIL_HOST'), app.config.get('EMAIL_PORT')),
        fromaddr=app.config.get('EMAIL_HOST_USER'),
        toaddrs=app.config.get('ADMINS'),
        credentials=(app.config.get('EMAIL_HOST_USER'), app.config.get('EMAIL_HOST_PASSWORD')),
        subject=app.config.get('EMAIL_SUBJECT')
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(mail_handler)
