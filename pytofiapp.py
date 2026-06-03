import os
import json
import time
import string
import pyconio  

from menu import CL_Menu
from poemmanager import CL_PoemManager
from dictionarymanager import CL_DictionaryManager
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
# Fő alkalmazás
# -------------------------------------------------------------------------------
class CL_PytofiApp:
    def __init__(self):
        self.menu = CL_Menu()
        self.poems = CL_PoemManager()
        self.dict = CL_DictionaryManager()

    def DEF_add_poem(self):
        chosen = self.poems.DEF_choose_poem()
        if not chosen:
            return

        content = self.poems.DEF_read_poem(chosen)
        lines = content.splitlines()

        file_title = lines[0].replace("Cím:", "").strip()
        file_author = lines[1].replace("Szerző:", "").strip()
        file_date = lines[2].replace("Dátum:", "").strip()

        text_body = "\n".join(lines[3:])

        success = self.dict.DEF_add_text(text_body, file_title, file_author, file_date , chosen)

        if success:
            pyconio.textcolor(pyconio.LIGHTGREEN)
            print(f"A(z) '{file_title}' sikeresen hozzáadva.")
          
    def DEF_search_word(self):
        pyconio.clrscr()
        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐")
        print("│        Szó keresése           │")
        print("└───────────────────────────────┘")

        loaded = self.dict.DEF_load()

        if not loaded:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nincs betöltött szótár!")
            return

        if not loaded["words"]:      # nincs memóriában szó
            # --- 2) próbáljuk betölteni a JSON-ból ---
            file_data = self.dict.DEF_load_dictionary_from_file()

            if file_data is None:
                pyconio.textcolor(pyconio.LIGHTRED)
                print("Nincs betöltött szótár! Előbb mentsd el vagy töltsd be.")
                return

            # Ha sikerült betölteni, töltsük be memóriába is
            self.dict.loaded_words = file_data["words"]
            self.dict.poems = file_data["poems"]
        else:
            # Ha memóriában volt adat, használjuk azt
            self.dict.loaded_words = loaded["words"]
            self.dict.poems = loaded["poems"]

        # --- keresési módok ---
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("1. Pontos szó keresése")
        print("2. Szórészlet keresése")
        print("3. Kezdőbetű szerinti keresés")

        mode = ""
        while mode not in ("1", "2", "3"):
            mode = input("Keresési mód (1-3): ").strip()

        pyconio.textcolor(pyconio.LIGHTCYAN)
        word = input("Add meg a keresett szót/részletet: ").strip().lower()

        words = self.dict.loaded_words  # gyors hivatkozás
        results = []

        # --- 1. Pontos keresés ---
        if mode == "1":
            if word in words:
                results = [(word, words[word])]
            else:
                results = []

        # --- 2. Szórészlet keresés ---
        elif mode == "2":
            results = [(w, info) for w, info in words.items() if word in w]

        # --- 3. Előtag keresés ---
        elif mode == "3":
            results = [(w, info) for w, info in words.items() if w.startswith(word)]

        # --- Ha nincs találat ---
        if not results:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("\nNincs találat.")
            return

        # --- Találatok kiírása ---
        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│                             KERESÉSI TALÁLATOK                              │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        print(f"| {'Szó':<20} | {'Db':<3} | Művek")
        for w, info in results:
            count = info["count"]

            titles = []
            for pid in info["poems"]:
                meta = self.dict.poems.get(str(pid))
                titles.append(meta["title"] if meta else "ismeretlen")

            title_text = ", ".join(titles)

            print(f"| {w:<20} | {count:<3} | {title_text}")




    def DEF_show_words(self):

        data = self.dict.DEF_import_dictionary()

        if not data:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("A szótár még nincs elmentve!")
            return

        pyconio.textcolor(pyconio.LIGHTCYAN)
        print(f"{'Szó':<20} {'Db':>5}   Művek")
        print("-" * 70)

        for item in data:
            word = item["word"]
            count = item["count"]
            poems = ", ".join(item["poems"])
            print(f"{word:<20} {count:>5}   {poems}")


    def DEF_view_poems(self):
        filename = self.poems.DEF_choose_poem()
        if filename:
            pyconio.textcolor(pyconio.LIGHTBLUE)
            print("┌───────────────────────────────┐")
            print("│    A vers tartalma            │")
            print("└───────────────────────────────┘")
            pyconio.textcolor(pyconio.LIGHTCYAN)
            print(self.poems.DEF_read_poem(filename))


    def DEF_run(self):
        loaded = self.dict.DEF_load_dictionary_from_file()

        if loaded:
            self.dict.loaded_words = loaded["words"]
            self.dict.poems = loaded["poems"]
            pyconio.textcolor(pyconio.LIGHTGREEN)
            print("Szótár automatikusan betöltve.\n")
        else:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nem található szótárfájl).")
            print("Kérlek először mentsd el a szótárat!")
            
        while True:
            self.menu.DEF_show()
            choice = self.menu.DEF_get_choice()
            
            if choice == 1:
                self.DEF_add_poem()
                self.menu.DEF_wait_for_enter()
                
            elif choice == 2:
                loaded = self.dict.DEF_load() 
                
                if "words" not in loaded or not loaded["words"]:
                    pyconio.textcolor(pyconio.LIGHTRED)
                    print("A szótár még nem készült el! Adj hozzá legalább egy verset.")
                    self.menu.DEF_wait_for_enter()
                    continue

                self.dict.loaded_words = loaded["words"]
                self.dict.poems = loaded["poems"]
                
                self.dict.DEF_compare_algorithms()
                self.menu.DEF_wait_for_enter()

            elif choice == 3:
                self.dict.DEF_export_dictionary()
                self.menu.DEF_wait_for_enter()

            elif choice == 4:
                # először betöltjük a json adattárolásra
                loaded = self.dict.DEF_load_dictionary_from_file()

                if loaded is None:
                    pyconio.textcolor(pyconio.LIGHTRED)
                    print("A szótárfájl nem található!")
                    self.menu.DEF_wait_for_enter()
                    continue
                else:
                    # eltároljuk memóriába a kereséshez
                    self.dict.loaded_words = loaded["words"]
                    self.dict.poems = loaded["poems"]  # hogy a keresésnél legyen cím
                    self.dict.titles = loaded["titles"] 
                    pyconio.textcolor(pyconio.LIGHTGREEN)
                    print("Szótár betöltve.")

                # végül KIÍRJUK is (ez az eredeti 4. menüpont funkció)
                self.dict.DEF_show_dictionary()

                self.menu.DEF_wait_for_enter()

            elif choice == 5:
                self.DEF_search_word()
                self.menu.DEF_wait_for_enter()
                continue

            elif choice == 6:
                self.DEF_view_poems()
                self.menu.DEF_wait_for_enter()

            elif choice == 7:
                print("Kilépés")
                break

