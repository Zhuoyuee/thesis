from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from pprint import pprint

def fetch_latest_raw_object():
    PROJECT_ID = "85dd0dfa41"
    MODEL_ID = "da6532c773"

    SERVER_URL = "https://app.speckle.systems"

    account = get_default_account()
    client = SpeckleClient(host=SERVER_URL)
    client.authenticate_with_account(account)

    # Get latest version metadata
    model_data = client.model.get_with_versions(project_id=PROJECT_ID, model_id=MODEL_ID)
    version_id = model_data.versions.items[0].id
    print(f"✅ [INFO] Using model version ID: {version_id}")

    version = client.version.get(version_id=version_id, project_id=PROJECT_ID)
    referenced_id = version.referencedObject
    print(f"📦 Resolved root object ID: {referenced_id}")

    # Fetch actual model object tree
    transport = ServerTransport(client=client, stream_id=PROJECT_ID)
    base_obj = client.object.get(referenced_id, transport)

    print("\n🔍 [DEBUG] Resolved object top-level structure:")
    if isinstance(base_obj, dict):
        for k in base_obj.keys():
            print(f"  - {k}")
    else:
        print("⚠️ Unexpected object type:", type(base_obj))

    return base_obj

if __name__ == "__main__":
    obj = fetch_latest_raw_object()
