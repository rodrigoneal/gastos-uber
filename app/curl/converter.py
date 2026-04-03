import json
import re


class CurlConverterUber:
    def __init__(self, curl: str):
        self.curl = curl
        self.cookies_keys = ["sid", "csid", "jwt-session"]
        self.headers, self.cookies = self.parse_curl(curl)

    def convert_to_data(self):
        with open("data/session.json", "w") as f:
            data = {
                "headers": self.headers,
                "cookies": self.cookies
            }
            json.dump(data, f, indent=4)
        return data

    def parse_curl(self, curl: str):
        headers = {}
        cookies = {}

        matches = re.findall(r"-H '([^']+)'", curl)

        for header in matches:
            key, value = header.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key.lower() == "cookie":
                for item in value.split("; "):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        if k.lower() not in self.cookies_keys:
                            continue
                        cookies[k] = v
        headers = {"x-csrf-token": "x"}
        
        return headers, cookies
