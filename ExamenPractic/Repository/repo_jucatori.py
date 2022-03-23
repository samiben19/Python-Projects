from Entity.jucator_entity import Jucator
from erori import RepoError


class RepoJucatori:
    def __init__(self, filename):
        """

        :param filename: numele fisierului unde se vor stoca datele
        self.__elems este o lista unde se stocheaza in timpul rularii datele, pentru acces mai usor
        """
        self.__filename = filename
        self.__elems = []

    def __citeste_tot_din_fisier(self):
        """
        Functia care citeste tot din fisier
        """
        try:
            with open(self.__filename,"r") as f:
                self.__elems = []
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        parts = line.split(";")
                        jucator = Jucator(parts[0],parts[1],int(parts[2]),parts[3])
                        self.__elems.append(jucator)
        except FileNotFoundError:
            with open(self.__filename,"w"): pass

    def __adauga_in_fisier(self, jucator):
        """
        Functia care adauga jucatorul jucator in fisier
        :param jucator:
        :return:
        """
        with open(self.__filename,"a") as f:
            f.write(jucator.get_nume()+";"+jucator.get_prenume()+";"+str(jucator.get_inaltime())+";"+jucator.get_post()+";\n")

    def __scrie_tot_in_fisier(self):
        """
        Functia care scrie toata lista de jucatori in fisier
        :return:
        """
        with open(self.__filename,"w") as f:
            for jucator in self.__elems:
                f.write(jucator.get_nume()+";"+jucator.get_prenume()+";"+str(jucator.get_inaltime())+";"+jucator.get_post()+";\n")

    def __len__(self):
        """
        Functia care returneaza lungimea listei de jucatori
        :return:
        """
        self.__citeste_tot_din_fisier()
        return len(self.__elems)

    def adauga(self, jucator):
        """
        Functia care incearca sa adauge jucatorul jucator in lista
            Daca acesta exista deja se ridica exceptia RepoError, altfel se adauga
        :param jucator:
        :return:
        """
        self.__citeste_tot_din_fisier()

        if jucator in self.__elems:
            raise RepoError("Jucator deja existent !\n")
        self.__elems.append(jucator)

        self.__adauga_in_fisier(jucator)

    def modifica(self, jucator_nou):
        """
        Functia care incearca modificarea jucatorului jucator_nou
            Daca numele si prenumele jucatorului jucator_nou nu se afla in lista, atunci se ridica exceptia
            RepoError
            altfel se modifica campul inaltime, al jucatorului respectiv
        :param jucator_nou: un jucator de tip Jucator care contine numele si prenumele jucatorului care trebuie modificat si inaltimea noua
        :return:
        """
        self.__citeste_tot_din_fisier()

        if jucator_nou not in self.__elems:
            raise RepoError("Jucator inexistent !\n")

        for i in range(len(self.__elems)):
            if self.__elems[i] == jucator_nou:
                self.__elems[i].set_inaltime(jucator_nou.get_inaltime())
                self.__scrie_tot_in_fisier()
                return

    def cauta_dupa_nume_prenume(self, nume, prenume):
        """
        Functia cauta un jucator dupa nume si prenume (fiind unice)
        :param nume: string
        :param prenume: string
        :return: jucatorul care are ca nume si prenume parametrii: nume, prenume
        """
        self.__citeste_tot_din_fisier()

        for jucator in self.__elems:
            if jucator.get_nume().lower() == nume.lower() and jucator.get_prenume().lower() == prenume.lower():
                return jucator

        raise RepoError("Jucator inexistent !\n")

    def get_all(self):
        """
        Functia returneaza lista de jucatori
        :return: o lista cu toti jucatorii din fisier
        """
        self.__citeste_tot_din_fisier()
        return self.__elems[:]