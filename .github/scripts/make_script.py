import os, feedparser, re, textwrap

RSS_URL = os.getenv("RSS_URL", "https://www.theverge.com/rss/index.xml")
TITLE_PREFIX = os.getenv("TITLE_PREFIX", "خبر داغ تکنولوژی: ")

feed = feedparser.parse(RSS_URL)
entry = feed.entries[0]

title = entry.title
summary = re.sub("<[^<]+?>", "", getattr(entry, "summary", "") or "")
url = getattr(entry, "link", "")

HOOK = f"{TITLE_PREFIX}{title}"
insights = [
    f"این خبر دربارهٔ {title} هست.",
    "نکتهٔ اول: تاثیرش روی کاربرها و کسب‌وکارها.",
    "نکتهٔ دوم: مقایسهٔ کوتاه با رقبای قبلی.",
]
FACT = "یک نکتهٔ سریع: همیشه منبع رسمی را چک کنید."
OUTRO = "اگه مفید بود لایک کن و سابسکرایب یادت نره!"

script = "\n".join([HOOK, *insights, FACT, OUTRO])

os.makedirs("out", exist_ok=True)
open("out/script.txt", "w", encoding="utf-8").write(script)
open("out/title.txt", "w", encoding="utf-8").write(HOOK)
open("out/desc.txt", "w", encoding="utf-8").write(textwrap.dedent(f"""
{HOOK}

{summary[:300]}...
منبع: {url}
#Tech #AI #Shorts
"""))
print("script_ready=1")
