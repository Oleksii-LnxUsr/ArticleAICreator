import random
import asyncio
from g4f.client import AsyncClient
from g4f.Provider import Bing


ARTICLE_GENRES = [
    "popular science",
    "historical fact",
    "fantasy",
    "mystery",
    "adventure",
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
]


def generate_random_time() -> str:
    return random.choice(TIMES + [f"the {random.randint(1, 21)}th century"])


def generate_prompt(level: str, language: str) -> str:
    genre = random.choice(ARTICLE_GENRES)
    country = random.choice(COUNTRIES)
    time = generate_random_time()

    return (
        f"Write an article IN {language} LANGUAGE. Use level {level}. "
        f"About {country} in time {time}, Genre - {genre}. "
        "Length should be 100 words. Use emoji!"
    )


async def generate_article(client: AsyncClient, level: str, language: str) -> str:
    prompt = generate_prompt(level, language)
    response = await client.chat.completions.create(
        model="",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


async def get_articles(language, level) -> list[str]:
    client = AsyncClient(provider=Bing)
    tasks = [generate_article(client, level=level, language=language) for _ in range(3)]
    responses = await asyncio.gather(*tasks)
    articles = [response for response in responses]
    return articles
