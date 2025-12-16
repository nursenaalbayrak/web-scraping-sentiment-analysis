from flask import Blueprint, render_template, request, url_for, redirect

from app.analysis.book_score import calculate_book_score 
from app.scraping.scraper import get_books, get_book_detail
from app.analysis.sentiment import (
    analyze_sentiment,
    split_into_sentences,
    sentiment_to_score
)

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/")
def index():
    books = get_books()
    if not books:
        return render_template("index.html", books=[], top_positive=[], top_negative=[])

    for book in books:
        book["average_score"] = calculate_book_score(book.get("url", "")) 
    
    scored_books = [b for b in books if "average_score" in b and b["average_score"] is not None]

    sorted_books = sorted(scored_books, key=lambda x: x.get("average_score", 0), reverse=True)
    
    top_positive = sorted_books[:3]
    top_negative = sorted_books[-3:]

    return render_template(
        "index.html",
        books=books,
        top_positive=top_positive,
        top_negative=top_negative
    )

@main_routes.route("/book")
def book_detail():
    book_url = request.args.get("url")
    
    if not book_url:
         # book_url boşsa, hata sayfasına yönlendir veya hata mesajı göster
        return render_template(
             "book_detail.html",
             book={"title": "Hata", "description": "Kitap URL'si eksik."},
             results=[],
             percentages={"Positive": 0, "Neutral": 0, "Negative": 0},
             average_score=0
         )

    book = get_book_detail(book_url)

    if not book or not book.get("description") or book["description"] == "No description available.":
         return render_template(
             "book_detail.html",
             book={"title": book.get("title", "Hata"), "description": "Kitap veya açıklaması bulunamadı."},
             results=[],
             percentages={"Positive": 0, "Neutral": 0, "Negative": 0},
             average_score=0
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

    return render_template(
        "book_detail.html",
        book=book,
        results=results,
        percentages=percentages,
        average_score=average_score
    )