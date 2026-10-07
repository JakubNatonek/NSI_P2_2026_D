import time
import json
import functools

def niezawodnosc_logger(log_path="awarie.jsonl"):
    def dekorator(funkcja):
        @functools.wraps(funkcja)
        def wrapper(*args, **kwargs):
            start = time.time()

            try:
                wynik = funkcja(*args, **kwargs)
                return wynik

            except Exception as e:
                wpis = {
                    "timestamp": time.time(),
                    "funkcja": funkcja.__name__,
                    "args": repr(args),
                    "kwargs": repr(kwargs),
                    "typ_bledu": type(e).__name__,
                    "komunikat": str(e),
                    "czas_do_awarii_s": time.time() - start,
                }

                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(wpis) + "\n")

                raise

        return wrapper

    return dekorator


def poprawny_numer(pierwsze_9_cyfr):
    if len(str(pierwsze_9_cyfr)) != 9:
        raise ValueError("Potrzeba dokładnie 9 pierwszych cyfr")

    suma = 0
    for cyfra in str(pierwsze_9_cyfr):
        suma += int(cyfra)

    kontrolna = suma % 10

    return str(pierwsze_9_cyfr) + str(kontrolna)