import requests


HOST = "localhost"
PORT = 8000


def create_admin(username: str, secret: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/workers"
    payload = {
        "username": username,
        "secret": secret,
        "email": f"{username}@example.com",
        "role": "administrator",
    }

    requests.post(url, json=payload)


def create_developer(username: str, secret: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/workers"
    payload = {
        "username": username,
        "secret": secret,
        "email": f"{username}@example.com",
        "role": "developer",
    }

    requests.post(url, json=payload)


def create_token(username: str, secret: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/token"
    payload = {"username": username, "secret": secret}

    resp = requests.post(url, json=payload)
    return resp.json()["result"]["token"]


# if __name__ == "__main__":
#     create_admin()
#     create_developer("jess", "jess_password")
#     create_developer("jess1", "jess1_password")
#     create_developer("jess2", "jess2_password")

#     admin_token = create_token("jack", "jack_password")
#     developer_token = create_token("jess", "jess_password")

#     print(f"Admin token: {admin_token}")
#     print(f"Developer token: {developer_token}")
