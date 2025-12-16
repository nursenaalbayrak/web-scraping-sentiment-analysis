# app/analysis/book_score.py (GÜNCELLENMİŞ)
from app.scraping.scraper import get_book_detail
from app.analysis.sentiment import analyze_sentiment, split_into_sentences, sentiment_to_score
from app.utils.cache import load_scores, save_scores # YENİ IMPORT

def calculate_book_score(book_url):
    # 1. Cache'i yükle
    scores_cache = load_scores()
    
    # 2. Eğer skor cache'te varsa, hemen döndür (PERFORMANS KAZANCI BURADA!)
    if book_url in scores_cache:
        print(f"CACHE: {book_url} için skor cache'ten yüklendi.")
        return scores_cache[book_url]
    
    print(f"SCRAPE/ANALİZ: {book_url} için skor hesaplanıyor...")

    # 3. Eğer cache'te yoksa, scraping ve analizi yap
    try:
        book = get_book_detail(book_url)
    except Exception as e:
        print(f"Hata: Kitap detayları çekilemedi ({book_url}): {e}")
        return 0

    if not book or not book.get("description"):
        final_score = 0
    else:
        sentences = split_into_sentences(book["description"])
        scores = []

        for s in sentences:
            sentiment = analyze_sentiment(s)
            score = sentiment_to_score(sentiment)
            scores.append(score)

        if not scores:
            final_score = 0
        else:
            final_score = round(sum(scores) / len(scores), 3)

    # 4. Yeni hesaplanan skoru cache'e ekle ve dosyaya kaydet
    scores_cache[book_url] = final_score
    save_scores(scores_cache)
    
    return final_score