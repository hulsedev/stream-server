username = "testuser"
email = "testuser@example.com"
password = "testpassword"
description = "Test cluster"
name = "Test cluster"
username2 = "testuser2"
password2 = "testpassword2"
email2 = "testuser2@example.com"
task = "text-classification"
data = "test data"


def get_cluster_data():
    return {"name": name, "description": description}


def get_query_data():
    return {"task": task, "data": data}
