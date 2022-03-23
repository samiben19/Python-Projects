from Domain.entity_student import Student
from Domain.exceptii import RepoError

class RepositoryStudenti(object):
    def __init__(self):
        """
        Se creaza o lista __elems care contine studentii adaugati
        """
        self._elems = []

    def __len__(self):
        """
        :return: lungimea listei __elems
        """
        return len(self._elems)

    def adauga(self, student):
        """
        Se adauga in lista __elems studentul student daca nu exista deja
        :param student: student de tip Student(id_stud,nume,grup)
        :return: RepoError daca exista deja
        """
        if student in self._elems:
            raise RepoError("Student existent !\n")
        self._elems.append(student)

    def modifica(self, student_nou):
        """
        Se modifica studentul care are ca parametru id_stud
        :param student_nou: student cu id unic dar restul parametrilor schimbati
        :return: RepoError daca nu exista
        """
        if student_nou not in self._elems:
            raise RepoError("Student inexistent !\n")

        for i in range(len(self._elems)):
            if self._elems[i] == student_nou:
                self._elems[i].set_nume(student_nou.get_nume())
                self._elems[i].set_grup(student_nou.get_grup())
                #self.__elems[i] = student_nou
                return

    def sterge(self, id_stud):
        """
        Se sterge studentul care are ca parametru id_stud
        :param id_stud: numar natural unic
        :return: RepoError daca nu exista
        """
        for i in range(len(self._elems)):
            if self._elems[i].get_id_stud() == id_stud:
                del self._elems[i]
                return
        raise RepoError("Student inexistent !\n")

    def cauta_id(self, id_stud):
        """
        :param id_stud: numar natural unic
        :return: studentul care are ca parametru __id_stud = id_stud
        """
        # Best case: elementul cautat este pe prima pozitie
        #       T(n) apartine Teta(1)
        # Worst case: elementul cautat nu se afla deloc in lista
        #       T(n) apartine Teta(n)
        # Average case: for-ul poate fi executat de 1,2,...,len(lista)-1 ori
        #       T(n) = (1+2+..+n-1)/n apartine Teta(n)
        # Per total complexitatea este O(n)

        # Complexitate de memorie: nu utilizeaza memorie aditionala (inplace)
        for student in self._elems:
            if student.get_id_stud() == id_stud:
                return student
        raise RepoError("Student inexistent !\n")

    def __cauta(self, lista, id_stud):
        if len(lista) < 1:
            raise RepoError("Student inexistent !\n")
        el = lista[0]
        if el.get_id_stud() == id_stud:
            return el
        else:
            return self.__cauta(lista[1:],id_stud)

    def cauta_id_recursiv(self, id_stud):
        lista = self._elems[:]
        return self.__cauta(lista, id_stud)

    def get_all(self):
        """
        :return: lista __elems ce contine studentii de tip Student
        """
        return self._elems[:]

class FileRepositoryStudenti(RepositoryStudenti):
    def __init__(self, filename):
        RepositoryStudenti.__init__(self)
        import os
        self.__filename = os.getcwd() + "\\Fisiere\\" + filename
        #self.__citeste_tot_din_fisier()

    def __citeste_tot_din_fisier(self):
        try:
            with open(self.__filename,"r") as f:
                self._elems = []
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line != "":
                        parts = line.split(";")
                        student = Student(int(parts[0]),parts[1],int(parts[2]))
                        self._elems.append(student)
        except FileNotFoundError:
            import os
            if not os.path.exists(os.getcwd() + "\\Fisiere\\"):
                os.mkdir(os.getcwd() + "\\Fisiere\\")
            with open(self.__filename, "w"): pass


    def __adauga_student_in_fisier(self, student):
        with open(self.__filename,"a") as f:
            f.write(str(student.get_id_stud()) + ";" + student.get_nume() + ";" + str(student.get_grup()) + "\n")

    def __scrie_tot_in_fisier(self):
        with open(self.__filename,"w") as f:
            for student in self._elems:
                f.write(str(student.get_id_stud()) + ";" + student.get_nume() + ";" + str(student.get_grup()) + "\n")

    def __len__(self):
        self.__citeste_tot_din_fisier()
        return RepositoryStudenti.__len__(self)

    def adauga(self, student):
        self.__citeste_tot_din_fisier()
        RepositoryStudenti.adauga(self, student)
        self.__adauga_student_in_fisier(student)

    def modifica(self, student_nou):
        self.__citeste_tot_din_fisier()
        RepositoryStudenti.modifica(self, student_nou)
        self.__scrie_tot_in_fisier()

    def sterge(self, id_stud):
        self.__citeste_tot_din_fisier()
        RepositoryStudenti.sterge(self, id_stud)
        self.__scrie_tot_in_fisier()

    def cauta_id(self, id_stud):
        self.__citeste_tot_din_fisier()
        return RepositoryStudenti.cauta_id(self,id_stud)

    def get_all(self):
        self.__citeste_tot_din_fisier()
        return RepositoryStudenti.get_all(self)