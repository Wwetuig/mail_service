'''модуль для обработки задач(тасок) при помощи celery'''

import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smtplib import SMTP
from celery import Celery
from app.config import settings


# Добавляем корень проекта в пути Python
#from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent))  # Переход на уровень выше (из app/ в mai_service/)


# Мнициалищация Celery

celery = Celery(
    'tasks',
    broker=settings.redis_url,    #Брокер отвечает за передачу задач от приложения к Celery-воркерам.
    backend=settings.redis_url,   #Бэкенд хранит результаты выполнения задач, чтобы их можно было получить позже.
)

#logger
import logging
logger = logging.getLogger(__name__)

@celery.task(bind=True, max_retries=3, name="app.tasks.send_email_task")
def send_email_task(self, email_data):
    """Задача Celery для отправки email"""
    try:
        logger.info(f"Starting email send to {email_data['to']}")  # Логируем начало

        msg = MIMEMultipart()
        msg['From'] = settings.from_email
        msg['To'] = email_data['to']
        msg['Subject'] = email_data['subject']

        # Просто текстовое письмо
        msg.attach(MIMEText(email_data['body'], 'plain'))

        # Отправка через SMTP
        with SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            logger.debug("SMTP STARTTLS successful")  # Логируем этапы
            server.login(settings.smtp_user, settings.smtp_password)
            logger.debug("SMTP login successful")
            server.send_message(msg)

        return {"status": "success", "message": f"Email sent to {email_data['to']}"}
    except Exception as e:
        print(e)
        logger.error(f"Email send failed: {str(e)}", exc_info=True)  # Логируем ошибку с traceback
        raise self.retry(exc=e, countdown=60)


#start
#celery -A tasks worker -l info -P eventlet