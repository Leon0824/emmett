# -*- coding: utf-8 -*-
"""
    tests.http
    ----------------

    Test weppy http module

    :copyright: (c) 2014-2016 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

from helpers import current_ctx
from weppy.http import HTTP, HTTPBytes, HTTPResponse, redirect


def test_http_default():
    http = HTTP(200)

    assert http.encoded_body is b''
    assert http.status_code == 200
    assert http.headers == [(b'Content-Type', b'text/plain')]


def test_http_bytes():
    http = HTTPBytes(200)

    assert http.body == b''
    assert http.status_code == 200
    assert http.headers == [(b'Content-Type', b'text/plain')]


def test_http():
    response = []
    buffer = []

    def start_response(status, headers):
        response[:] = [status, headers]
        return buffer.append

    http = HTTP(200, 'Hello World',
                headers={'X-Test': 'Hello Header'},
                cookies={'cookie_test': 'hello cookie'})

    assert http.encoded_body == b'Hello World'
    assert http.status_code == 200
    assert http.headers == [
        (b'X-Test', b'Hello Header'), (b'Set-Cookie', b'e')]


def test_redirect():
    with current_ctx('/') as ctx:
        try:
            redirect('/redirect', 302)
        except HTTPResponse as http_redirect:
            assert ctx.response.status == 302
            assert http_redirect.status_code == 302
            assert http_redirect.headers == [(b'Location', b'/redirect')]
