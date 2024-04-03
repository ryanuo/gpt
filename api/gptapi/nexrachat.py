import requests
import json


class NexraChatAPI:
    def __init__(self, proxies=None):
        self.url = "https://nexra.aryahcr.cc/api/chat/complements"
        self.proxies = proxies
        self.headers = {"Content-Type": "application/json"}

    # You can also use these models: "qwen-b14", "mistral", and "zephyr"
    def send_message(self, messages, model="leo"):
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                data=json.dumps(
                    {
                        "messages": messages,
                        "data": {
                            "system_message": "",
                            "max_tokens": 2048,
                            "temperature": 0.9,
                            "top_p": 0.95,
                            "top_k": 40,
                            "repetition_penalty": 1.1,
                        },
                        "model": model,
                        "stream": False,
                        "markdown": False,
                    }
                ),
                proxies=self.proxies,
            )
            if response.status_code == 200:
                result = None

                count = -1
                for i in range(len(response.text)):
                    if count <= -1:
                        if response.text[i] == "{":
                            count = i
                    else:
                        break

                if count <= -1:
                    err = {
                        "code": 500,
                        "status": False,
                        "error": "INTERNAL_SERVER_ERROR",
                        "message": "general (unknown) error",
                    }
                    result = None
                else:
                    try:
                        js = response.text[count:]
                        js = json.loads(js)
                        if (
                            js is not None
                            and js["code"] is not None
                            and js["code"] == 200
                            and js["status"] is not None
                            and js["status"]
                        ):
                            result = js
                        else:
                            err = js
                    except Exception as e:
                        err = {
                            "code": 500,
                            "status": False,
                            "error": "INTERNAL_SERVER_ERROR",
                            "message": "general (unknown) error",
                        }

                    if result is None:
                        err = json.dumps(err)
                        print(err)
                        return err
                    else:
                        result = json.dumps(result)
                        print(result)
                return result
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(e)
