USERS = {
    1: {
        "first_name": "Bui",
        "last_name": "Dinh Canh",
        "email": "bdc@vnu.vn",
    },
    2: {
        "first_name": "Do",
        "last_name": "Trung Hieu",
        "email": "dth@vnu.vn",
    },
}


def get_user(uid):
    return USERS.get(uid)