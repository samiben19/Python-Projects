class Sortari:
    def selectionSort(self, lista, *, key=lambda x:x, reversed=False):
        for i in range(0, len(lista) - 1):
            index = i
            # find the smallest element in the rest of the list
            for j in range(i + 1, len(lista)):
                if reversed:
                    if key(lista[j]) >= key(lista[index]):
                        index = j
                else:
                    if key(lista[j]) <= key(lista[index]):
                        index = j
            if (i < index):
                lista[i],lista[index]=lista[index],lista[i]

    def gnomeSort(self, lista, *, key=lambda x:x, reversed=False):
        index = 0
        while index < len(lista):
            if index == 0 and index + 1 < len(lista):
                index = index + 1
            if reversed:
                if key(lista[index]) <= key(lista[index - 1]):
                    index = index + 1
                else:
                    lista[index], lista[index - 1] = lista[index - 1], lista[index]
                    index = index - 1
            else:
                if key(lista[index]) >= key(lista[index - 1]):
                    index = index + 1
                else:
                    lista[index], lista[index - 1] = lista[index - 1], lista[index]
                    index = index - 1