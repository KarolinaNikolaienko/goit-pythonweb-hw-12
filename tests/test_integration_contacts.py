from datetime import date
from src.conf import messages

test_contact={
    "name": "Testname",
    "surname": "Testsurname",
    "email": "test@example.com",
    "phone": "098567457",
    "birthday": str(date(2000,4,23)),
    "additional_data": ""
}
def test_create_contact(client, get_token):
    response = client.post(
        "/api/contacts",
        json=test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == test_contact["name"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_contact(client, get_token):
    response = client.get(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == test_contact["name"]
    assert "id" in data

def test_get_contact_not_found(client, get_token):
    response = client.get(
        "/api/contacts/2", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND

def test_get_contacts(client, get_token):
    response = client.get("/api/contacts", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["name"] == test_contact["name"]
    assert "id" in data[0]

def test_update_contact(client, get_token):
    updated_test_contact = test_contact.copy()
    updated_test_contact["name"] = "new_test_contact"
    response = client.put(
        "/api/contacts/1",
        json=updated_test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == updated_test_contact["name"]
    assert "id" in data
    assert data["id"] == 1

def test_update_contact_not_found(client, get_token):
    updated_test_contact = test_contact.copy()
    updated_test_contact["name"] = "new_test_contact"
    response = client.put(
        "/api/contacts/2",
        json=updated_test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND

def test_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 204, response.text
    data = response.text
    assert data == ''

def test_repeat_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND

