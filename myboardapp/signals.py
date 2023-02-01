from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Comment, Bulletin, CategoryModel
# импортируем модуль для отправки писем
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .views import accepted
from django.contrib.auth.models import User # User is sender
# импортируем модуль для отправки писем
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import date, timedelta
from django.template.loader import render_to_string
import Bboard.settings as settings

@receiver(post_save, sender=Comment)
def create_comment(sender, instance, **kwargs):
    # print(sender.objects.values()) # all comments
    # # bulletin_id = sender.objects.
    # print(instance.username) # a person who created the comment
    # print(instance.id) # id of post
    # we need here an author of the post

    post_url = instance.get_absolute_url()
    full_url = ''.join(['http://', get_current_site('127.0.0.1').domain, ':8000']) + post_url

    auth = Comment.objects.get(id=instance.id).bulletin.author
    # print(auth.email) # post author's email

    print(full_url)

    send_mail(
        subject=f'A new comment from "{instance.username}" is created!',
        message=f'{instance.date_added.strftime("%d %m %Y")} - {instance.body [:50]}', #{full_url}',
        from_email='FPW-13@yandex.ru',
        recipient_list=[auth.email]
    )

# receiving "accepted" signal from views after "accept" function was called and "accepted" signal was sent
@receiver(accepted)
def comment_accepted (sender, **kwargs): # these arguments are passed by post_save
    # in kwargs we receive pk of comment
    # via this pk we can access all other information as bulletin author and comment author
    bulletin = Comment.objects.get(pk=kwargs['pk']).bulletin

    comment = Comment.objects.get(pk=kwargs['pk'])
    comment_auth = comment.username

    print(comment.body)
    print(comment_auth.email)

    send_mail(
        subject=f'Your comment is accepted!',
        message= f'Your comment in post {bulletin.title} from {comment.date_added.strftime("%d/%m/%Y")} - with content {comment.body[:50]} is accepted', #, {full_url}',
        from_email='FPW-13@yandex.ru',
        recipient_list=[comment_auth.email]
    )


# weekly digest of new bulletins for the subscribers
def week_post():
    # if date.today().weekday() == 5:  # если сегодня четверг
        start = date.today() - timedelta(7)  # вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки дат
        finish = date.today()  # сегодняшний день - конец диапазона выборки дат

        # список постов, отфильтрованный по дате создания в диапазоне start и finish
        list_of_bulletins = Bulletin.objects.filter(date_created__range=(start, finish))

        # все возможные категории
        categories = CategoryModel.objects.all()

        # возьмём все возможные категории и пробежимся по ним
        for category in categories:
            # создадим список, куда будем собирать почтовые адреса подписчиков
            subscribers_emails = []
            # из списка всех пользователей
            for user in User.objects.all():
                # отфильтруем только тех, кто подписан на конкретную категорию, по которой идёт выборка
                # делаем это за счёт того, что в модели CategoryModel в поле subscribers
                # мы добавили имя обратной связи от User к CategoryModel, чтобы получить доступ
                # ко всем связанным объектам пользователя --> related_name='subscriber'
                user.subscriber.filter(category_name=category)
                # добавляем в список адреса пользователей, подписанных на текущую категорию
                subscribers_emails.append(user.email)

                # укажем контекст в виде словаря, который будет рендерится в шаблоне week_posts.html
                html_content = render_to_string('apscheduler/week_posts.html',
                                                {'posts': list_of_bulletins, 'category': category})

                # формируем тело письма
                msg = EmailMultiAlternatives(
                    subject=f'По Вашей подписке появились новые объявления за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")

        msg.send()  # отсылаем
        print('Еженедльная рассылка успешна отправлена')
        print(subscribers_emails)
