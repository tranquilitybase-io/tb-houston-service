from pprint import pformat
from tests import pytest_lib
from tb_common.remote.standard_request import Houston


def test_main():
    get_all()
    get()


def get_all():
    print("get_all Tests")

    resp = Houston().get("/applications")

    assert resp.status_code == 200

    resp_json = resp.json()
    for resp_j in resp_json:
        pytest_lib.typestest_application(resp_j)


def get():
    print("get Tests")

    resp = Houston().get("/applications" + "1")

    assert resp.status_code == 200

    resp_json = resp.json()
    print(f"resp_json: {pformat(resp_json)}")
    pytest_lib.typestest_application(resp_json)


if __name__ == "__main__":
    test_main()
