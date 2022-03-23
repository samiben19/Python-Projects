import random
import string

from Domain.exceptii import ValidError, RepoError, ExitNow


class UI_pb:
    def __init__(self, srv, srv_lab):
        """
        :param srv: ServiceProblema prelucreaza datele RAW
        """
        self.__srv = srv
        self.__srv_lab = srv_lab
        self.__comenzi = {
            "add": self.__UI_Adauga_problema,
            "modif": self.__UI_Modifica_problema,
            "del": self.__UI_Sterge_problema,
            "caut": self.__UI_Cauta_problema,
            "list": self.__UI_Afis_probleme,
            "random": self.__UI_Random_probleme,
            "help": self.__help,
            "exit": self.__exit
        }

    def __UI_Adauga_problema(self):
        """
        Se citeste un numar natural (nr_pb), un string (descriere) si un numar natural (deadline)
        Se transmit parametrii catre functia Adauga_problema a serviciului (srv) pentru
        a adauga problema intr-un repozitor (repo)
        """
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o adaugati: "))
        descriere = input("Introduceti descrierea problemei: ")
        deadline = int(input("Introduceti deadline-ul problemei: "))
        self.__srv.Adauga_problema(nr_pb,descriere,deadline)
        print("Problema adaugata cu succes !\n")

    def __generare(self):
        nr_pb = random.randint(0, 100000)
        lung_d = random.randint(1, 16)
        descriere = ''.join(random.choices(string.ascii_letters, k=lung_d))
        deadline = random.choice(range(1,20))
        return nr_pb,descriere,deadline

    def __UI_Random_probleme(self):
        n = int(input("Introduceti cate probleme doriti sa se creeze in mod aleator: "))
        if n <= 0: raise ValueError
        for i in range(n):
            ok = False
            while not ok:
                try:
                    nr_pb, descriere, deadline = self.__generare()
                    self.__srv.Adauga_problema(nr_pb,descriere,deadline)
                    ok = True
                except RepoError: continue
        if n == 1:
            print("Problema adaugata cu succes !\n")
        else:
            print("Probleme adaugate cu succes !\n")

    def __UI_Modifica_problema(self):
        """
        Se citeste un numar natural id_stud, un string nume_nou si un numar natural grup_nou
        Se transmit parametrii catre functia Modifica_student a serviciului srv pentru a modifica un student cu
        ID = id_stud daca exista => nume = nume_nou, grup = grup_nou
        """
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o modificati: "))
        self.__srv.Cauta_problema_nr(nr_pb)
        descriere_noua = input("Introduceti noua descriere a problemei: ")
        deadline_nou = int(input("Introduceti noul deadline al problemei: "))
        self.__srv.Modifica_problema(nr_pb,descriere_noua,deadline_nou)
        self.__srv_lab.Update()
        print("Problema modificata cu succes !\n")

    def __UI_Sterge_problema(self):
        """
        Se citeste un numar natural nr_pb
        Se transmite catre functia Sterge_student a serviciului srv pentru a sterge un student cu
        ID = id_stud daca exista
        """
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o stergeti: "))
        self.__srv.Sterge_problema(nr_pb)
        self.__srv_lab.Update()
        print("Problema stearsa cu succes !\n")

    def __UI_Cauta_problema(self):
        """
        Se citeste un numar natural nr_pb
        Se transmite catre functia Cauta_problema_nr a serviciului srv
        pentru a cauta problema cu numarul = nr_pb, daca exista se afiseaza detaliile sale
        """
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o cautati: "))
        problema = self.__srv.Cauta_problema_nr(nr_pb)
        print("  Problema cu numarul " + str(nr_pb) + " este:\n" + str(problema))
        print()

    def __UI_Afis_probleme(self):
        """
        Se afiseaza toata lista de probleme
        """
        probleme = self.__srv.Get_probleme()
        if len(probleme) == 0:
            print("Nu exista probleme in lista !\n")
            return
        print("  Lista de probleme este:\n")
        for problema in probleme:
            print(problema)
        print()

    def __help(self):
        """
        Functia care afiseaza comenzile care lucreaza cu lista de probleme
        """
        print("  Meniu probleme")
        print("ADG      Adauga o problema in lista")
        print("MODIF    Modifica o problema din lista dupa NUMAR")
        print("CAUT     Cauta problema dupa NUMAR")
        print("DEL      Sterge o problema din lista dupa NUMAR")
        print("LIST     Afiseaza lista de probleme")
        print("RANDOM   Genereaza si adauga in lista probleme random\n")
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
            cmd = input("C:\Meniu\Probleme>").lower().strip()
            if cmd == "back":
                return
            if cmd in self.__comenzi:
                try:
                    self.__comenzi[cmd]()
                except ValueError:
                    print("EROARE ! Valoare numerica invalida !")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            else:
                print("Comanda invalida ! Introduceti 'help' pentru a vedea comenzile.\n")