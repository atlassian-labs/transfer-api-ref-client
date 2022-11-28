def mocked_request_401(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.reason = data
            self.status_code = status_code

        def json(self):
            return self.data

    return MockResponse({}, 401)


def mocked_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.reason = data
            self.status_code = status_code

        def json(self):
            return self.data

    if "/chunk/probe" in args[0]:
        etag = kwargs["json"]["chunks"][0]["hash"]
        size = kwargs["json"]["chunks"][0]["size"]
        return MockResponse({"data": {"results": {etag + "-" + size: {"exists": False}}}}, 200)
    else:
        return MockResponse({}, 201)


def mocked_request_500(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.reason = data
            self.status_code = status_code

        def json(self):
            return self.data

    if "/chunk" in args[0]:
        return MockResponse({}, 500)
    else:
        return MockResponse({"upaload_id"}, 200)
