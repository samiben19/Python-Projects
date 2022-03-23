from Domain.entity_laborator import Laborator, MedieDTO
from Domain.entity_student import Student
from Domain.entity_problema import Problema
from Domain.exceptii import RepoError, ValidError, ServError
from Domain.sortari import Sortari


class ServiceStudenti:
    def __init__(self, valid, repo):
        self.__valid = valid
        self.__repo = repo

    def Adauga_student(self, id_stud, nume, grupa):
        """
        Creaza un student de tip Student si incarca sa-l adauge in repozitor
        daca nu mai exista un alt student cu acelasi ID
        :param id_stud: numar natural, unic
        :param nume: string
        :param grupa: numar natural
        :return: RepoError daca exista deja
        """
        student = Student(id_stud, nume, grupa)
        self.__valid.valideaza(student)
        self.__repo.adauga(student)

    def Modifica_student(self, id_stud, nume_nou, grup_noua):
        """
        Modifica studentul cu ID-ul id_stud daca exista
        :param id_stud: numar natural unic
        :param nume_nou: string
        :param grup_noua: numar natural
        :return: RepoError daca nu exista
        """
        student = Student(id_stud, nume_nou, grup_noua)
        self.__valid.valideaza(student)
        self.__repo.modifica(student)

    def Sterge_student(self, id_stud):
        """
        Sterge studentul cu ID-ul id_stud daca exista
        :param id_stud: numar natural unic
        :return: RepoError daca nu exista
        """
        self.__repo.sterge(id_stud)

    def Cauta_student_id(self, id_stud):
        """
        Cauta studentul cu ID-ul id_stud si il returneaza
        :param id_stud: numar natural unic
        :return: student de tip Student daca exista sau RepoError in caz contrar
        """
        return self.__repo.cauta_id(id_stud)

    def Get_studenti(self):
        """
        Returneaza lista tuturor studentilor
        :return: o lista cu elemente de tip Student
        """
        return self.__repo.get_all()


class ServiceProbleme:
    def __init__(self, valid, repo):
        self.__valid = valid
        self.__repo = repo

    def Adauga_problema(self, nr_pb, descriere, deadline):
        """
        Creaza o problema de tip Problema si se incearca adaugarea in repozitor
        daca nu mai exista o alta problma cu acelasi numar
        :param nr_pb: numar natural, unic
        :param descriere: string
        :param deadline: numar natural
        :return: RepoError daca exista deja
        """
        problema = Problema(nr_pb, descriere, deadline)
        self.__valid.valideaza(problema)
        self.__repo.adauga(problema)

    def Modifica_problema(self, nr_pb, descriere_noua, deadline_nou):
        """
        Modifica problema care are ca numar nr_pb daca exista
        :param nr_pb: numar natural unic
        :param descriere_noua: string
        :param deadline_nou: numar natural
        :return: RepoError daca nu exista
        """
        problema = Problema(nr_pb,descriere_noua,deadline_nou)
        self.__valid.valideaza(problema)
        self.__repo.modifica(problema)

    def Sterge_problema(self, nr_pb):
        """
        Sterge problema care are ca numar nr_pb daca exista
        :param nr_pb: numar natural unic
        :return: RepoError daca nu exista
        """
        self.__repo.sterge(nr_pb)

    def Cauta_problema_nr(self, nr_pb):
        """
        Cauta si returneaza daca gaseste problema care are numarul nr_pb
        :param nr_pb: numar natural unic
        :return: problema de tip Problema daca exista sau RepoError in caz contrar
        """
        return self.__repo.cauta_nr_pb(nr_pb)

    def Get_probleme(self):
        """
        Returneaza lista tuturor problemelor
        :return: o lista cu elemente de tip Problema
        """
        return self.__repo.get_all()


