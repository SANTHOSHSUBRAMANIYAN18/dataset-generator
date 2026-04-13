import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="AI Dataset Generator ML Service")


class GenerateRequest(BaseModel):
    task: str = Field(min_length=1)
    labels: list[str] = Field(min_length=1)
    samples: int = Field(gt=0)


FAKE_NEWS_EXAMPLES = {
    "fake": [
        "Breaking: Scientists confirm a miracle fruit cures diabetes overnight, but pharmacies are hiding it.",
        "Viral post claims the government will fine people for charging phones after midnight starting next week.",
        "Celebrity doctor says drinking silver-infused water reverses aging in just three days.",
        "Unverified article reports a secret satellite controls weather patterns above major cities.",
        "Online blog alleges schools will replace all textbooks with AI chips by the end of the month."
    ],
    "real": [
        "The city council approved a $12 million road repair plan focused on flood-prone neighborhoods.",
        "Researchers at a public university published a peer-reviewed study on battery recycling methods.",
        "The health ministry issued updated seasonal flu guidance ahead of winter vaccination campaigns.",
        "A regional airline announced new direct flights between Delhi and Singapore starting in July.",
        "The finance department released quarterly data showing slower inflation in food and fuel prices."
    ]
}

SENTIMENT_EXAMPLES = {
    "positive": [
        "The app is fast, easy to use, and solved my problem in minutes.",
        "I loved the packaging and the product quality was better than expected.",
        "Customer support responded quickly and fixed the issue the same day.",
        "This course explained difficult topics clearly and kept me engaged throughout.",
        "The restaurant had fresh food, friendly staff, and a relaxing atmosphere."
    ],
    "negative": [
        "The update made the app crash repeatedly and I lost my work twice.",
        "The product arrived damaged and the return process was frustratingly slow.",
        "Support kept sending generic replies without addressing the actual problem.",
        "The lesson videos were confusing and full of audio issues.",
        "The meal was cold, overpriced, and not worth the wait."
    ],
    "neutral": [
        "The product was delivered on Tuesday and included the listed accessories.",
        "The article describes the company policy changes announced this quarter.",
        "The user completed the sign-up process and viewed the dashboard.",
        "The package contains a charger, user guide, and protective case.",
        "The meeting lasted 30 minutes and covered the planned agenda items."
    ]
}

SPAM_EXAMPLES = {
    "spam": [
        "Congratulations! You have won a free vacation. Click here now to claim your reward.",
        "Limited-time offer: earn $5,000 a week from home with zero experience required.",
        "Urgent account alert: verify your bank details immediately to avoid suspension.",
        "You were selected for an exclusive cash prize. Submit your card number today.",
        "Act fast to unlock premium access and bonus gifts before this link expires."
    ],
    "not spam": [
        "Your appointment with Dr. Mehta is confirmed for Monday at 10:30 AM.",
        "Please find attached the revised project timeline for next week's review.",
        "Reminder: the school will remain closed on Friday for a public holiday.",
        "Your order has been shipped and is expected to arrive by Thursday evening.",
        "Can we reschedule our call to 3 PM? I have a client meeting at noon."
    ]
}

WEATHER_CONDITIONS = [
    "sunny skies",
    "light rain",
    "scattered thunderstorms",
    "humid and cloudy conditions",
    "heavy showers",
    "clear evening skies",
    "moderate rainfall",
    "partly cloudy weather"
]

TEMPERATURE_RANGES = [
    "around 28C",
    "near 31C",
    "between 24C and 29C",
    "around 33C in the afternoon",
    "close to 26C by evening"
]

WEATHER_ALERTS = [
    "Residents are advised to carry umbrellas.",
    "Commuters should expect slow traffic during peak hours.",
    "No major weather disruptions are expected today.",
    "A brief spell of rain is likely later in the day.",
    "Humidity levels may remain high through the evening."
]


def normalize_label(label: str) -> str:
    return label.strip().lower().replace("-", " ")


def infer_task_family(task: str) -> str:
    task_lower = task.lower()

    if "weather" in task_lower or "forecast" in task_lower:
        return "weather"
    if "fake news" in task_lower or "news" in task_lower:
        return "fake_news"
    if "sentiment" in task_lower or "review" in task_lower:
        return "sentiment"
    if "spam" in task_lower or "email" in task_lower or "sms" in task_lower:
        return "spam"
    return "generic"


def generate_fake_news_text(label: str, index: int) -> str:
    normalized = normalize_label(label)
    pool = FAKE_NEWS_EXAMPLES["fake"] if normalized == "fake" else FAKE_NEWS_EXAMPLES["real"]
    return random.choice(pool)


def generate_sentiment_text(label: str, index: int) -> str:
    normalized = normalize_label(label)
    pool = SENTIMENT_EXAMPLES.get(normalized)
    if pool:
        return random.choice(pool)
    return f"The feedback sample #{index} expresses a {label} opinion about the product."


def generate_spam_text(label: str, index: int) -> str:
    normalized = normalize_label(label)
    pool = SPAM_EXAMPLES["spam"] if normalized == "spam" else SPAM_EXAMPLES["not spam"]
    return random.choice(pool)


def generate_weather_text(label: str, index: int) -> str:
    city = label.strip()
    return (
        f"{city} weather update: Expect {random.choice(WEATHER_CONDITIONS)} with temperatures "
        f"{random.choice(TEMPERATURE_RANGES)}. {random.choice(WEATHER_ALERTS)}"
    )


def generate_generic_text(task: str, label: str, index: int) -> str:
    subjects = [
        "customer request",
        "news snippet",
        "support message",
        "product review",
        "social media post"
    ]
    tones = [
        "clear and direct",
        "short and conversational",
        "detailed and formal",
        "casual and realistic"
    ]
    actions = [
        "reports an issue",
        "shares an opinion",
        "asks for help",
        "describes an event",
        "summarizes a situation"
    ]
    return (
        f"This {random.choice(subjects)} is {random.choice(tones)} and {random.choice(actions)} "
        f"for the task '{task}'. It belongs to the label '{label}'. Sample #{index}."
    )


def generate_text(task: str, label: str, index: int) -> str:
    family = infer_task_family(task)

    if family == "fake_news":
        return generate_fake_news_text(label, index)
    if family == "sentiment":
        return generate_sentiment_text(label, index)
    if family == "spam":
        return generate_spam_text(label, index)
    if family == "weather":
        return generate_weather_text(label, index)
    return generate_generic_text(task, label, index)


@app.post("/generate")
def generate_dataset(payload: GenerateRequest):
    task = payload.task.strip()
    cleaned_labels = [label.strip() for label in payload.labels if label.strip()]

    if not task:
        raise HTTPException(status_code=400, detail="Task is required.")

    if not cleaned_labels:
        raise HTTPException(status_code=400, detail="At least one valid label is required.")

    base_count = payload.samples // len(cleaned_labels)
    remainder = payload.samples % len(cleaned_labels)

    dataset = []
    example_number = 1

    for index, label in enumerate(cleaned_labels):
        label_count = base_count + (1 if index < remainder else 0)

        for _ in range(label_count):
            dataset.append(
                {
                    "text": generate_text(task, label, example_number),
                    "label": label,
                }
            )
            example_number += 1

    return {"dataset": dataset}
