import requests
import json

# Ваш Access Token
# access_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6ImtXSTJzWGNEZWZFc2Vnalh4T3pPWVp5RFdlWUMxMzB4RHRfN2YwYmxjV0kiLCJhbGciOiJSUzI1NiIsIng1dCI6IkpETmFfNGk0cjdGZ2lnTDNzSElsSTN4Vi1JVSIsImtpZCI6IkpETmFfNGk0cjdGZ2lnTDNzSElsSTN4Vi1JVSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zYzg1OGFmYi01ZDE4LTQwZjQtYTFiMi01NTMyNzM0OWJjMTIvIiwiaWF0IjoxNzQxODQ5NTU1LCJuYmYiOjE3NDE4NDk1NTUsImV4cCI6MTc0MTkzNjI1NiwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFVUUF1LzhaQUFBQU1TQ2U2ZXhLRGtaVUE1eUtYdnA2ZXVTY0JwYnhTS0F4Qkg3K1NuWmdhWVUvVG82Y24yRW9rTURCLytnYlNpeDNOd0FVTTd4UVhTckpFK1cyYTR3N1Z3PT0iLCJhbXIiOlsicHdkIiwicnNhIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJkZXZpY2VpZCI6Ijg5OGVjMTFhLTljODEtNDk0My04Y2ZlLWU1MjZiM2Q1NWU1NSIsImZhbWlseV9uYW1lIjoi0J_Rg9GF0LDQu9GM0YHRjNC60LAiLCJnaXZlbl9uYW1lIjoi0JzQsNGA0LjQvdCwIiwiaWR0eXAiOiJ1c2VyIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiIxNzguMTU4LjIzNi4xNjAiLCJuYW1lIjoi0J_Rg9GF0LDQu9GM0YHRjNC60LAg0JzQsNGA0LjQvdCwINCS0LDRgdC40LvRltCy0L3QsCIsIm9pZCI6IjUxNzM3YzY4LTBmZGItNDAyNi1iYWQ5LTI1NDI5ZDJjMDQ1ZCIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS03ODkzMzYwNTgtMTEyMzU2MTk0NS02ODIwMDMzMzAtNDM5MDk3IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAwOUEyMzA3RjEiLCJyaCI6IjEuQVM4QS00cUZQQmhkOUVDaHNsVXljMG04RWdNQUFBQUFBQUFBd0FBQUFBQUFBQUN3QUxJdkFBLiIsInNjcCI6IkNhbGVuZGFycy5SZWFkV3JpdGUgQ2hhdC5SZWFkQmFzaWMgQ2hhdC5SZWFkV3JpdGUgQ2hhdE1lc3NhZ2UuU2VuZCBDb250YWN0cy5SZWFkV3JpdGUgRGlyZWN0b3J5LkFjY2Vzc0FzVXNlci5BbGwgRGlyZWN0b3J5LlJlYWQuQWxsIERpcmVjdG9yeS5SZWFkV3JpdGUuQWxsIEZpbGVzLlJlYWRXcml0ZS5BbGwgR3JvdXAuUmVhZC5BbGwgR3JvdXAuUmVhZFdyaXRlLkFsbCBHcm91cE1lbWJlci5SZWFkLkFsbCBNYWlsLlJlYWRXcml0ZSBOb3Rlcy5SZWFkV3JpdGUuQWxsIG9wZW5pZCBQZW9wbGUuUmVhZCBwcm9maWxlIFNjaGVkdWxlLlJlYWQuQWxsIFNpdGVzLlJlYWRXcml0ZS5BbGwgVGFza3MuUmVhZFdyaXRlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgZW1haWwiLCJzaWQiOiJhNzI5NGJkMS02NmM2LTQwNDAtOTkxMy1iMGM4YTcxYzQ1ZmMiLCJzaWduaW5fc3RhdGUiOlsiZHZjX21uZ2QiLCJkdmNfZG1qZCIsImlua25vd25udHdrIiwia21zaSJdLCJzdWIiOiJsM3pFRGxqOVBKRU9zaDJYYjdWT2RYd2NtUlBCX3N6b3JEOXBkZVZMdW04IiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkVVIiwidGlkIjoiM2M4NThhZmItNWQxOC00MGY0LWExYjItNTUzMjczNDliYzEyIiwidW5pcXVlX25hbWUiOiJwdWtoYWxza0BmdWliLmNvbSIsInVwbiI6InB1a2hhbHNrQGZ1aWIuY29tIiwidXRpIjoiN1I5b3cwb2ZtVW1fUHRKQm5zZ0RBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX2Z0ZCI6Il9nN191QkhWTFNHeWE2d0VwWGpoTXdpLUlJZWxEWXFiWVJvU2VsNV8wTmciLCJ4bXNfaWRyZWwiOiIyOCAxIiwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoiQXA4XzZUdjE1Wi15a2hGc3BvNkFyQW0tdUhpeTVlSUZZTUwyb3QyZENrayJ9LCJ4bXNfdGNkdCI6MTUwNjQxMjE1MX0.Ur-_mh6G9qNSE4ij4Az3njCqTlK5KA7iQSiWx-Uqnjs9afGdtRrqBtt5bJfT2jTE4yVNWEH3dyxymEaqjMkyrUbIRr5EXyKeGRGAFXMcvWhUiElBQZL8vxdN0PS4yYTPGgv3hdVVBs5ElnRTiKjTG7kt931t_j-6dkVW0Obh9FW3w7UP04w1cDnNlC4N2aqaGaCKQ3EF8Pcx9TjjMyEvMzmQZKmdm17IQRrRT5SK193rv7qvVkv4uG4NiDEe-ta_31VnCXFg443ie4q6pONi6UEtGNFiLbh9_JNwJbpgZiArUU7R1XvvV18eyn1Qd63BmH3pbXu2sDQvWQtUdQa6Pw'

# ID чату, куди ви хочете надіслати повідомлення
# chat_id = '19:fbae889ff53449ac9046eadfddabe097@thread.v2'

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
