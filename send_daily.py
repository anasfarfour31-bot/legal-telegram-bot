import os
import json
import urllib.request
import datetime
from zoneinfo import ZoneInfo


BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]

TIMEZONE = "Europe/Istanbul"
POSTS_FILE = "posts.json"


def load_posts():
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def choose_today_post(posts):
    today = datetime.datetime.now(ZoneInfo(TIMEZONE)).date()

    # هذا التاريخ فقط لاختيار ترتيب الأسئلة
    start_date = datetime.date(2026, 1, 1)

    index = (today - start_date).days % len(posts)
    return posts[index]


def build_message(post):
    return f"""⚖️ سؤال اليوم:

{post["question"]}

✅ الإجابة:

{post["answer"]}

تنبيه: هذه معلومة قانونية عامة عن القوانين التركية، وليست استشارة قانونية شخصية. قد تختلف النتيجة حسب تفاصيل كل حالة.
"""


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = json.dumps({
        "chat_id": CHANNEL_ID,
        "text": text
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError(result)

    print("Message sent successfully.")


def main():
    posts = load_posts()

    if not posts:
        raise RuntimeError("posts.json is empty.")

    post = choose_today_post(posts)
    message = build_message(post)
    send_to_telegram(message)


if __name__ == "__main__":
    main()
