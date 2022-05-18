from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Comment, Bulletin
# импортируем модуль для отправки писем
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .views import accepted
from django.contrib.auth.models import User # User is sender
# импортируем модуль для отправки писем
from django.core.mail import send_mail, EmailMultiAlternatives

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

    # send_mail(
    #     subject=f'A new comment from "{instance.username}" is created!',
    #     message=f'{instance.date_added.strftime("%d %m %Y")} - {instance.body [:50]}', #, {full_url}',
    #     from_email='FPW-13@yandex.ru',
    #     recipient_list=[auth.email]
    # )

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