import asyncio
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from crawl4ai import AsyncWebCrawler

# Pages to crawl
URLS = [
    "https://ecom-beauty.netlify.app/",
    "https://ecom-beauty.netlify.app/pages/faq",
    "https://ecom-beauty.netlify.app/pages/about",
    "https://ecom-beauty.netlify.app/pages/products",
    "https://ecom-beauty.netlify.app/pages/policy?policy=shipping",
    "https://ecom-beauty.netlify.app/pages/policy?policy=returns",
    "https://ecom-beauty.netlify.app/pages/policy?policy=payment",
    "https://ecom-beauty.netlify.app/pages/policy?policy=warranty",
    "https://ecom-beauty.netlify.app/pages/blog",
    "https://ecom-beauty.netlify.app/pages/careers",
    "https://ecom-beauty.netlify.app/pages/terms",
    "https://ecom-beauty.netlify.app/pages/contact",
    "https://ecom-beauty.netlify.app/pages/help-center",
    "https://ecom-beauty.netlify.app/pages/categories",
]

# Output directory
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def filename_from_url(url: str) -> str:
    """
    Convert URL into a readable filename.

    Examples:
    /                 -> index.md
    /pages/about      -> about.md
    /pages/help-center -> help-center.md
    /pages/policy?policy=shipping -> policy_shipping.md
    """
    parsed = urlparse(url)

    path = parsed.path.strip("/")

    if not path:
        return "index.md"

    name = path.split("/")[-1]

    if parsed.query:
        params = parse_qs(parsed.query)

        if "policy" in params:
            name = f"policy_{params['policy'][0]}"

    return f"{name}.md"


async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:

        results = await crawler.arun_many(URLS)

        success = 0
        failed = 0

        for result in results:

            print("=" * 80)
            print(result.url)

            if not result.success:
                failed += 1
                print(f"❌ Failed: {result.error_message}")
                continue

            filename = RAW_DIR / filename_from_url(result.url)

            markdown = f"""---
url: {result.url}
crawled_at: {datetime.utcnow().isoformat()}Z
---

{result.markdown}
"""

            filename.write_text(markdown, encoding="utf-8")

            print(f"✅ Saved -> {filename}")

            success += 1

        print("\n" + "=" * 80)
        print(f"Finished!")
        print(f"Successful: {success}")
        print(f"Failed: {failed}")
        print(f"Output folder: {RAW_DIR.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())