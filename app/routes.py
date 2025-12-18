from flask import Blueprint, render_template, request

from app.analysis.book_score import calculate_book_score
from app.scraping.scraper import get_books, get_book_detail
from app.analysis.sentiment import (
    analyze_sentiment,
    split_into_sentences,
    sentiment_to_score
)
from app.analysis.confidence import calculate_confidence

main_routes = Blueprint("main_routes", __name__)

# ======================
# INDEX PAGE
# ======================
@main_routes.route("/")
def index():
    books = get_books()
    if not books:
        return render_template("index.html", books=[], top_positive=[], top_negative=[])

    for book in books:
        book["average_score"] = calculate_book_score(book.get("url", ""))

    scored_books = [
        b for b in books
        if "average_score" in b and b["average_score"] is not None
    ]

    sorted_books = sorted(
        scored_books,
        key=lambda x: x.get("average_score", 0),
        reverse=True
    )

    top_positive = sorted_books[:3]
    top_negative = sorted_books[-3:]

    return render_template(
        "index.html",
        books=books,
        top_positive=top_positive,
        top_negative=top_negative
    )

# ======================
# BOOK DETAIL PAGE
# ======================
@main_routes.route("/book")
def book_detail():
    book_url = request.args.get("url")

    if not book_url:
        return render_template(
            "book_detail.html",
            book={"title": "Hata", "description": "Kitap URL'si eksik."},
            results=[],
            percentages={"Positive": 0, "Neutral": 0, "Negative": 0},
            average_score=0,
            confidence="Low"
        )

    book = get_book_detail(book_url)

    if not book or not book.get("description") or book["description"] == "No description available.":
        return render_template(
            "book_detail.html",
            book={
                "title": book.get("title", "Hata"),
                "description": "Kitap veya açıklaması bulunamadı."
            },
            results=[],
            percentages={"Positive": 0, "Neutral": 0, "Negative": 0},
            average_score=0,
            confidence="Low"
        )

    sentences = split_into_sentences(book["description"])

    results = []
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    scores = []

    for s in sentences:
        sentiment = analyze_sentiment(s)
        score = sentiment_to_score(sentiment)

        results.append({
            "sentence": s,
            "sentiment": sentiment,
            "score": score
        })

        counts[sentiment] += 1
        scores.append(score)

    total = len(results)

    percentages = {
        "Positive": round((counts["Positive"] / total) * 100, 2) if total else 0,
        "Neutral": round((counts["Neutral"] / total) * 100, 2) if total else 0,
        "Negative": round((counts["Negative"] / total) * 100, 2) if total else 0,
    }

    average_score = round(sum(scores) / total, 3) if total else 0

    # ✅ CONFIDENCE HESABI — DOĞRU YER
    confidence = calculate_confidence(results)

    return render_template(
        "book_detail.html",
        book=book,
        results=results,
        percentages=percentages,
        average_score=average_score,
        confidence=confidence
    )
@main_routes.route("/overview")
def overview():
    books = get_books()
    if not books:
        return render_template(
            "overview.html",
            total_books=0,
            avg_score=0,
            positive_count=0,
            neutral_count=0,
            negative_count=0,
            best_book=None,
            worst_book=None
        )

    scored_books = []

    for book in books:
        score = calculate_book_score(book.get("url", ""))
        if score is not None:
            book["average_score"] = score
            scored_books.append(book)

    total_books = len(scored_books)
    avg_score = round(
        sum(b["average_score"] for b in scored_books) / total_books, 3
    ) if total_books else 0

    positive = [b for b in scored_books if b["average_score"] > 0]
    neutral = [b for b in scored_books if b["average_score"] == 0]
    negative = [b for b in scored_books if b["average_score"] < 0]

    best_book = max(scored_books, key=lambda x: x["average_score"], default=None)
    worst_book = min(scored_books, key=lambda x: x["average_score"], default=None)

    return render_template(
        "overview.html",
        total_books=total_books,
        avg_score=avg_score,
        positive_count=len(positive),
        neutral_count=len(neutral),
        negative_count=len(negative),
        best_book=best_book,
        worst_book=worst_book
    )
