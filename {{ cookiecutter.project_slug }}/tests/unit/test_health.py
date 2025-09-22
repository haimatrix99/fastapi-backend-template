{% if cookiecutter.include_tests == "y" -%}
def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
{%- endif %}