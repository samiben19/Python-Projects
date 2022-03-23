from Domain.entity_laborator import Laborator
from Domain.entity_problema import Problema
from Domain.entity_student import Student
from Domain.exceptii import RepoError

class RepositoryLaborator(object):
    def __init__(self):
        """
        Se creaza o lista __elems care contine laboratoarele adaugate
        """
        self._elems = []

    def __len__(self):
        """
        :return: lungimea listei __elems
        """
        return len(self._elems)

    def update(self, new_list):
        self._elems = new_list

    def adauga(self, laborator):
        if laborator in self._elems:
            raise RepoError("Laborator deja asignat studentului cu ID-ul "+str(laborator.get_id_stud())+" !\n")
        self._elems.append(laborator)

    def cauta_id_stud(self, id_stud):
        """
        :param id_stud:
        :return: o lista ce contine toate laboratoarele unui student cu __id_stud = id_stud
        """
        laboratoare = []
        for laborator in self._elems:
            if laborator.get_id_stud() == id_stud:
                laboratoare.append(laborator)
        if len(laboratoare) == 0:
            raise RepoError("Nu exista niciun laborator asignat studentului cu acest ID !\n")
        return laboratoare

    def modifica(self, laborator_nou):
        if laborator_nou not in self._elems:
            raise RepoError("Nu exista acest laborator asignat studentului cu ID-ul dat!\n")
        for i in range(len(self._elems)):
            if self._elems[i] == laborator_nou:
                self._elems[i] = laborator_nou
                #self._elems[i].set_stud(laborator_nou.get_stud())
                #self._elems[i].set_prob(laborator_nou.get_prob())
                #self._elems[i].set_nota(laborator_nou.get_nota())
                return

    def cauta_exact(self, id_stud, nr_pb):
        """
        :param id_stud:
        :param nr_pb:
        :return: laboratorul care are ca student, studentul cu __id_stud = id_stud si ca problema, problema cu __nr_pb = nr_pb
        """
        for lab in self._elems:
            if lab.get_id_stud() == id_stud and lab.get_nr_pb() == nr_pb:
                return lab
        raise RepoError("Studentul dat nu are asignata problema introdusa !\n")

    def sterge(self, id_stud, nr_pb):
        for i in range(len(self._elems)):
            if self._elems[i].get_id_stud() == id_stud and self._elems[i].get_nr_pb() == nr_pb:
                del self._elems[i]
                return
        raise RepoError("Studentul cu ID-ul "+str(id_stud)+" nu are asignata problema "+str(nr_pb)+" !\n")

    def get_all(self):
        """
        :return: lista __elems ce contine laboratorarele de tip Laborator
        """
        return self._elems[:]

class FileRepositoryLaborator(RepositoryLaborator):
    def __init__(self, filename):
        #RepositoryLaborator.__init__(self)
        super().__init__()
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
                        student = Student(int(parts[0]), parts[1], int(parts[2]))
                        problema = Problema(int(parts[3]), parts[4], int(parts[5]))
                        laborator = Laborator(student, problema, float(parts[6]))
                        self._elems.append(laborator)
        except FileNotFoundError:
            import os
            if not os.path.exists(os.getcwd() + "\\Fisiere\\"):
                os.mkdir(os.getcwd() + "\\Fisiere\\")
            with open(self.__filename, "w") as f: pass


    def __adauga_in_fisier(self, laborator):
        with open(self.__filename, "a") as f:
            f.write(str(laborator.get_id_stud()) + ";" + laborator.get_stud().get_nume() + ";" + str(laborator.get_stud().get_grup())\
                    + ";" + str(laborator.get_nr_pb()) + ";" + laborator.get_prob().get_descriere() + ";" + str(laborator.get_prob().get_deadline())\
                    + ";" + str(laborator.get_nota()) + "\n")

    def __scrie_tot_in_fisier(self):
        with open(self.__filename, "w") as f:
            for laborator in self._elems:
                f.write(str(laborator.get_id_stud()) + ";" + laborator.get_stud().get_nume() + ";" + str(laborator.get_stud().get_grup())\
                        + ";" + str(laborator.get_nr_pb()) + ";" + laborator.get_prob().get_descriere() + ";" + str(laborator.get_prob().get_deadline())\
                        + ";" + str(laborator.get_nota()) + "\n")

    def __len__(self):
        self.__citeste_tot_din_fisier()
        return RepositoryLaborator.__len__(self)

    def update(self, new_list):
        #self.__citeste_tot_din_fisier()
        RepositoryLaborator.update(self, new_list)
        self.__scrie_tot_in_fisier()

    def adauga(self, laborator):
        self.__citeste_tot_din_fisier()
        RepositoryLaborator.adauga(self, laborator)
        self.__adauga_in_fisier(laborator)

    def modifica(self, laborator_nou):
        self.__citeste_tot_din_fisier()
        RepositoryLaborator.modifica(self, laborator_nou)
        self.__scrie_tot_in_fisier()

    def cauta_exact(self, id_stud, nr_pb):
        self.__citeste_tot_din_fisier()
        return RepositoryLaborator.cauta_exact(self, id_stud, nr_pb)

    def sterge(self, id_stud, nr_pb):
        self.__citeste_tot_din_fisier()
        RepositoryLaborator.sterge(self, id_stud, nr_pb)
        self.__scrie_tot_in_fisier()

    def get_all(self):
        self.__citeste_tot_din_fisier()
        return RepositoryLaborator.get_all(self)