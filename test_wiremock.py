import requests


# Настройка WireMock для мока
def setup_wiremock_mock():
    url = "http://localhost:8080/__admin/mappings"
    payload = {
        "requests": {
            "method": "GET",
            "url": "/gismeteo/get/weather",  # мы указываем что если ктото сделате запрос на ручку
            # http://localhost:8080/gismeteo/get/weather
        },
        "response": {
            "status": 200,
            "body": '{"temperature": 25}',
            "headers": {"Content-Type": "application/json"},
        },
    }
    response = requests.post(url, json=payload)


def test_wiremock():
    setup_wiremock_mock()
    response = requests.get("http://localhost:8080/gismeteo/get/weather")
    assert response.status_code == 200
    assert response.json() == {"temperature": 25}
    print("Test passed!")
