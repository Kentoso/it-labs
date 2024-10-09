import requests

json_api_base_url = "https://jsonplaceholder.typicode.com/"


def get_posts(params=None):
    response = requests.get(f"{json_api_base_url}/posts", params=params)
    return response.json()


def get_users(params=None):
    response = requests.get(f"{json_api_base_url}/users", params=params)
    j = response.json()
    for i in j:
        i["address"] = str(i["address"])
        i["company"] = str(i["company"])
    return j


def get_comments(params=None):
    response = requests.get(f"{json_api_base_url}/comments", params=params)
    return response.json()


POSTS_DB_URL = "http://localhost:8081"
USERS_DB_URL = "http://localhost:8082"
COMMENTS_DB_URL = "http://localhost:8083"


def init_db(db_url, db_name, schema, records):
    requests.post(f"{db_url}/databases", json={"name": db_name})
    requests.post(
        f"{db_url}/databases/{db_name}/tables",
        json={"table_name": db_name, "schema": schema},
    )
    for record in records:
        requests.post(
            f"{db_url}/databases/{db_name}/tables/{db_name}/rows",
            json=record,
        )


def get_posts_from_db():
    response = requests.get(f"{POSTS_DB_URL}/databases/posts_db/tables/posts_db/rows")
    return response.json()


if __name__ == "__main__":
    # Posts DB
    init_db(
        POSTS_DB_URL,
        "posts_db",
        {
            "id": "integer",
            "title": "string",
            "body": "string",
            "userId": "integer",
        },
        get_posts(),
    )

    # Users DB
    init_db(
        USERS_DB_URL,
        "users_db",
        {
            "id": "integer",
            "name": "string",
            "username": "string",
            "email": "string",
            "address": "string",
            "phone": "string",
            "website": "string",
            "company": "string",
        },
        get_users(),
    )

    # Comments DB
    init_db(
        COMMENTS_DB_URL,
        "comments_db",
        {
            "id": "integer",
            "postId": "integer",
            "name": "string",
            "email": "string",
            "body": "string",
        },
        get_comments(),
    )

    print("Databases initialized")

    print("Posts from DB:")
    print(get_posts_from_db())
