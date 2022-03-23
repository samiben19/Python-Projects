from erori import ValidError, RepoError


class UI:
    def __init__(self, srv):
        """
        Pentru clasa UI se intra cu un parametru srv de tip ServiceJucatori
        :param srv
        """
        self.__srv = srv
        self.__comenzi = {
            "add":self.__UI_adauga,
            "1": self.__UI_adauga,
            "modif":self.__UI_modifica,
            "2": self.__UI_modifica,
            "echipa":self.__UI_echipa,
            "3": self.__UI_echipa,
            "import":self.__UI_importa,
            "4": self.__UI_importa,
            "afis":self.__UI_afis,
            "5": self.__UI_afis,
            "help": self.__UI_meniu,
            "?": self.__UI_meniu
        }

    def __UI_meniu(self):
        """
        Meniul de comenzi
        :return:
        """
        print("=-=-=-=-=-=-Meniu-=-=-=-=-=-=")
        print("1. ADD - adauga un jucator in lista")
        print("2. MODIF - modifica inaltimea unui jucator din lista")
        print("3. ECHIPA - afiseaza echipa formata din 2 extreme, 2 fundasi si un pivot, cu media inaltimii cea mai mare")
        print("4. IMPORT - importa jucatori dintr-un fisier (deja existent in folderul programului)")
        print("5. AFIS - afiseaza lista tuturor jucatorilor\n")
        print("0. EXIT - iesire din program")

    def __UI_adauga(self):
        """
        Functia care citeste numele, prenumele, inaltimea si postul unui jucator, care mai apoi urmeaza sa apele functia Adauga_jucator
        din service, pentru a adauga in lista jucatorul, daca acesta nu mai exista deja
        :return:
        """
        nume = input("Introduceti numele jucatorului: ").strip()
        prenume = input("Introduceti prenumele jucatorului: ").strip()
        inaltime = int(input("Introduceti inaltimea jucatorului: "))
        post = input("Introduceti postul jucatorului (Fundas, Pivot sau Extrema): ").strip()
        self.__srv.Adauga_jucator(nume,prenume,inaltime,post)
        print("Jucator adaugat cu succes !\n")

    def __UI_modifica(self):
        """
        Functia care citeste numele, prenumele unui jucator si noua inaltime pentru acesta si apeleaza functia din service Modifica care
        incearca sa modifice inaltimea jucatorului daca acesta exista in lista
        :return:
        """
        nume = input("Introduceti numele jucatorului: ").strip()
        prenume = input("Introduceti prenumele jucatorului: ").strip()
        inaltime = int(input("Introduceti noua inaltimea a jucatorului: "))
        self.__srv.Modifica_jucator(nume,prenume,inaltime)
        print("Inaltime modificata cu succes !\n")

    def __UI_echipa(self):
        """
        Functia afiseaza o echipa din 5 jucatori, 2 fundasi, 2 extreme si 1 pivot, acestia impreuna avand media inaltimii cea mai mare dintre
        toti jucatorii din lista
        :return:
        """
        echipa = self.__srv.Cerinta3()
        for el in echipa:
            print(el)
        print()

    def __UI_afis(self):
        """
        Functia afiseaza toti jucatorii din lista
        :return:
        """
        jucatori = self.__srv.Get_jucatori()
        if len(jucatori) == 0:
            print("Nu exista jucatori in lista !\n")
            return
        print("Lista de jucatori este: \n")
        k=1
        for jucator in jucatori:
            print(str(k),end=". ")
            k+=1
            print(jucator)
        print()

    def __UI_importa(self):
        """
        Functia citeste numele unui fisier deja existent si apeleaza functia Importa din service care
        incearca importarea jucatorilor din acest fisier. In final se afiseaza cati jucatori au fost importati din acest fisier
        :return:
        """
        nume_fisier = input("Introduceti numele fisierului deja existent (cu .txt la final): ").strip()
        nr_adaugati = self.__srv.Importa(nume_fisier)
        print("Au fost adaugati " + str(nr_adaugati) + " jucatori !\n")

    def run(self):
        """
        Functia principala in care se citesc comenzile si se prind erorile (ValueError, RepoError, ValidError
            si FileNotFoundError pentru functia import)
        :return:
        """
        while True:
            cmd = input("Introduceti comanda ('help' pentru a vedea lista de comenzi): ").lower().strip()
            if cmd == "exit" or cmd == "0":
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
                except FileNotFoundError:
                    print("Fisier inexistent !\n")
            else:
                print("Comanda invalida !Introduceti 'help' pentru a vedea comenzile\n")