from string import ascii_lowercase, ascii_uppercase, digits

EN_LOWER = set(ascii_lowercase)
EN_UPPER = set(ascii_uppercase)
DIGITS = set(digits)
RUS_LOWER = set("йцукенгшщзхфывапролджэячсмитбюьъё")
RUS_UPPER = set("ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЬЪЁ")
FORBIDDEN_EXTRA = set("`~!@№#;$%:^&?*()-+={}[]'/|<>")


def validate_login(login: str, cur, table: str) -> list[str]:
    errors = []
    if len(login) < 8:
        errors.append("Логин должен содержать не менее 8 символов")
    cur.execute(f"SELECT 1 FROM {table} WHERE Login = ?", (login,))
    if cur.fetchone():
        errors.append("Такой логин уже используется")
    return errors


def validate_password(password: str) -> list[str]:
    errors = []
    if len(password) < 8:
        errors.append("Пароль должен содержать не менее 8 символов")
    if not any(ch in EN_LOWER for ch in password):
        errors.append("Пароль должен содержать хотя бы одну строчную английскую букву")
    if not any(ch in EN_UPPER for ch in password):
        errors.append("Пароль должен содержать хотя бы одну заглавную английскую букву")
    if not any(ch in DIGITS for ch in password):
        errors.append("Пароль должен содержать хотя бы одну цифру")
    if any(ch in RUS_LOWER or ch in RUS_UPPER for ch in password):
        errors.append("Пароль должен содержать только английские буквы и цифры")
    if any(ch in FORBIDDEN_EXTRA for ch in password):
        errors.append('Пароль не должен содержать спецсимволы (допускается только "_")')
    return errors


def validate_names(fam: str, name: str, oth: str) -> list[str]:
    errors = []
    if not fam.strip():
        errors.append("Введите фамилию")
    if not name.strip():
        errors.append("Введите имя")
    if not oth.strip():
        errors.append("Введите отчество")
    return errors
