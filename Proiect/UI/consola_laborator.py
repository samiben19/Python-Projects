from Domain.exceptii import ValidError, RepoError, ServError, ExitNow

class UI_lab:
    def __init__(self, srv):
        """
        :param srv: ServiceLaborator prelucreaza datele RAW
        """
        self.__srv = srv
        self.__comenzi = {
            "asig":self.__UI_Asignare,
            "aasig":self.__UI_Asignare_grupa,
            "nota":self.__UI_Asignare_nota,
            "modifn":self.__UI_Modifica_nota,
            "del":self.__UI_Sterge_lab,
            "list":self.__UI_Afis_laboratoare,
            "stat1":self.__UI_Nota_la_problema,
            "stat2":self.__UI_Medie_mai_mica,
            "stat3":self.__UI_Medie_in_interval,
            "help":self.__help,
            "exit":self.__exit
        }

    def __UI_Asignare(self):
        """
        Se citesc doua numare naturale (id_student) si (nr_pb)
        Se transmit parametrii catre functia Asignare a serviciului (srv) pentru a
        asigna studentului cu id-ul (id_student) problema cu numarul (nr_pb)
        """
        id_student = int(input("Introduceti ID-ul studentului caruia doriti sa ii asignati un laborator: "))
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o asignati studentului: "))
        self.__srv.Asignare(id_student,nr_pb)
        print("Asignare realizata cu succes !\n")

    def __UI_Asignare_grupa(self):
        """
        Se citesc doua numare naturale (grup) si (nr_pb)
        Se transmit parametrii catre functia Asignare_grupa a serviciului (srv) pentru a
        asigna tuturor studentilor din (grupa) grup problema cu numarul (nr_pb)
        """
        grup = int(input("Introduceti numarul grupei pentru care doriti sa asignati laboratorul: "))
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o asignati tuturor studentilor din grupa: "))
        self.__srv.Asignare_grupa(grup,nr_pb)
        print("Asignare realizata cu succes !\n")

    def __UI_Asignare_nota(self):
        """
        Se citesc doua numare naturale (id_student) si (nr_pb) si un numar real (nota)
        Se transmit parametrii catre functia Asignare_nota a serviciului (srv) pentru a
        asigna (nota) studentului cu id-ul (id_student), problemei cu numarul (nr_pb)
            daca acesta nu are deja nota
        """
        id_student = int(input("Introduceti ID-ul studentului caruia doriti sa ii asignati un laborator: "))
        nr_pb = int(input("Introduceti numarul problemei pe care doriti sa o asignati studentului: "))
        nota = float(input("Introduceti nota: "))
        self.__srv.Asignare_nota(id_student, nr_pb, nota)
        print("Nota asignata cu succes !\n")

    def __UI_Modifica_nota(self):
        """
        Se citesc doua numare naturale (id_student) si (nr_pb) si un numar real (nota)
        Se transmit parametrii catre functia Modifica_nota a serviciului (srv) pentru a
        modifica (nota) studentului cu id-ul (id_student), problemei cu numarul (nr_pb)
            daca acesta are deja nota
            Functionaza si pe post de stergere nota daca se introduce nota=0
        """
        id_student = int(input("Introduceti ID-ul studentului caruia doriti sa ii modificati nota: "))
        nr_pb = int(input("Introduceti numarul problemei caruia doriti sa ii modificati nota: "))
        nota = float(input("Introduceti nota: "))
        self.__srv.Modifica_nota(id_student,nr_pb,nota)
        print("Modificare realizata cu succes !\n")

    def __UI_Sterge_lab(self):
        """
        Se citesc doua numare naturale (id_student) si (nr_pb)
        Se transmit parametrii catre functia Sterge a serviciului (srv) pentru a
        sterge laboratorul identificat de id-ul studentului (id_student) si de numarul problemei (nr_pb)
        """
        id_student = int(input("Introduceti ID-ul studentului: "))
        nr_pb = int(input("Introduceti numarul problemei: "))
        self.__srv.Sterge(id_student,nr_pb)
        print("Stergere realizata cu succes !\n")

    def __UI_Afis_laboratoare(self):
        """
        Se afiseaza toata lista de laboratoare
        """
        laboratoare = self.__srv.Get_laboratoare()
        if len(laboratoare) == 0:
            print("Nu exista laboratoare in lista !\n")
            return
        for lab in laboratoare:
            print(lab)
        print()

    def __UI_Nota_la_problema(self):
        """
        Se afiseaza lista de studenți și notele lor la o problema de laborator dat, ordonat: alfabetic după nume, după notă.
        """
        nr_pb = int(input("Introduceti numarul problemei pentru care doriti sa se afiseze toate notele: "))
        labs = self.__srv.Nota_la_problema(nr_pb)
        if len(labs) == 0:
            print("Nu exista studenti cu note la problema data !\n")
            return
        for lab in labs:
            if lab.get_nota() != 0:
                print("#"+str(lab.get_id_stud())+" "+lab.get_stud().get_nume()+" "+str(lab.get_nota()))

    def __UI_Medie_mai_mica(self):
        """
        Se afiseaza toti studenții cu media notelor de laborator mai mic decât 5. (nume student și notă)
        """
        medii = self.__srv.Medie_mai_mica(0.0001,5)
        if len(medii) == 0:
            print("Nu exista studenti cu media notelor mai mica decat 5!\n")
            return
        for el in medii:
            print(el)

    def __UI_Medie_in_interval(self):
        """
        Se afiseaza toti studenții cu media notelor de laborator intre a si b. (nume student și notă)
        """
        a = float(input("Introduceti extremitatea inferioara a intervalului: "))
        b = float(input("Introduceti extremitatea superioara a intervalului: "))
        if a > b:
            a,b=b,a
        medii = self.__srv.Medie_mai_mica(a,b)
        if len(medii) == 0:
            print("Nu exista studenti cu media notelor intre "+str(a)+" si "+str(b)+"!\n")
            return
        for el in medii:
            print(el)




    def __help(self):
        """
        Functia care afiseaza comenzile care lucreaza cu lista de laboratoare
        """
        print("  Meniu laboratoare")
        print("ASIG     Asigneaza unui student un laborator")
        print("AASIG    Asigneaza tuturor studentilor dintr-o grupa o problema")
        print("NOTA     Asigneaza nota unui laborator dat")
        print("MODIFN   Modifica nota unui laborator")
        print("DEL      Sterge un laborator in functie de ID si numar problema")
        print("STAT1    Afiseaza notele studentilor la o problema de laborator dat,"
              " ordonate desc dupa nota si cresc dupa nume")
        print("STAT2    Afiseaza toti studentii cu media notelor de laborator mai mica decat 5")
        print("STAT3    Afiseaza toti studentii cu media notelor de laborator intr-un interval dat")
        print("LIST     Afiseaza lista de laboratoare\n")
        print("BACK     Intoarcere la meniul principal")
        print("EXIT     Iesire din program\n")

    def __exit(self):
        raise ExitNow

    def run(self):
        """
        Functia care citeste o comanda (cmd), verifica daca este in lista de comenzi,
        iar daca este atunci se realizeaza comanda data, altfel se afiseaza un mesaj corespunzator
        """
        while True:
            cmd = input("C:\Meniu\Laboratoare>").lower().strip()
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
                except ServError as se:
                    print(se)
            else:
                print("Comanda invalida ! Introduceti 'help' pentru a vedea comenzile.\n")