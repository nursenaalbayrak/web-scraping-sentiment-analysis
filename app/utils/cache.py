# app/utils/cache.py
import json
import os

# Dosya yolu: data klasörünün projenin kök dizininde olduğunu varsayıyoruz.
CACHE_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'book_scores.json')

def load_scores():
    """Cache dosyasından tüm skorları yükler."""
    if not os.path.exists(CACHE_FILE_PATH):
        return {}
    
    try:
        with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Uyarı: Cache dosyası bozuk. Yeniden oluşturuluyor.")
        return {}
    except Exception as e:
        print(f"Cache yüklenirken hata oluştu: {e}")
        return {}

def save_scores(scores):
    """Skorlar sözlüğünü cache dosyasına kaydeder."""
    try:
        # data klasörünün mevcut olduğundan emin ol
        data_dir = os.path.dirname(CACHE_FILE_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        with open(CACHE_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Cache kaydedilirken hata oluştu: {e}")