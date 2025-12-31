import requests

def test_connection(url="https://render.com"):
    """
    Sprawdza połączenie z podanym adresem URL.
    """
    print(f"Testowanie połączenia z {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Rzuć wyjątek dla złych kodów statusu (4xx lub 5xx)
        print(f"Pomyślnie połączono z {url}. Kod statusu: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Nie udało się połączyć z {url}. Błąd: {e}")
        return False

if __name__ == "__main__":
    test_connection()
