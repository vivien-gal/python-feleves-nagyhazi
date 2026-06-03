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
# Menü osztály
# -------------------------------------------------------------------------------
class CL_Menu:
    def DEF_show(self):
        pyconio.clrscr()
        pyconio.textcolor(pyconio.LIGHTBLUE)
        print("┌───────────────────────────────┐") #(Unicode Block: U+2500–U+257F)
        print("│        Pytőfi Szótár          │")
        print("└───────────────────────────────┘")

        pyconio.textcolor(pyconio.LIGHTCYAN)
        print("  1. Vers hozzáadása")
        print("  2. Rendező algoritmusok összehasonlítása")
        print("  3. Szótár mentése fájlba")
        print("  4. Szótár megtekintése")
        print("  5. Szó keresése")
        print("  6. Versek megtekintése")

        pyconio.textcolor(pyconio.LIGHTRED)
        print("  7. Kilépés")

    def DEF_get_choice(self):
        try:
            pyconio.textcolor(pyconio.LIGHTCYAN)
            choice = int(input("Válassz egy menüpontot (1-7): "))
            if choice not in range(1, 8):
                pyconio.textcolor(pyconio.LIGHTRED)
                print("Hibás választás! Csak 1 és 7 közötti számot adj meg.")
                return None
            return choice
        except ValueError:
            pyconio.textcolor(pyconio.LIGHTRED)
            print("Érvénytelen bemenet! Csak számot adj meg.")
            return None

    def DEF_wait_for_enter(self):
        pyconio.textcolor(pyconio.LIGHTGREEN)
        print("Továbblépéshez nyomj Entert... ", end="")
        input()
