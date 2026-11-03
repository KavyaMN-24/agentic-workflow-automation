from app.tools.report_sender import send_report


def test_report_is_not_sent_when_rejected(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "no")

    result = send_report("Monthly sales report")

    assert result["status"] == "rejected"


def test_report_is_sent_when_approved(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "yes")

    result = send_report("Monthly sales report")

    assert result["status"] == "approved"
    assert "Monthly sales report" in capsys.readouterr().out