import json
import os
import time
import string
import pyconio
import sortingalgorithms
from sortingalgorithms import CL_SortingAlgorithms
"""--------------------------------------------------------------------------------------------------------
Pytőfi Szótár - Python Program
-----------------------------------------------------------------------------------------------------------
A Pytőfi Szótár egy Python nyelven írt program, amely Petőfi Sándor verseinek
feldolgozásával szógyakorisági szótárt készít. A program képes:
- Versek beolvasására és tárolására (cím, szerző, dátum, szöveg)
- A szöveg feldolgozására: írásjelek eltávolítása, szavak kisbetűsítése
- Szavak keresésére, megtekintésére és gyakoriság szerinti rendezésére
- Rendező algoritmusok (QuickSort, Kupacrendezés, Buborékrendezés, Shell Sort) demonstrálására

Fejlesztő: Gál Vivien Viktória (FKT6WE)        Dátum: 2025-11-16         Verzió: 3.2
-------------------------------------------------------------------------------------------------------"""
# -------------------------------------------------------------------------------
# Szótárkezelő osztály
# -------------------------------------------------------------------------------
class CL_DictionaryManager:
    def __init__(self, json_file="data.json", stopwords_file="stopwords.txt"):
        self.json_file = json_file
        self.stopwords_file = stopwords_file

        self.data = self.DEF_load()

        if "titles" not in self.data:
            self.data["titles"] = []

        if "poems" not in self.data:
            self.data["poems"] = {}

        if "words" not in self.data:
            self.data["words"] = {}

        self.titles = self.data["titles"]
        self.poems = self.data["poems"]
        self.words = self.data["words"]

        self.stopwords = self.DEF_load_stopwords()

        
    def DEF_load(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r", encoding="UTF-8") as f:
                return json.load(f)
        return {} # Ha a fájl nem létezik -> üres szótár

    def DEF_load_stopwords(self):

        if not os.path.exists(self.stopwords_file):
            return []  # üres lista, ha nincs fájl

        # UTF-8-SIG BOM eltávolítással
        with open(self.stopwords_file, "r", encoding="utf-8-sig") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def DEF_add_text(self, text, poem_title, poem_author, poem_date , poem_source):
        extra = "„”–—…"

        # ---- DUPLIKÁCIÓ ELLENŐRZÉS ----
        if poem_title in self.titles:
            pyconio.textcolor(pyconio.LIGHTRED)
            print(f"Hiba: a(z) '{poem_title}' című vers már szerepel!")
            return False

        # Ellenőrzés: csak Petőfi Sándor engedélyezett
        if poem_author != "Petőfi Sándor":
            pyconio.textcolor(pyconio.LIGHTRED)
            print(f"Hiba: csak Petőfi Sándor verseit lehet hozzáadni! (kapott: {poem_author})")
            return False
        
        # ---- ÚJ CÍM BESZÚRÁSA ----
        poem_id = len(self.titles)
        self.titles.append(poem_title)

        # ---- METAADATOK MENTÉSE ----
        self.poems[str(poem_id)] = {
            "title": poem_title,
            "author": poem_author,
            "date": poem_date,
            "source": poem_source
        }


        # ---- SZAVAK FELDOLGOZÁSA ----
        for word in text.split():
            word = word.strip(string.punctuation + extra).lower()

            if word in self.stopwords or not word:
                continue

            if word not in self.words:
                self.words[word] = {"count": 0, "poems": []}

            self.words[word]["count"] += 1

            if poem_id not in self.words[word]["poems"]:
                self.words[word]["poems"].append(poem_id)

        self.DEF_save()
        return True

    def DEF_save(self):
        # mindig frissítsd a self.data-t
        self.data["titles"] = self.titles
        self.data["poems"] = self.poems
        self.data["words"] = self.words

        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
            
    def DEF_search(self, word):
        word = word.lower()
        return self.words.get(word, 0)
            
    def DEF_sort_words(self, items=None):
        if items is None:
            items = list(self.words.items())
            if not items:
                pyconio.textcolor(pyconio.LIGHTRED)
                print("A szótár üres, nincs mit rendezni.")
                return [], "", 0

        sorter = CL_SortingAlgorithms()
        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐")
        print("│         Rendezések            │")
        print("└───────────────────────────────┘")
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("1. QuickSort")
        print("2. HeapSort")
        print("3. BubbleSort")
        print("4. ShellSort")

        try:
            pyconio.textcolor(pyconio.LIGHTCYAN)
            val = int(input("Válaszd ki a rendezési algoritmust (1-4): "))
        except ValueError:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Érvénytelen bemenet!")
            return None, None, None 

        # --------------- FUTÁSIDŐ MÉRÉSE ----------------
        start = time.perf_counter()

        if val == 1:
            sorted_items = sorter.DEF_quick_sort(items)
            alg = "QuickSort"
        elif val == 2:
            sorted_items = sorter.DEF_heap_sort(items)
            alg = "HeapSort"
        elif val == 3:
            sorted_items = sorter.DEF_bubble_sort(items)
            alg = "BubbleSort"
        elif val == 4:
            sorted_items = sorter.DEF_shell_sort(items)
            alg = "ShellSort"
        else:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Hibás választás! QuickSort lesz az alapértelmezett.")
            sorted_items = sorter.DEF_quick_sort(items)
            alg = "QuickSort"

        end = time.perf_counter()
        elapsed = end - start
        # -------------------------------------------------
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print(f"{alg} futási ideje: {elapsed:.6f} másodperc")
        return sorted_items, alg, elapsed

    def DEF_compare_algorithms(self):
        loaded = self.DEF_load() 
        
        if loaded is None:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nincs szótárfájl! Mentsd el előbb egyet!")
            return

        items = list(loaded["words"].items())

        if not items:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("A szótárfájl üres, nincs mit rendezni.")
            return


        sorter = CL_SortingAlgorithms()
        results = []

        algos = [
            ("QuickSort", sorter.DEF_quick_sort),
            ("HeapSort", sorter.DEF_heap_sort),
            ("BubbleSort", sorter.DEF_bubble_sort),
            ("ShellSort", sorter.DEF_shell_sort),
        ]

        for name, func in algos:
            start = time.perf_counter()
            func(list(items))
            end = time.perf_counter()
            results.append((name, end - start))

        max_time = max([t for _, t in results])
        max_stars = 50
        
        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐")
        print("│ Algoritmusok összehasonlítása │")
        print("└───────────────────────────────┘")
        
        pyconio.textcolor(pyconio.LIGHTCYAN)
        for name, elapsed in results:
            stars = int((elapsed / max_time) * max_stars)
            print(f"{name:<10}: {'*' * stars} ({elapsed:.6f}s)")

        pyconio.flush()

    def DEF_export_dictionary(self):
        if not self.words:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("A szótár üres, nincs mit menteni!")
            return

        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐")
        print("│     Szótár mentése fájlba     │")
        print("└───────────────────────────────┘")
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("Válaszd ki milyen rendezéssel szeretnéd rendezni a szótárat")

        #  A user választ rendezési algoritmust
        result = self.DEF_sort_words()
        if result is None or result[0] is None:
            return

        sorted_items, alg, elapsed = result

        if not sorted_items:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nem sikerült rendezni a szótárat.")
            return

        #  A words mezőt új sorrendben építjük újra
        sorted_words_dict = {}
        for word, data in sorted_items:
            sorted_words_dict[word] = {
                "count": data["count"],
                "poems": data["poems"]
            }

        #  Új JSON struktúra a kívánt formátumban
        export_data = {
            "titles": self.titles,
            "poems": self.poems,
            "words": sorted_words_dict
        }

        #  Kiírás JSON-be
        filename = "szotar_export.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=4)

        pyconio.textcolor(pyconio.LIGHTGREEN)
        print(f"A szótár sikeresen elmentve ide: {filename}")
            
    
    def DEF_show_dictionary(self, filename="szotar_export.json"):
        if not os.path.exists(filename):
            pyconio.textcolor(pyconio.LIGHTRED)
            print(f"A '{filename}' fájl nem található!")
            return

        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌──────────────────────────────────────┐")
        print("│         Szótár megtekintése          │")
        print("└──────────────────────────────────────┘")

        # ---- JSON beolvasása ----
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "words" not in data or not data["words"]:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("A fájl nem tartalmaz szavakat.")
            return

        words = data["words"]

        # ---- SZŰRŐ BEKÉRÉSE ----
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("Szeretnél betű szerinti szűrést alkalmazni?")
        print("Nyomj ENTER-t, ha mindent szeretnél látni.")
        prefix = input("Kezdőbetű: ").strip().lower()

        # ---- SZŰRÉS ----
        if prefix:
            filtered_words = {w: info for w, info in words.items() if w.startswith(prefix)}
        else:
            filtered_words = words

        if not filtered_words:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nincs ilyen betűvel kezdődő szó.")
            return

        # ---- Fejléc ----
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print(f"{'Szó':<20} {'Db':>5}   Művek")
        print("-" * 70)

        # ---- Sorok kiírása ----
        for word, info in filtered_words.items():
            count = info["count"]

            titles = []
            for pid in info["poems"]:
                meta = data["poems"].get(str(pid))
                titles.append(meta["title"] if meta else "ismeretlen")

            title_text = ", ".join(titles)
            print(f"{word:<20} {count:>5}   {title_text}")

        pyconio.flush()


    def DEF_load_dictionary_from_file(self, filename="szotar_export.json"):
        if not os.path.exists(filename):
            return None

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data






        
