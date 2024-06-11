import random
import asyncio
from g4f.client import AsyncClient
from g4f.Provider import Bing


ARTICLE_GENRES = [
    "popular science",
    "historical fact",
    "cool fact",
    "fantasy",
    "mystery",
    "adventure",
    "dialogue",
]

COUNTRIES = [
    "USA",
    "Russia",
    "China",
    "Germany",
    "Japan",
    "France",
    "Ukraine",
    "Greece",
]

TIMES = [
    "the Middle Ages",
    "the future",
    "World War II",
    "modern day",
    f"the {random.randint(1, 21)}th century",
]


def generate_prompt(level: str, language: str) -> str:
    """Generate a prompt for article generation based on the given level and language"""
    genre = random.choice(ARTICLE_GENRES)
    country = random.choice(COUNTRIES)
    time = random.choice(TIMES)

    beginning = f"Write an article IN {language} LANGUAGE. Use level {level}. "
    theme = f"random object that people use in country {country} at time {time} "
    genre = f"article should be in genre {genre} "
    end = "Length should be 100 words. Use emoji!"

    return f"{beginning}{theme}{genre}{end}"


async def generate_article(client: AsyncClient, level: str, language: str) -> str:
    """Generate a single article based on the given level and language"""
    prompt = generate_prompt(level, language)
    response = await client.chat.completions.create(
        model="",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


async def get_articles(language, level) -> list[str]:
    """Generate a list of articles asynchronously."""
    client = AsyncClient(provider=Bing)
    tasks = [generate_article(client, level=level, language=language) for _ in range(3)]
    responses = await asyncio.gather(*tasks)
    articles = [response for response in responses]
    return articles
