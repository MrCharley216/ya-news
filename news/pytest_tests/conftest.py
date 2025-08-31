"""Файл для фикстур."""
from datetime import datetime

import pytest
from django.test.client import Client
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News
from yanews import settings


@pytest.fixture
def home_url():
    """Передача домашнего адреса."""
    return reverse('news:home')


@pytest.fixture
def detail_url(new):
    """Передача адреса новости."""
    return reverse('news:detail', args=(new.id,))


@pytest.fixture
def url_to_comments(new):
    """адрес с полями комментариев."""
    return reverse('news:detail', args=(new.id,)) + '#comments'


@pytest.fixture
def edit_url(new):
    """Адрес редактирования."""
    return reverse('news:edit', args=(new.id,))


@pytest.fixture
def delete_url(new):
    """Передача адреса удаления."""
    return reverse('news:delete', args=(new.id,))


@pytest.fixture
def author(django_user_model):
    """Создание автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def auth_user(django_user_model):
    """Создание пользователя."""
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def author_client(author):
    """Авторизация автора в клиенте."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def auth_user_client(auth_user):
    """Авторизация пользователя в клиенте."""
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def new():
    """Создание новости."""
    new = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return new


@pytest.fixture
def id_for_new(new):
    """Передача id новости."""
    return (new.id,)


@pytest.fixture
def comment(author, new):
    """Создание комментария."""
    comment = Comment.objects.create(
        news=new,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def id_for_comment(comment):
    """Передача id комментария."""
    return (comment.id,)


@pytest.fixture
def today():
    """Передача сегодняшней даты."""
    return datetime.today()


@pytest.fixture
def many_news(db):
    """Создание пачки новостей для теста."""
    all_news = [
        News(title=f'Новость {index}', text='Просто текст.')
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return News.objects.all()


@pytest.fixture
def comment_text():
    """Текст комментария."""
    return 'Текст комментария'


@pytest.fixture
def new_comment_text():
    """Обновлённый текст комментария."""
    return 'Обновлённый комментарий'


@pytest.fixture
def form_data(new_comment_text):
    """Данные для формы."""
    return {
        'text': new_comment_text,
    }


@pytest.fixture
def bad_words():
    """Список плохих слов."""
    return BAD_WORDS
