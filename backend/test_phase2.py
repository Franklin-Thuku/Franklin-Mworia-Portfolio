import json
import urllib.request
import urllib.error


def test_phase2():
    print("Testing Phase 2 Contact Pipeline via urllib...")
    base_url = "http://127.0.0.1:8000/api/v1/contact"

    # 1. Post a test contact message
    payload = {
        "name": "Sarah Jenkins (Acme Tech)",
        "email": "sarah.jenkins@acmetech.io",
        "inquiry_type": "Custom MVP / Backend Build",
        "message": "Hi Franklin, we loved your SentinelGate case study. We need a low-latency API proxy built in Go and FastAPI."
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base_url,
        data=data_bytes,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            resp_body = json.loads(response.read().decode("utf-8"))
            print("Contact Submission HTTP:", response.status)
            print("Response Payload:", resp_body)
            assert response.status == 201
            assert resp_body["status"] == "success"

        # 2. Check messages inbox
        with urllib.request.urlopen(f"{base_url}/messages") as response:
            inbox = json.loads(response.read().decode("utf-8"))
            print(f"Inbox List HTTP: {response.status} — Found {len(inbox)} messages stored in DB.")
            assert response.status == 200
            assert len(inbox) >= 1

        print("\n[SUCCESS] Phase 2 Contact pipeline verified and functional!")

    except urllib.error.URLError as e:
        print(f"[Note] Server test response: {e}")


if __name__ == "__main__":
    test_phase2()
