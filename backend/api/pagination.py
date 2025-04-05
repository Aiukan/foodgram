"""Пагинация API проекта."""
from rest_framework.pagination import PageNumberPagination

from foodgram_backend.constants import RECIPE_PAGE_SIZE


class RecipePagination(PageNumberPagination):
    """Класс пагинации для рецепта."""

    page_size = RECIPE_PAGE_SIZE
    page_size_query_param = 'limit'
