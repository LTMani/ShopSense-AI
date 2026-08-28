def test_unauthenticated_protected_route_redirects(client):
    res = client.get('/customer/dashboard', follow_redirects=False)
    # Unauthenticated user redirected to login
    assert res.status_code in (302, 401)


def test_customer_cannot_access_seller_portal(auth_customer_client):
    res = auth_customer_client.get('/seller/dashboard')
    assert res.status_code in (302, 403)


def test_seller_can_access_seller_portal(auth_seller_client):
    res = auth_seller_client.get('/seller/dashboard')
    assert res.status_code == 200


def test_security_headers_present(client):
    res = client.get('/')
    assert res.status_code == 200
    assert 'X-Content-Type-Options' in res.headers
    assert res.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in res.headers
