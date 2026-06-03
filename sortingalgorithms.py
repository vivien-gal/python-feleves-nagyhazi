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
# Rendezési algoritmusok (magyar ABC szerinti összehasonlítással)
# -------------------------------------------------------------------------------

class CL_SortingAlgorithms:

    # ---------- MAGYAR ÉKEZET NORMALIZÁLÁS ----------
    def normalize_hu(word):
        """
        Magyar ABC szerinti rendezési kulcs előállítása.
        A beépített Unicode-rendezés rossz (á → végére kerül),
        ezért az ékezetes betűket külön súllyal látjuk el.
        """

        table = {
        "a": "a0", "á": "a1",
        "e": "e0", "é": "e1",
        "i": "i0", "í": "i1",
        "o": "o0", "ó": "o1", "ö": "o2", "ő": "o3",
        "u": "u0", "ú": "u1", "ü": "u2", "ű": "u3"
        }

        result = ""
        for ch in word.lower():
            result += table.get(ch, ch)
        return result

    # ---------------------------------------------------------------------------
    # HEAPSORT
    # ---------------------------------------------------------------------------
    def DEF_heap_sort(self, arr):
        arr = list(arr)
        norm = CL_SortingAlgorithms.normalize_hu

        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and norm(arr[l][0]) > norm(arr[largest][0]):
                largest = l
            if r < n and norm(arr[r][0]) > norm(arr[largest][0]):
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(n, largest)

        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(i, 0)

        return arr

    # ---------------------------------------------------------------------------
    # QUICKSORT
    # ---------------------------------------------------------------------------
    def DEF_quick_sort(self, arr):
        arr = list(arr)
        norm = CL_SortingAlgorithms.normalize_hu

        if len(arr) <= 1:
            return arr

        pivot = norm(arr[len(arr) // 2][0])

        left = [x for x in arr if norm(x[0]) < pivot]
        middle = [x for x in arr if norm(x[0]) == pivot]
        right = [x for x in arr if norm(x[0]) > pivot]

        return self.DEF_quick_sort(left) + middle + self.DEF_quick_sort(right)

    # ---------------------------------------------------------------------------
    # BUBBLESORT
    # ---------------------------------------------------------------------------
    def DEF_bubble_sort(self, arr):
        arr = list(arr)
        norm = CL_SortingAlgorithms.normalize_hu
        n = len(arr)

        for i in range(n):
            for j in range(0, n - i - 1):
                if norm(arr[j][0]) > norm(arr[j + 1][0]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    # ---------------------------------------------------------------------------
    # SHELLSORT
    # ---------------------------------------------------------------------------
    def DEF_shell_sort(self, arr):
        arr = list(arr)
        norm = CL_SortingAlgorithms.normalize_hu
        n = len(arr)

        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and norm(arr[j - gap][0]) > norm(temp[0]):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

        return arr
