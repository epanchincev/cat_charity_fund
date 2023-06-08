# any
JWT_LIFETIME_SECONDS = 3600
MIN_PASSWORD_LEN = 3
MAX_LEN_NAME_FIELD = 100
EXCLUDED_DONATION_FIELD_FOR_USERS = ['user_id', 'fully_invested', 'close_date', 'invested_amount']

# password error messages
PASSWORD_LESS_THAN_NEED_ERROR = (
    f'Password should be at least {MIN_PASSWORD_LEN} characters'
)
PASSWORD_MUST_NOT_CONTAIN_EMAIL_ERROR = 'Пароль не должен содержаеть e-mail.'

# validator error messages
OBJECT_NOT_FOUND_ERROR = '{} не найден!'
PROJECT_EXISTS_ERROR = 'Проект с таким именем уже существует!'
CLOSED_OBJECT_UPDATE_ERROR = 'Закрытый проект нельзя редактировать!'
OBJECT_INVESTED_DELETE_ERROR = (
    'В проект были внесены средства, не подлежит удалению!'
)
NEW_AMOUNT_LESS_EXISTS_ERROR = (
    'Нельзя установить требуемую сумму меньше уже вложенной.'
)

# user endpoint error messages
DELETING_USERS_IS_NOT_ALLOWED = 'Удаление пользователей запрещено!'
