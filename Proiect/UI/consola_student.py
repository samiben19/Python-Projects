import string
import random

from Domain.exceptii import ValidError, RepoError, ExitNow


class UI_stud:
    def __init__(self, srv, srv_lab):
        """
        :param srv: ServiceStudenti prelucreaza datele RAW
        """
        self.__srv = srv
        self.__srv_lab = srv_lab
        self.__comenzi = {
            "add":self.__UI_Adauga_student,
            "modif":self.__UI_Modifica_student,
            "del":self.__UI_Sterge_student,
            "caut":self.__UI_Cauta_student_id,
            "list":self.__UI_Afis_studenti,
            "random":self.__UI_Random_studenti,
            "help":self.__help,
            "exit":self.__exit
        }

    def __UI_Adauga_student(self):
        """
        Se citeste un numar natural id_stud, un string nume si un numar natural grup
        Se transmit parametrii catre functia Adauga_student a serviciului srv pentru a adauga studentul intr-un repozitor
        """
        id_stud = int(input("Introduceti ID-ul studentului pe care doriti sa-l adaugati: "))
        nume = input("Introduceti numele studentului: ")
        grup = int(input("Introduceti numarul grupei: "))
        self.__srv.Adauga_student(id_stud, nume, grup)
        print("Student adaugat cu succes !\n")

    def __generare(self):
        id_stud = random.randint(0, 100000)
        #lung_n = random.randint(1, 16)
        #nume = ''.join(random.choices(string.ascii_letters, k=lung_n))
        nume = random.choice(["Sami","Dragos","Cosmin","Andrei","Raul","Paul","Alex","Alexandra","Tabita","Denisa","Rebeca","Larisa","Patricia","David","Ilie","Mihai","George","Diana"])
        grup = random.choice(range(211, 219))
        return id_stud, nume, grup

    def __UI_Random_studenti(self):
        n = int(input("Introduceti cati studenti doriti sa se creeze in mod aleator: "))
        if n <= 0: raise ValueError
        for i in range(n):
            ok = False
            while not ok:
                try:
                    id_stud, nume, grup = self.__generare()
                    self.__srv.Adauga_student(id_stud,nume,grup)
                    ok = True
                except RepoError: continue
        if n == 1:
            print("Student adaugat cu succes !\n")
        else:
            print("Studenti adaugati cu succes !\n")


    def __UI_Modifica_student(self):
        """
        Se citeste un numar natural id_stud, un string nume_nou si un numar natural grup_nou
        Se transmit parametrii catre functia Modifica_student a serviciului srv pentru a modifica un student cu
        ID = id_stud daca exista => nume = nume_nou, grup = grup_nou
        """
        id_stud = int(input("Introduceti ID-ul studentului pe care doriti sa-l modificati: "))
        self.__srv.Cauta_student_id(id_stud)
        nume_nou = input("Introduceti noul nume al studentului: ")
        grup_nou = int(input("Introduceti noul numar al grupei: "))
        self.__srv.Modifica_student(id_stud,nume_nou,grup_nou)
        self.__srv_lab.Update()
        print("Student modificat cu succes !\n")

    def __UI_Sterge_student(self):
        """
        Se citeste un numar natural id_stud
        Se transmite catre functia Sterge_student a serviciului srv pentru a sterge un student cu
        ID = id_stud daca exista
        """
        id_stud = int(input("Introduceti ID-ul studentului pe care doriti il stergeti: "))
        self.__srv.Sterge_student(id_stud)
        self.__srv_lab.Update()
        print("Student sters cu succes !\n")

    def __UI_Cauta_student_id(self):
        """
        Se citeste un numar natural id_stud
        Se transmite catre functia Cauta_student_id a serviciului srv
        pentru a cauta studentul cu ID = id_stud, daca exista se afiseaza detaliile sale
        """
        id_stud = int(input("Introduceti ID-ul studentului pe care doriti sa-l cautati: "))
        student = self.__srv.Cauta_student_id(id_stud)
        print("  Studentul cu ID-ul "+str(id_stud)+" este:\n"+str(student))
        print()

    def __UI_Afis_studenti(self):
        """
        Se afiseaza toata lista de studenti
        """
        studenti = self.__srv.Get_studenti()
        if len(studenti) == 0:
            print("Nu exista studenti in lista !\n")
            return
        print("  Lista de studenti este:\n")
        for student in studenti:
            print(student)
        print()

    def __help(self):
        """
        Functia care afiseaza comenzile care lucreaza cu lista de studenti
        """
        print("  Meniu studenti")
        print("ADD      Adauga un student in lista")
        print("MODIF    Modifica un student din lista dupa ID")
        print("CAUT     Cauta un student dupa ID")
        print("DEL      Sterge un student din lista dupa ID")
        print("LIST     Afiseaza lista de studenti")
        print("RANDOM   Genereaza si adauga in lista studenti random\n")
        print("BACK     Intoarcere la meniul principal")
        print("EXIT     Iesire din program\n")

    def __exit(self):
        raise ExitNow

    def run(self):
        """
        Functia care citeste o comanda cmd, verifica daca este in lista de comenzi,
        iar daca este atunci se realizeaza comanda data, altfel se afiseaza un mesaj corespunzator
        """
        while True:
            cmd = input("C:\Meniu\Studenti>").lower().strip()
            if cmd == "back":
                return
            if cmd in self.__comenzi:
                try:
                    self.__comenzi[cmd]()
                except ValueError:
                    print("EROARE ! Valoare numerica invalida !\n")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            else:
                print("Comanda invalida ! Introduceti 'help' pentru a vedea comenzile.\n")