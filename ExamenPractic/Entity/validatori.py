from erori import ValidError


class ValidatorJucator:
    def valideaza(self, jucator):
        """
        Functia verifica daca jucatorul jucator are
            numele si prenumele diferit de sirul vid,
            inaltimea un numar natural strict pozitiv
            si postul unul dintre urmatoarele stringuri: "fundas", "pivot" sau "extrema"
        :param jucator: un jucator de tip Jucator
        :return: ridica exceptia ValidError daca s-au gasit astfel de erori, sau None in caz contrar
        """
        erori = ""
        if jucator.get_nume() == "":
            erori += "Nume invalid !\n"
        if jucator.get_prenume() == "":
            erori += "Prenume invalid !\n"
        if jucator.get_inaltime() <= 0:
            erori += "Inaltime invalida !\n"
        if jucator.get_post().lower() != "fundas" and jucator.get_post().lower() != "pivot" and jucator.get_post().lower() != "extrema":
            erori += "Post invalid !\n"

        if len(erori) > 0:
            raise ValidError(erori)