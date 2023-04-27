import requests, json

message = [{"role" : "user", "content" : "Hello"}]
requestBody = {"model" : "gpt-3.5-turbo",
            "messages" : message,
            "temperature" : 0.5,
            "max_tokens" : 1000,
            "top_p" : 1,
            "frequency_penalty" : 0,
            "presence_penalty" : 0
            }
headers = {"contentType" : "application/json", "Authorization" : "Bearer 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"}
result = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json = requestBody)
response = result.json()
print(response["choices"][0]["message"]["content"])