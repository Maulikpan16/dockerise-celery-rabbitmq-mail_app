from flask import Flask
from flask_mail import Mail, Message
from flask_restful import Api, Resource
import config
from tasks import make_celery

app = Flask(__name__)
api = Api(app)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:@rabbit:5672//' #here rabbit refers to service in docker-compose file
app.config['CELERY_RESULT_BACKEND'] = 'db+sqlite:///db.sqlite3'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

celery = make_celery(app)
mail = Mail(app)


class MailApi(Resource):
    def get(self):
        send_mail.delay()
        return "task is assigned!"


@celery.task(name='send_mail')
def send_mail():
    msg = Message("MAIL API", sender='', recipients=[''])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Mail Sent!"


api.add_resource(MailApi, '/mailapp')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
