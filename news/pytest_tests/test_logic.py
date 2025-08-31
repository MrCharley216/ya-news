"""Файл тестов логики проекта."""
import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db()
def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    """Тест, что аноним не может создать комментарий."""
    client.post(detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    auth_user_client,
    detail_url,
    form_data,
    comment_text,
    new
):
    """Тест, что авторизованный пользователь может создать коммент."""
    response = auth_user_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text, comment_text
    assert comment.news, new
    assert comment.author, auth_user_client


def test_user_cant_use_bad_words(bad_words, auth_user_client, detail_url):
    """Проверка цензуры."""
    bad_words_data = {'text': f'Какой-то текст, {bad_words[0]}, еще текст'}
    response = auth_user_client.post(detail_url, data=bad_words_data)
    form = response.context['form']
    assert WARNING in form.errors['text']
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
    author_client,
    delete_url,
    url_to_comments,
    comment
):
    """Проверка возможности удаления комментария атвором."""
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
    auth_user_client,
    delete_url,
    comment
):
    """Проверка, что пользователь не может удалить чужой комментарий."""
    response = auth_user_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client,
    edit_url,
    form_data,
    url_to_comments,
    comment,
    new_comment_text
):
    """Проверка возможности редактирования комментария автором."""
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_comment_text


def test_user_cant_edit_comment_of_another_user(
    auth_user_client,
    edit_url,
    form_data,
    comment,
    comment_text
):
    """Проверка невозможности редактирования чужого комментария."""
    response = auth_user_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
