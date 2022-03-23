from Controller.servicii import ServiceStudenti, ServiceProbleme, ServiceLaboratoare
from Domain.exceptii import ExitNow
from Domain.validatoare import ValidatorStudent, ValidatorProblema, ValidatorLaborator
from Repository.repo_laborator import RepositoryLaborator, FileRepositoryLaborator
from Repository.repo_problema import RepositoryProbleme, FileRepositoryProbleme
from Repository.repo_student import RepositoryStudenti, FileRepositoryStudenti
from UI.consola_laborator import UI_lab
from UI.consola_problema import UI_pb
from UI.consola_student import UI_stud

class UI_main:
    def __init__(self):
        """
        Initializarea tuturor validatorilor, repozitoarelor, serviciilor si a consolelor
        """
        print("Deltasoft [Version 1.0.1139]\n(c) 2020 Deltasoft Corporation. All rights reserved.\n")
        self.__running_state = True

        if self.__is_fisier():
            self.__repo_stud = FileRepositoryStudenti("studenti.txt")
            self.__repo_pb = FileRepositoryProbleme("probleme.txt")
            self.__repo_lab = FileRepositoryLaborator("laboratoare.txt")
        else:
            self.__repo_stud = RepositoryStudenti()
            self.__repo_pb = RepositoryProbleme()
            self.__repo_lab = RepositoryLaborator()

        # Validatoarele
        self.__valid_stud = ValidatorStudent()
        self.__valid_pb = ValidatorProblema()
        self.__valid_lab = ValidatorLaborator()

        # Serviciile
        self.__srv_stud = ServiceStudenti(self.__valid_stud, self.__repo_stud)
        self.__srv_pb = ServiceProbleme(self.__valid_pb, self.__repo_pb)
        self.__srv_lab = ServiceLaboratoare(self.__valid_lab, self.__repo_stud, self.__repo_pb, self.__repo_lab)

        # Consolele
        self.__consola_stud = UI_stud(self.__srv_stud, self.__srv_lab)
        self.__consola_pb = UI_pb(self.__srv_pb, self.__srv_lab)
        self.__consola_lab = UI_lab(self.__srv_lab)

        # Comenzile principale
        self.__comenzi = {
            "stud": self.__consola_stud.run,
            "st": self.__consola_stud.run,
            "1": self.__consola_stud.run,
            "prob": self.__consola_pb.run,
            "pb": self.__consola_pb.run,
            "2": self.__consola_pb.run,
            "lab": self.__consola_lab.run,
            "3": self.__consola_lab.run,
            "help": self.__help
        }

    def __is_fisier(self):
        while True:
            mod = input("Introduceti modul de lucru (memorie/fisier): ")
            if mod.strip().lower() == "memorie":
                return False
            elif mod.strip().lower() == "fisier":
                return True
            elif mod.strip().lower() == "exit":
                self.__running_state = False

                return
            else:
                print("Mod invalid ! Introduceti 'memorie' sau 'fisier' !")

    def __help(self):
        """
        Functia care afiseaza comenzile principale
        """
        print("  Meniu principal")
        print("STUD     Meniu studenti")
        print("PROB     Meniu probleme")
        print("LAB      Meniu laborator\n")
        print("EXIT     Iesire din program\n")

    def run(self):
        """
        Functia care citeste o comanda cmd, verifica daca este in lista de comenzi,
        iar daca este atunci se realizeaza comanda data, altfel se afiseaza un mesaj corespunzator
        """
        while self.__running_state:
            cmd = input("C:\Meniu>").lower().strip()

            if cmd == "exit" or cmd == "0":
                break
            elif cmd in self.__comenzi:
                try:
                    self.__comenzi[cmd]()
                except ExitNow:
                    break
            else:
                print("Comanda invalida ! Introduceti 'help' pentru a vedea comenzile.\n")
        print("Ati iesit din program !\n")
            # elif cmd == "help":
            #     self.__help()
            # elif cmd == "stud" or cmd == "1":
            #     self.__consola_stud.run()
            # elif cmd == "prob" or cmd == "2":
            #     self.__consola_pb.run()
            # else:
            #     print("Comanda invalida ! Introduceti 'help' pentru a vedea comenzile.\n")