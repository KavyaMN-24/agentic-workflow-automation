from app.core.approval import request_approval


def test_approval_granted(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "yes")

    assert request_approval("Send business report") is True


def test_approval_rejected(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "no")

    assert request_approval("Send business report") is False


def test_approval_rejects_unexpected_response(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "maybe")

    assert request_approval("Send business report") is False