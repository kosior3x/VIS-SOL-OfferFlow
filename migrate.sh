#!/bin/bash
# Skrypt do automatycznej migracji o 00:01:00 w Nowy Rok
echo "mv /app/index2.html /app/index.html" | at 00:01 010126
