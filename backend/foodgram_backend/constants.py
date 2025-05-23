"""Константы приложения foodgram_backend."""
MAX_FIRST_NAME_LENGTH = 150

MAX_LAST_NAME_LENGTH = 150

MAX_USERNAME_LENGTH = 150

MAX_EMAIL_LENGTH = 254

INGREDIENT_NAME_MAX_LENGTH = 128

MEASUREMENT_UNIT_MAX_LENGTH = 64

RECIPE_NAME_MAX_LENGTH = 256

TAGS_NAME_MAX_LENGTH = 32

TAGS_SLUG_MAX_LENGTH = 32

INGREDIENT_AMOUNT_MIN = 1

INGREDIENT_AMOUNT_MAX = 32000

AMOUNT_MIN_ERROR = f'Количество должно быть не меньше {INGREDIENT_AMOUNT_MIN}.'

AMOUNT_MAX_ERROR = f'Количество не должно превышать {INGREDIENT_AMOUNT_MAX}.'

COOKING_TIME_MIN = 1

COOKING_TIME_MAX = 32000

COOKING_TIME_MIN_ERROR = (
    f'Время приготовления должно быть не меньше {COOKING_TIME_MIN}.'
)

COOKING_TIME_MAX_ERROR = (
    f'Время приготовления не должно превышать {COOKING_TIME_MAX}.'
)

INGREDIENT_FORMAT = '{0} — {1}'

RECIPE_PAGE_SIZE = 6

SHORT_CODE_MAX_LENGTH = 8
