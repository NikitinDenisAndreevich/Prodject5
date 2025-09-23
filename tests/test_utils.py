import json

from openpyxl import Workbook

from src.utils import load_csv_transactions, load_excel_transactions, load_json_transactions


def test_load_json_transactions_valid(tmp_path):
    p = tmp_path / "ok.json"
    data = [
        {
            "date": "2023-01-01T00:00:00",
            "description": "Test",
            "state": "EXECUTED",
            "operationAmount": {"amount": "10", "currency": {"name": "Ruble", "code": "RUB"}},
        },
        {
            "date": "2023-01-01T00:00:00",
            "description": "Bad",
            "state": "EXECUTED",
            "operationAmount": "wrong",
        },
    ]
    p.write_text(json.dumps(data), encoding="utf-8")
    res = load_json_transactions(p)
    assert len(res) == 1


def test_load_json_transactions_errors(tmp_path):
    p1 = tmp_path / "bad.json"
    p1.write_text("{not json}", encoding="utf-8")
    assert load_json_transactions(p1) == []

    p2 = tmp_path / "not_list.json"
    p2.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert load_json_transactions(p2) == []


def test_load_csv_transactions_semicolon(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text(
        """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-09-05T11:30:32Z;100;Ruble;RUB;Счет 1;Счет 2;Перевод
2;CANCELED;2023-09-05T11:30:32Z;100;Ruble;RUB;Счет 1;Счет 2;Перевод
""",
        encoding="utf-8",
    )
    res = load_csv_transactions(p)
    assert len(res) == 2
    assert res[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_load_excel_transactions_normalize(tmp_path):
    p = tmp_path / "t.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append([
        "id",
        "state",
        "date",
        "amount",
        "currency_name",
        "currency_code",
        "from",
        "to",
        "description",
    ])
    ws.append([1, "EXECUTED", "2023-01-01T00:00:00", "10", "Ruble", "RUB", "Счет 1", "Счет 2", "Перевод"])
    wb.save(p)

    res = load_excel_transactions(p)
    assert len(res) == 1
    assert res[0]["operationAmount"]["currency"]["code"] == "RUB"
