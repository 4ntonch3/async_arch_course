import requests


HOST = "localhost"
PORT = 8001


def add_task(token: str, description: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/tasks"
    headers = {"x-token": token}
    payload = {"description": description}

    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()["result"]["id"]


def get_tasks(token: str) -> str:
    url = f"http://{HOST}:{PORT}/api/v1/tasks"
    headers = {"x-token": token}

    resp = requests.get(url, headers=headers)

    return resp.json()["result"]["tasks"]


def reassign_tasks(token: str) -> None:
    url = f"http://{HOST}:{PORT}/api/v1/tasks/reassign"
    headers = {"x-token": token}

    requests.post(url, headers=headers)


def close_task(token: str, task_id: str) -> None:
    url = f"http://{HOST}:{PORT}/api/v1/tasks/{task_id}/close"
    headers = {"x-token": token}
    payload = {"task_id": task_id}

    requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJjNmYyZWQ5Ny05NzJiLTQ3ZmQtYTIyNi1hM2I4NDkyZGJkNjIiLCJ1c2VybmFtZSI6ImphY2siLCJzZWNyZXQiOiIzYTQ5ODVmMzgzYmFiZTRjMzMzMWQ2MTU0YmIxZmNlYjc0MTBmYWZlOTg4NGI5MWNjZDYyM2M1MjAwZmRmY2U4IiwiZW1haWwiOiJqYWNrQGV4YW1wbGUuY29tIiwicm9sZSI6ImFkbWluaXN0cmF0b3IiLCJleHAiOjE3MDk5Nzc4Mzh9.N1GuY02bxkmNXXed6WXK7RmcKa92_1u2pFaEZnA9lDE"
    DEVELOPER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJhZDdmMjMzNS0wYTQzLTRhODEtODc4ZS04NGQ0ZTNhZDBmZmMiLCJ1c2VybmFtZSI6Implc3MiLCJzZWNyZXQiOiJmMjdhZjY1M2YzNThjNWI0Zjc4ZTQ4NmE5NzEzMzQ2YjY0NTM5YzVhMDMxNDBlODYzMzA4ZjYxNmUyZjQzODBlIiwiZW1haWwiOiJqZXNzQGV4YW1wbGUuY29tIiwicm9sZSI6ImRldmVsb3BlciIsImV4cCI6MTcwOTk3NzgzOH0.luToPDR6rGQN5wqxCaf5q31s8O-0ECvGZvYISGMoBRI"
    # task_id = add_task(ADMIN_TOKEN, "Task #1 by Admin")
    # add_task(DEVELOPER_TOKEN, "Task #1 by Developer")

    # print(f"Admin tasks: {get_tasks(ADMIN_TOKEN)}")
    # print(f"Developer tasks: {get_tasks(DEVELOPER_TOKEN)}")

    # print()

    reassign_tasks(ADMIN_TOKEN)
    # print(f"Admin tasks: {get_tasks(ADMIN_TOKEN)}")
    # print(f"Developer tasks: {get_tasks(DEVELOPER_TOKEN)}")

    # print()

    # close_task(DEVELOPER_TOKEN, task_id)
    # print(f"Admin tasks: {get_tasks(ADMIN_TOKEN)}")
    # print(f"Developer tasks: {get_tasks(DEVELOPER_TOKEN)}")
