import os

if __name__ == "__main__":
    destination_mode = os.environ.get("DESTINATION_MODE", "INCREMENTAL")
    destination_name = os.environ["DESTINATION_NAME"]
    