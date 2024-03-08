import requests


HOST = "localhost"
PORT = 8000


def create_admin() -> str:
    url = f"http://{HOST}:{PORT}/api/v1/worker"
    payload = {
        "username": "jack",
        "secret": "jack_password",
        "email": "jack@example.com",
        "role": "administrator",
    }

    requests.post(url, json=payload)

    url = f"http://{HOST}:{PORT}/api/v1/token"
    payload = {"username": "jack", "secret": "jack_password"}

    resp = requests.post(url, json=payload)
    return resp.json()["result"]["token"]


def create_developer() -> str:
    url = f"http://{HOST}:{PORT}/api/v1/worker"
    payload = {
        "username": "jess",
        "secret": "jess_password",
        "email": "jess@example.com",
        "role": "developer",
    }

    requests.post(url, json=payload)


def create_token(username: str, secret: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/token"
    payload = {"username": username, "secret": secret}

    resp = requests.post(url, json=payload)
    return resp.json()["result"]["token"]


if __name__ == "__main__":
    create_admin()
    create_developer()

    admin_token = create_token("jack", "jack_password")
    developer_token = create_token("jess", "jess_password")

    print(f"Admin token: {admin_token}")
    print(f"Developer token: {developer_token}")
