import requests
import json

# Ваш Access Token
access_token = '' #токен

# ID чату, куди ви хочете надіслати повідомлення
chat_id = '19:fbae889ff53449ac9046eadfddabe097@thread.v2'

# Повідомлення, яке ви хочете надіслати
message = {
    "body": {
        "content": "  ()()\n  ( -.-)\n  o_(\")(\")"
    }
}

# URL для відправлення повідомлення в чат
url = f'https://graph.microsoft.com/v1.0/chats/{chat_id}/messages'

# Заголовки запиту
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Відправляємо запит
response = requests.post(url, headers=headers, data=json.dumps(message))

# Перевірка на успішний запит
if response.status_code == 201:
    print("Message sent successfully!")
else:
    print(f"Error: {response.status_code}, {response.text}")
