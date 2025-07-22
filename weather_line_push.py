import os
import requests
from datetime import datetime, timedelta, timezone

# 日本時間のタイムゾーンを定義
JST = timezone(timedelta(hours=9))

# 現在の日本時間を取得
now = datetime.now(JST)

# 日付・曜日・時刻を文字列で整形
date_str = now.strftime("%m月%d日（%a）")  # 例: 07月17日（木）
time_str = now.strftime("%H:%M")          # 例: 15:50

# GitHub Secrets から読み込み
CHANNEL_ACCESS_TOKEN = os.environ["LINE_TOKEN"]
TO_USER_ID = os.environ["LINE_USER_ID"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
CITY_NAME = "Himeji"
UNITS = "metric"

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units={UNITS}&lang=ja"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return "天気情報の取得に失敗しました。"

    weather = data['weather'][0]['description']
    temp = round(data['main']['temp'], 1)
    humidity = data['main']['humidity']

    now = datetime.now(JST)  # ← ここを修正
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    date_str = f"{now.month}月{now.day}日（{weekdays[now.weekday()]}）"
    time_str = now.strftime("%H:%M")

    message = f"{date_str} {time_str}時点の姫路の天気は「{weather}」。気温は{temp}℃、湿度は{humidity}%です。"
    return message

def send_push_message(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "to": TO_USER_ID,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }
    res = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=payload
    )
    if res.status_code == 200:
        print("✅ メッセージを送信しました！")
    else:
        print(f"❌ 送信に失敗しました: {res.status_code} - {res.text}")

if __name__ == "__main__":
    weather_message = get_weather()
    print("投稿内容：", weather_message)
    send_push_message(weather_message)
