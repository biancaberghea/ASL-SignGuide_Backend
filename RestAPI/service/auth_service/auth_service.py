from RestAPI.repository.auth_repo import auth_repo


def create_admin():
    auth_repo.create_admin()


def login(email, password):
    return auth_repo.login(email, password)


def sign_up(email, password, username):
    return auth_repo.sign_up(email, password, username)


def refresh_authentication():
    return auth_repo.refresh_authentication()


def get_username():
    return auth_repo.get_username()


def get_user_id():
    return auth_repo.get_user_id()


def get_user_role():
    return auth_repo.get_user_role()
