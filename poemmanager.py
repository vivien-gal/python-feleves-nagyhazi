import os
import pyconio
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
# Verskezelő osztály
# -------------------------------------------------------------------------------
class CL_PoemManager:
    def __init__(self, folder="poems"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

    def DEF_list_poems(self):
        lista = []
        for f in os.listdir(self.folder):
            if f.endswith(".txt"):
                lista.append(f)
        return lista

    def DEF_choose_poem(self):
        poems = self.DEF_list_poems()
        if not poems:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Nincs egyetlen vers sem a 'poems' mappában!")
            return None
        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐")
        print("│        Elérhető versek        │")
        print("└───────────────────────────────┘")
        pyconio.textcolor(pyconio.LIGHTCYAN)
        for i in range(len(poems)):
            print(str(i + 1) + ". " + poems[i])

        try:
            pyconio.textcolor(pyconio.LIGHTCYAN)
            val = int(input("Válaszd ki a verset (1-től kezdve): "))
            if val < 1 or val > len(poems):
                pyconio.textcolor(pyconio.LIGHTRED)
                print("Hibás sorszám!")
                return None
            return poems[val - 1]
        except ValueError:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Csak számot adj meg!")
            return None

    def DEF_read_poem(self, filename):
        path = os.path.join(self.folder, filename)
        with open(path, "r", encoding="UTF-8") as f:
            return f.read()
