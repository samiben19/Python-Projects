from Domain.entity_problema import Problema
from Domain.exceptii import RepoError

class RepositoryProbleme(object):
    def __init__(self):
        """
        Se creaza o lista __elems care contine problemele adaugate
        """
        self._elems = []

    def __len__(self):
        """
        :return: lungimea listei __elems
        """
        return len(self._elems)

    def adauga(self, problema):
        if problema in self._elems:
            raise RepoError("Problema existenta !\n")
        self._elems.append(problema)

    def modifica(self, problema_noua):
        if problema_noua not in self._elems:
            raise RepoError("Problema inexistenta !\n")

        for i in range(len(self._elems)):
            if self._elems[i] == problema_noua:
                self._elems[i].set_descriere(problema_noua.get_descriere())
                self._elems[i].set_deadline(problema_noua.get_deadline())
                #self.__elems[i] = problema_noua
                return

    def sterge(self, nr_pb):
        for i in range(len(self._elems)):
            if self._elems[i].get_nr_pb() == nr_pb:
                del self._elems[i]
                return
        raise RepoError("Problema inexistenta !\n")

    def cauta_nr_pb(self, nr_pb):
        for problema in self._elems:
            if problema.get_nr_pb() == nr_pb:
                return problema
        raise RepoError("Problema inexistenta !\n")

    def __cauta(self, lista, nr_pb):
        if len(lista) < 1:
            raise RepoError("Problema inexistenta !\n")
        el = lista[0]
        if el.get_nr_pb() == nr_pb:
            return el
        else:
            return self.__cauta(lista[1:],nr_pb)

    def cauta_nr_pb_recursiv(self, nr_pb):
        lista = self._elems[:]
        return self.__cauta(lista, nr_pb)

    def get_all(self):
        """
        :return: lista __elems ce contine problemele de tip Problema
        """
        return self._elems[:]

class FileRepositoryProbleme(RepositoryProbleme):
    def __init__(self, filename):
        RepositoryProbleme.__init__(self)
        import os
        self.__filename = os.getcwd() + "\\Fisiere\\" + filename
        #self.__citeste_tot_din_fisier()

    def __citeste_tot_din_fisier(self):
        try:
            with open(self.__filename, "r") as f:
                self._elems = []
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line != "":
                        parts = line.split(";")
                        problema = Problema(int(parts[0]),parts[1],int(parts[2]))
                        self._elems.append(problema)
        except FileNotFoundError:
            import os
            if not os.path.exists(os.getcwd() + "\\Fisiere\\"):
                os.mkdir(os.getcwd() + "\\Fisiere\\")
            with open(self.__filename, "w") as f: pass


    def __adauga_in_fisier(self, problema):
        with open(self.__filename,"a") as f:
            f.write(str(problema.get_nr_pb()) + ";" + problema.get_descriere() + ";" + str(problema.get_deadline()) + "\n")

    def __scrie_tot_in_fisier(self):
        with open(self.__filename,"w") as f:
            for problema in self._elems:
                f.write(str(problema.get_nr_pb()) + ";" + problema.get_descriere() + ";" + str(problema.get_deadline()) + "\n")

    def __len__(self):
        self.__citeste_tot_din_fisier()
        return RepositoryProbleme.__len__(self)

    def adauga(self, problema):
        self.__citeste_tot_din_fisier()
        RepositoryProbleme.adauga(self, problema)
        self.__adauga_in_fisier(problema)

    def modifica(self, problema_noua):
        self.__citeste_tot_din_fisier()
        RepositoryProbleme.modifica(self, problema_noua)
        self.__scrie_tot_in_fisier()

    def sterge(self, nr_pb):
        self.__citeste_tot_din_fisier()
        RepositoryProbleme.sterge(self, nr_pb)
        self.__scrie_tot_in_fisier()

    def cauta_nr_pb(self, nr_pb):
        self.__citeste_tot_din_fisier()
        return RepositoryProbleme.cauta_nr_pb(self, nr_pb)

    def get_all(self):
        self.__citeste_tot_din_fisier()
        return RepositoryProbleme.get_all(self)