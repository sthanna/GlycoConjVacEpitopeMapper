"""Contains useful utility functions."""

import json
import urllib.parse
from pathlib import Path

import requests
# Removed tiktoken import to eliminate OpenAI dependencies

from virtual_lab.constants import (
    DEFAULT_FINETUNING_EPOCHS,
    MODEL_TO_INPUT_PRICE_PER_TOKEN,
    MODEL_TO_OUTPUT_PRICE_PER_TOKEN,
    FINETUNING_MODEL_TO_TRAINING_PRICE_PER_TOKEN,
    PUBMED_TOOL_NAME,
)
from virtual_lab.prompts import format_references


def get_pubmed_central_article(
    pmcid: str, abstract_only: bool = False
) -> tuple[str | None, list[str] | None]:
    """Gets the title and content (abstract or full text) of a PubMed Central article given a PMC ID.

    Note: This only returns main text, ignoring tables, figures, and references.

    :param pmcid: The PMC ID of the article.
    :param abstract_only: Whether to return only the abstract instead of the full text.
    :return: The title and content (abstract or full text of the article as a list of paragraphs)
        or None if the article is not found.
    """
    # Get article from PMC ID in JSON form
    text_url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_JSON/PMC{pmcid}/unicode"
    response = requests.get(text_url)
    response.raise_for_status()

    # Try to parse JSON
    try:
        article = response.json()
    except json.JSONDecodeError:
        return None, None

    # Get document
    document = article[0]["documents"][0]

    # Get title
    title = next(
        passage["text"]
        for passage in document["passages"]
        if passage["infons"]["section_type"] == "TITLE"
    )

    # Get relevant passages
    passages = [
        passage
        for passage in document["passages"]
        if passage["infons"]["type"] in {"abstract", "paragraph"}
    ]

    # Get abstract or full text of article (excluding references)
    if abstract_only:
        passages = [
            passage
            for passage in passages
            if passage["infons"]["section_type"] in ["ABSTRACT"]
        ]
    else:
        passages = [
            passage
            for passage in passages
            if passage["infons"]["section_type"]
            in ["ABSTRACT", "INTRO", "RESULTS", "DISCUSS", "CONCL", "METHODS"]
        ]

    # Get content
    content = [passage["text"] for passage in passages]

    return title, content


def run_pubmed_search(
    query: str, num_articles: int = 3, abstract_only: bool = False
) -> str:
    """Runs a PubMed search, returning the full text of the top matching article.

    :param query: The query to search PubMed with.
    :param num_articles: The number of articles to search for.
    :param abstract_only: Whether to return only the abstract instead of the full text.
    :return: The full text of the top matching article.
    """
    # Print search query
    print(
        f'Searching PubMed Central for {num_articles} articles ({"abstracts" if abstract_only else "full text"}) with query: "{query}"'
    )

    # Perform PubMed Central search for query to get PMC ID
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={urllib.parse.quote_plus(query)}&retmax={2 * num_articles}&retmode=json&sort=relevance"
    response = requests.get(search_url)
    response.raise_for_status()
    pmcids_found = response.json()["esearchresult"]["idlist"]

    # Loop through top articles
    texts = []
    titles = []
    pmcids = []

    for pmcid in pmcids_found:
        # Break if reached desired number of articles
        if len(pmcids) >= num_articles:
            break

        title, content = get_pubmed_central_article(
            pmcid=pmcid,
            abstract_only=abstract_only,
        )

        if title is None:
            continue

        texts.append(f"PMCID = {pmcid}\n\nTitle = {title}\n\n{'\n\n'.join(content)}")
        titles.append(title)
        pmcids.append(pmcid)

    # Print articles found
    article_count = len(texts)

    print(f"Found {article_count:,} articles on PubMed Central")

    # Combine texts
    if article_count == 0:
        combined_text = f'No articles found on PubMed Central for the query "{query}".'
    else:
        combined_text = format_references(
            references=tuple(texts),
            reference_type="paper",
            intro=f'Here are the top {article_count} articles on PubMed Central for the query "{query}":',
        )

    return combined_text

# Removed OpenAI-specific functions: run_tools (Run object), get_messages, async_get_messages

def count_tokens(string: str) -> int:
    """Returns the approximate number of tokens in a text string.
    Note: Using 1 token ~= 4 characters as a rough approximation to avoid OpenAI dependencies.
    """
    return len(string) // 4


def update_token_counts(
    token_counts: dict[str, int],
    discussion: list[dict[str, str]],
    response: str,
) -> None:
    """Updates the token counts (in place) with a discussion and response."""
    new_input_token_count = sum(count_tokens(turn["message"]) for turn in discussion)
    new_output_token_count = count_tokens(response)

    token_counts["input"] += new_input_token_count
    token_counts["output"] += new_output_token_count

    token_counts["max"] = max(
        token_counts["max"], new_input_token_count + new_output_token_count
    )


def count_discussion_tokens(
    discussion: list[dict[str, str]],
) -> dict[str, int]:
    """Counts the number of tokens in a discussion."""
    token_counts = {
        "input": 0,
        "output": 0,
        "max": 0,
    }

    for index, turn in enumerate(discussion):
        if turn["agent"] != "User":
            update_token_counts(
                token_counts=token_counts,
                discussion=discussion[:index],
                response=turn["message"],
            )

    return token_counts

# Helper to load summaries
def get_summary(discussion: list[dict[str, str]]) -> str:
    return discussion[-1]["message"]

def load_summaries(discussion_paths: list[Path]) -> tuple[str, ...]:
    summaries = []
    for discussion_path in discussion_paths:
        with open(discussion_path, "r") as file:
            discussion = json.load(file)
        summaries.append(get_summary(discussion))
    return tuple(summaries)

def save_meeting(
    save_dir: Path, save_name: str, discussion: list[dict[str, str]]
) -> None:
    save_dir.mkdir(parents=True, exist_ok=True)
    with open(save_dir / f"{save_name}.json", "w") as f:
        json.dump(discussion, f, indent=4)
    with open(save_dir / f"{save_name}.md", "w") as file:
        for turn in discussion:
            file.write(f"## {turn['agent']}\n\n{turn['message']}\n\n")
