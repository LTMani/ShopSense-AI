import json


def test_api_products_list(client):
    res = client.get('/api/products/')
    assert res.status_code == 200
    data = res.get_json()
    assert 'products' in data
    assert 'total' in data
    assert data['total'] > 0


def test_api_search_endpoint(client):
    res = client.get('/api/search/?q=laptop')
    assert res.status_code == 200
    data = res.get_json()
    assert 'products' in data
    assert 'extracted_filters' in data


def test_api_copilot_chat(client):
    res = client.post('/api/copilot/chat', json={
        'message': 'Find me a high battery laptop under 70000'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'conversation_id' in data
    assert 'recommended_products' in data


def test_api_comparison(client):
    res = client.get('/api/compare/?ids=1,2')
    assert res.status_code == 200
    data = res.get_json()
    assert 'products' in data


def test_api_system_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data
