#!/bin/bash
TARGET_TIME="00:01:00"

echo "Oczekuję na $TARGET_TIME..."

while true; do
  CURRENT_TIME=$(date +%H:%M:%S)
  if [[ "$CURRENT_TIME" > "$TARGET_TIME" ]]; then
    echo "Uruchamiam migrację VIS-SOL 2.0..."
    if [ -f "index2.html" ]; then
      mv index2.html index.html
      echo "Migracja zakończona pomyślnie. Plik index.html został zaktualizowany."
    else
      echo "Błąd: Plik index2.html nie został znaleziony."
    fi
    break
  fi
  sleep 1
done
