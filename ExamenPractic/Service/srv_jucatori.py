from Entity.jucator_entity import Jucator
from erori import ValidError, RepoError


class ServiceJucatori:
    def __init__(self, valid, repo):
        """
        Pentru clasa service se intra cu un validator de jucatori su cu un repository de jucatori
        :param valid:
        :param repo:
        """
        self.__valid = valid
        self.__repo = repo

    def Adauga_jucator(self, nume, prenume, inaltime, post):
        """
        Functia primeste ca parametrii
        :param nume: string
        :param prenume: string
        :param inaltime: int
        :param post: string
        si valideaza parametrii, daca sirurile nu sunt vide, daca post este unul dintre (fundas, pivot, extrema) si inaltimea este strict pozitiva
        si incearca adaugarea jucatorului in lista, daca acesta nu este deja in lista, daca deja este se ridica exceptia RepoError
        """
        jucator = Jucator(nume,prenume,inaltime,post)
        self.__valid.valideaza(jucator)
        self.__repo.adauga(jucator)

    def Modifica_jucator(self, nume, prenume, inaltime_noua):
        """
        Functia primeste ca parametrii
        :param nume: string
        :param prenume: string
        :param inaltime_noua: int
        si ii valideaza, si incearca modificarea jucatorului cu numele si prenumele introduse, daca acesta nu exista se ridica exceptia RepoError
        """
        jucator = Jucator(nume,prenume,inaltime_noua, "fundas")
        self.__valid.valideaza(jucator)
        self.__repo.modifica(jucator)

    def Cerinta3(self):
        """
        Functia ia toti jucatorii din lista, ii sorteaza dupa post crescator si descrescator dupa inaltime iar apoi ia jucatori pana cand s-au pus
        2 fundasi in echipa, 2 extreme si un pivot, sau pana cand s-a terminat lista,
        daca lista 'echipa' nu are 5 jucatori se ridica exceptia ValidError, altfel
        returneaza lista echipa
        :return: o lista, care este o echipa formata din 5 jucatori (2 fundasi, 2 extreme si 1 pivot)
        """
        jucatori = self.__repo.get_all()
        if len(jucatori) < 5:
            raise ValidError("Prea putini jucatori in lista, trebuie minim 5 !\n")

        jucatori.sort(key=lambda x: (x.get_post(), -x.get_inaltime()))
        fundasi = pivot = extrema = 0
        echipa = []
        for el in jucatori:
            if el.get_post().lower() == "fundas" and fundasi < 2:
                fundasi += 1
                echipa.append(el)
            elif el.get_post().lower() == "pivot" and pivot < 1:
                pivot += 1
                echipa.append(el)
            elif el.get_post().lower() == "extrema" and extrema < 2:
                extrema += 1
                echipa.append(el)
            if fundasi == 2 and pivot == 1 and extrema == 2:
                break

        if len(echipa) != 5:
            raise ValidError("Nu s-au gasit destui jucatori din fiecare post !\n")
        return echipa

    def __generare(self):
        """
        Functia genereaza aleator un int, simbolizand inaltimea si un string din lista ["Extrema","Pivot","Fundas"],
        simbolizand postul jucatorului
        :return: int inaltime, string post
        """
        import random
        inaltime = random.randint(1,301)
        post = random.choice(["Extrema","Pivot","Fundas"])
        return inaltime, post

    def Importa(self, nume_fisier):
        """
        Functia ia numele unui fisier deja existent si incearca generarea unor noi jucatori daca acestia nu exista deja in lista,
        adica numele si prenumele lor nu se afla deja in lista de jucatori
        In final se returneaza cati jucatori au fost importati din acel fisier
        :param nume_fisier: string, nume de fisier deja existent
        :return: adaugati, int, simbolizand cati jucatori au fost importati din fisierul nume_fisier
        """
        adaugati = 0
        with open(nume_fisier, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line != "":
                    parts = line.split(" ")
                    parts[1] = parts[1].split("\n")[0]
                    try:
                        self.__repo.cauta_dupa_nume_prenume(parts[0],parts[1])
                    except RepoError:
                        inaltime, post = self.__generare()
                        self.Adauga_jucator(parts[0],parts[1],inaltime,post)
                        adaugati += 1
        return adaugati

    def Get_jucatori(self):
        """
        :return: Lista tuturor jucatorilor
        """
        return self.__repo.get_all()