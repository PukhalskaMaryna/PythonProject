import requests

# Введіть ваш access token
access_token = 'your-access-token'

# URL для отримання чату користувача
url = "https://graph.microsoft.com/v1.0/me/chats"

# Заголовки для запиту
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Виконання GET запиту до Microsoft Graph
response = requests.get(url, headers=headers)

# Перевірка відповіді
if response.status_code == 200:
    chats = response.json()
    print("Chats:", chats)
else:
    print(f"Error fetching chats: {response.status_code}")
