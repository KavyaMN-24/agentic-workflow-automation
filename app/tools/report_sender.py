from app.core.approval import request_approval


def send_report(report: str) -> dict:
    approved = request_approval(
        "Send the generated business report"
    )

    if not approved:
        return {
            "status": "rejected",
            "message": "Report was not sent."
        }

    # Simulated action only — no external email is sent.
    print("\nSIMULATED REPORT DELIVERY")
    print("=" * 40)
    print(report)

    return {
        "status": "approved",
        "message": "Report delivery simulated successfully."
    }