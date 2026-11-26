"""
Пагинация приложения habits.
Pagination of the habits app.
"""

from rest_framework.pagination import LimitOffsetPagination


# ============================================
# Пагинация limit/offset: по 5 привычек на страницу.
# Ответ содержит count, next, previous, results,
# а параметры запроса limit и offset управляют выборкой.
# ============================================
# Limit/offset pagination: 5 habits per page.
# The response contains count, next, previous, results,
# while the limit and offset query params control the slice.
# ============================================
class HabitPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 5
