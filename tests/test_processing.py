import pytest

from src.processing import process_bank_search, process_bank_operations, filter_by_state, sort_by_date

def test_process_bank_search():
    data = [
        {'description': 'Payment for services'},
        {'description': 'Monthly subscription'}
    ]
    assert len(process_bank_search(data, 'payment')) == 1

def test_process_bank_operations():
    data = [
        {'description': 'Transfer'},
        {'description': 'Transfer'},
        {'description': 'Payment'}
    ]
    assert process_bank_operations(data, ['Transfer', 'Payment']) == {
        'Transfer': 2,
        'Payment': 1
    }

@pytest.fixture
def test_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]


@pytest.mark.parametrize(
    "state, expected_result",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
            ]
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
            ]
        )
    ]
)
def test_filter_by_state(test_data, state, expected_result):
    assert filter_by_state(test_data, state) == expected_result


def test_filter_by_state_default(test_data):
    assert filter_by_state(test_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]


@pytest.mark.parametrize(
    "reverse, expected_result",
    [
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
            ]
        ),
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
            ]
        )
    ]
)
def test_sort_by_date(test_data, reverse, expected_result):
    sorted_data = sort_by_date(test_data, reverse=reverse)
    assert sorted_data == expected_result
