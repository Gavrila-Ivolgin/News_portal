import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import datetime
from news.models import Post, Subscription
from django.utils import timezone  # Поддержка часового пояса

logger = logging.getLogger(__name__)


def my_job():
    """
    posts = Post.objects.order_by('-rating')[:3]
    text = '\n'.join(['{} - {}'.format(p.title, p.rating) for p in posts])
    mail_managers("Посты с высоким рейтингом", text)
    """
    # Получаем список категорий новых постов за неделю
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    # Получаем уникальные значения категорий из этих постов
    categories = set(posts.values_list('postCategory__name', flat=True))  # flat=True - получить список

    # Создаем словарь, где ключ - email, а значение - список категорий
    email_dict = {}
    for category in categories:
        subscriptions = Subscription.objects.filter(category__name=category)
        for subscription in subscriptions:
            email = subscription.user.email
            if email in email_dict:
                email_dict[email].append(category)
            else:
                email_dict[email] = [category]
    # {'gavrivolgin@gmail.com': ['Экономика', 'Культура'], 'Gavrila@mail.ru': ['Экономика', 'Культура']}
    print(email_dict)

    # Отправляем письма с ссылками на новые посты каждому email
    subject = f'Еженедельная рассылка новостей! 🎉🎉🎉'
    for email, categories in email_dict.items():
        # Фильтруем посты по выбранным категориям для каждого email-адреса
        posts = Post.objects.filter(dateCreation__gte=last_week, postCategory__name__in=categories)
        send_email(email, categories, posts, subject)


def send_email(emails, category, posts, subject):
    text = str(posts.values_list('title', flat=True))
    html_content = render_to_string(
        'news/daily_post.html',
        {
            'domain_name': settings.DOMAIN_NAME,
            'category': category,
            'posts': posts,
        }

    )

    # Отправляем email:
    msg = EmailMultiAlternatives(subject, None, None, [emails])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', minute="00", hour="18"),  # Каждую пт. в 18-00
            # trigger=CronTrigger(second="*/3"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
