class Jucator:
    def __init__(self,nume,prenume,inaltime,post):
        self.__nume = nume
        self.__prenume = prenume
        self.__inaltime = inaltime
        self.__post = post

    def get_nume(self): return self.__nume
    def get_prenume(self): return self.__prenume
    def get_inaltime(self): return self.__inaltime
    def get_post(self): return self.__post

    def set_inaltime(self, value): self.__inaltime = value

    def __eq__(self, other):
        return self.__nume.lower() == other.__nume.lower() and self.__prenume.lower() == other.__prenume.lower()

    def __str__(self):
        return self.__nume + " " + self.__prenume + " " + str(self.__inaltime) + " " + self.__post + ""