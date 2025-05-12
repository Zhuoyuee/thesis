from pprint import pprint

def recurse(obj, depth=0):
    if isinstance(obj, dict):
        if "speckle_type" in obj:
            indent = "  " * depth
            print(f"{indent}{obj['speckle_type']} | keys: {list(obj.keys())}")
        for k, v in obj.items():
            recurse(v, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            recurse(item, depth + 1)

if __name__ == "__main__":
    from speckle_stream import fetch_latest_raw_object
    raw_obj = fetch_latest_raw_object()
    recurse(raw_obj)