class ServiceLaboratoare:
    def __init__(self, valid, repo_stud, repo_prob, repo_lab):
        self.__valid = valid
        self.__repo_stud = repo_stud
        self.__repo_prob = repo_prob
        self.__repo_lab = repo_lab
        self.__sorting = Sortari()
        #self.Update()
        #self.__id_lab = 0

    def __exista(self, id_stud, nr_pb):
        """
        Se cauta studentul cu ID-ul id_stud si problema cu numarul nr_pb
        :param id_stud: numar natural unic
        :param nr_pb: numar natural unic
        :return: stud, prob reprezentand studentul cu ID-ul stud_id si problema cu numarul nr_pb daca exista
                    sau ServError in caz contrar
        """
        exist = ""
        try:
            stud = self.__repo_stud.cauta_id(id_stud)
        except RepoError as re:
            exist += str(re)
        try:
            prob = self.__repo_prob.cauta_nr_pb(nr_pb)
        except RepoError as re:
            exist += str(re)
        if len(exist) > 0: raise ServError(exist)
        return stud, prob

    def Asignare(self, id_stud, nr_pb):
        """
        Apeleaza functia __exista pentru a verifica daca exista studentul cu id-ul dat si problema cu numarul introdus
        Creaza o legatura intre student si problema de tip Laborator, in care initial nota este 0
        :param id_stud: numar natural unic
        :param nr_pb: numar natural unic
        :return: RepoError daca mai exista in lista de laboratoare
        """
        #stud_ver=Student(id_stud,"verif",1)
        #pb_ver=Problema(nr_pb,"verif",1)
        #laborator_ver = Laborator(stud_ver,pb_ver,nota)
        #self.__valid.valideaza(laborator_ver)
        stud, prob = self.__exista(id_stud,nr_pb)
        laborator = Laborator(stud,prob,0)
        self.__valid.valideaza(laborator)
        self.__repo_lab.adauga(laborator)

    def Asignare_grupa(self, grup, nr_pb):
        """
        Asigneaza tuturor studentilor care au ca grupa (grup) problema cu numarul (nr_pb)
        daca acestia nu au deja asignata acea problema
            in caz contrar se asigneaza la restul studentilor dar se ofera si un mesaj pentru a cunoaste
            care studenti aveau deja asignata acea problema
        :param grup: numar natural
        :param nr_pb: numar natural unic
        :return: None in cazul in care s-a asignat sau nu problema studentilor si/sau ServError daca exista studenti cu problema
                    respectiva deja asignata
        """
        prob = self.__repo_prob.cauta_nr_pb(nr_pb)
        exist = ""
        for stud in self.__repo_stud.get_all():
            if stud.get_grup() == grup:
                lab = Laborator(stud,prob,0)
                self.__valid.valideaza(lab)
                try:
                    self.__repo_lab.adauga(lab)
                except RepoError as re:
                    exist += str(re)
        if len(exist) > 0:
            raise ServError(exist)

    def Asignare_nota(self, id_stud, nr_pb, nota):
        """
        Se asigneaza nota unui laborator de tip laborator deja existent, daca nu exista se afiseaza un mesaj corespunzator
        :param id_stud: numar natural unic
        :param nr_pb: numar natural unic
        :param nota: numar real cuprins intre [0,10] (0 inseamna anulare)
        :return: ValidError in cazul in care laboratorul nu este existent adica studentul cu ID-ul id nu are asignata problema cu numarul nr_pb
        """
        #stud_ver = Student(id_stud, "verif", 1)
        #pb_ver = Problema(nr_pb, "verif", 1)
        #laborator_ver = Laborator(stud_ver, pb_ver, nota)
        #self.__valid.valideaza(laborator_ver)
        laborator = self.__repo_lab.cauta_exact(id_stud,nr_pb)
        laborator_cu_nota = Laborator(laborator.get_stud(), laborator.get_prob(), nota)
        self.__valid.valideaza(laborator_cu_nota)
        self.__valid.are_nota(laborator)
        self.__repo_lab.modifica(laborator_cu_nota)
        #laborator.set_nota(nota)

    def Modifica_nota(self, id_stud, nr_pb, nota):
        """
        Se modifica nota unui laborator care exista si are deja nota asignata, daca nu exista sau nu are nota asignata se afiseaza un mesaj corespunzator
        :param id_stud: numar natural unic
        :param nr_pb: numar natural unic
        :param nota: numar real cuprins intre [0,10] (0 inseamna stergerea notei)
        :return: RepoError in cazul in care laboratorul nu este existent adica studentul cu ID-ul id_stud nu are asignata problema cu numarul nr_pb
                    sau in cazul in care nu este o nota asignata unui laborator existent
        """
        laborator = self.__repo_lab.cauta_exact(id_stud,nr_pb)
        laborator_nou = Laborator(laborator.get_stud(), laborator.get_prob(), nota)
        self.__valid.valideaza(laborator_nou)
        try:
            self.__valid.are_nota(laborator)
            raise ServError("Studentul cu ID-ul dat nu are inca nota la problema precizata !\n")
        except ValidError:
            self.__repo_lab.modifica(laborator_nou)

    def Sterge(self, id_stud, nr_pb):
        """
        Sterge un laborator dupa ID-ul unui student id_stud si numarul unei probleme nr_pb
        :param id_stud: numar natural unic
        :param nr_pb: numar natural unic
        :return: RepoError daca nu exista
        """
        self.__exista(id_stud,nr_pb)
        self.__repo_lab.sterge(id_stud,nr_pb)

    def Update(self):
        """
        :param labs: Lista de laboratoare
        Actualizeaza lista de laboratoare, stergand laboratoarele care contin studenti sau probleme inexistente
        """
        labs = self.__repo_lab.get_all()
        for el in reversed(labs):
            try:
                self.__exista(el.get_id_stud(), el.get_nr_pb())
                modif = Laborator(self.__repo_stud.cauta_id(el.get_id_stud()),self.__repo_prob.cauta_nr_pb(el.get_nr_pb()),el.get_nota())
                labs.remove(el)
                labs.append(modif)
            except ServError:
                labs.remove(el)
        self.__repo_lab.update(labs)

    def Nota_la_problema(self, nr_pb):
        """
        :param nr_pb: Numarul problemei
        :return: lista de laboratoare sortate dupa nota descrescator si crescator dupa nume
        """
        self.__repo_prob.cauta_nr_pb(nr_pb)
        labs = self.__repo_lab.get_all()
        self.__sorting.selectionSort(labs,key=lambda x: (-x.get_nota(), x.get_stud().get_nume()))
        #labs.sort(key=lambda x: (-x.get_nota(),x.get_stud().get_nume()))
        for el in labs:
            if el.get_nr_pb() != nr_pb:
                labs.remove(el)

        return labs

    def __Get_note(self):
        """

        :return: un dictionar care are ca si keye id_ul unui student, si o lista de 2 elemente
                pe pozitia 0 se memoreaza suma notelor
                pe pozitia 1 se memoreaza numarul de note
        """
        note = {}
        laboratoare = self.__repo_lab.get_all()
        for lab in laboratoare:
            if lab.get_nota() != 0:
                if lab.get_id_stud() in note:
                    note[lab.get_id_stud()][0] += lab.get_nota()
                    note[lab.get_id_stud()][1] += 1
                else:
                    note[lab.get_id_stud()] = [lab.get_nota(), 1]
        return note

    def __Get_medii(self):
        """
        se calculeaza media elevilor si se incapsuleaza in MedieDTO
        :return: o lista de medii care contine elemente de tip MedieDTO(student,medie)
        """
        note = self.__Get_note()
        medii = []
        for el in note:
            stud = self.__repo_stud.cauta_id(el)
            medie = note[el][0]/note[el][1]
            dto = MedieDTO(stud,medie)
            medii.append(dto)
        return medii

    def __ValidareNota(self, a):
        if a<0 or a>10:
            raise ValidError("Interval invalid !\n")

    def Medie_mai_mica(self, a, b):
        """
        prin intermediul functiei __Get_medii() functia ia mediile tuturor elevilor si le sterge pe cele mai mari decat 5
        :return: o lista cu elemente de tip MedieDTO
        """
        self.__ValidareNota(a)
        self.__ValidareNota(b)
        medii = self.__Get_medii()
        self.__sorting.gnomeSort(medii, key=lambda x: (x.get_medie(), x.get_stud().get_nume()), reversed=True)
        #medii = sorted(medii, key=lambda x: -x.get_medie())
        #medii.sort(key=lambda x: -x.get_medie())
        for el in reversed(medii):
            if el.get_medie() > b or el.get_medie() < a:
                medii.remove(el)
        return medii

    def Get_laboratoare(self):
        """
        Returneaza lista tuturor laboratoarelor
        :return: o lista cu elemente de tip Laborator
        """
        return self.__repo_lab.get_all()
