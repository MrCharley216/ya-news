"""Файл для тестирования маршрутов."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', lf('id_for_new')),
        ('users:login', None),
        ('users:signup', None)
    )
)
@pytest.mark.django_db()
def test_pages_availability_for_anonymous_user(client, name, args):
    """Тест доступности страниц для анонимного пользователя."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    [
        (lf('auth_user_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ],
)
@pytest.mark.parametrize('name, args', (
    ('news:edit', lf('id_for_comment')),
    ('news:delete', lf('id_for_comment'))
))
def test_availability_for_comment_edit_and_delete(
    parametrized_client,
    name,
    args,
    expected_status
):
    """Тест для работы со страницами редактирования и удаления."""
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args', (
        ('news:edit', lf('id_for_new')),
        ('news:delete', lf('id_for_new'))
    )
)
@pytest.mark.django_db()
def test_redirect_for_anonymous_client(name, args, client):
    """Тест для редиректа на страницу логина."""
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
