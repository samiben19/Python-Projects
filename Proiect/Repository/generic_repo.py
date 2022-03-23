from Domain.entity_student import Student
from Domain.exceptii import RepoError

class GenericRepository:
    def __init__(self, filename):
        self.__elems = []
        self.__filename = filename

    def __citeste_tot_din_fisier(self):
        try:
            with open(self.__filename,"r") as f:
                self.__elems = []
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        parts = line.split(";")
                        entitate = 0 #Entity(parts[0],parts[1]....)
                        self.__elems.append(entitate)
        except FileNotFoundError:
            with open(self.__filename,"w"): pass

    def __adauga_in_fisier(self, entitate):
        with open(self.__filename,"a") as f:
            f.write(str(entitate.get_id()) + ";" + ...)

    def __scrie_tot_in_fisier(self):
        with open(self.__filename,"w") as f:
            for el in self.__elems:
                f.write(str(el.get_id()) + ";" + ...)

    def __len__(self):
        self.__citeste_tot_din_fisier()
        return len(self.__elems)

    def adauga(self, entitate):
        self.__citeste_tot_din_fisier()

        if entitate in self.__elems:
            raise RepoError("Entitate existenta !\n")
        self.__elems.append(entitate)

        self.__adauga_in_fisier(entitate)

    def modifica(self, entitate_noua):
        self.__citeste_tot_din_fisier()

        if entitate_noua not in self.__elems:
            raise RepoError("Entitate inexistenta !\n")

        for i in range(len(self.__elems)):
            if self.__elems[i] == entitate_noua:
                self.__elems[i].set_toate(entitate_noua.get_toate())
                return

        self.__scrie_tot_in_fisier()

    def sterge(self, id):
        self.__citeste_tot_din_fisier()

        for i in range(len(self.__elems)):
            if self.__elems[i].get_id() == id:
                del self.__elems[i]
                self.__scrie_tot_in_fisier()
                return

        raise RepoError("Entitate inexistenta !\n")

    def cauta_id(self, id):
        self.__citeste_tot_din_fisier()

        for el in self.__elems:
            if el.get_id() == id:
                return el

        raise RepoError("Entitate inexistenta !\n")

    def get_all(self):
        self.__citeste_tot_din_fisier()
        return self.__elems[:]