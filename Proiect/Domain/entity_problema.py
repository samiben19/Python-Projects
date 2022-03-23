class Problema(object):
    def __init__(self, nr_pb, descriere, deadline):
        self.__nr_pb = nr_pb
        self.__descriere = descriere
        self.__deadline = deadline

    def get_nr_pb(self): return self.__nr_pb
    def get_descriere(self): return self.__descriere
    def get_deadline(self): return self.__deadline

    def set_descriere(self, value): self.__descriere = value
    def set_deadline(self, value): self.__deadline = value

    def __str__(self):
        return "Nr. problema: " + str(self.__nr_pb) + ", descriere: " + self.__descriere + ", deadline: " + str(self.__deadline)

    def __eq__(self, other):
        return self.__nr_pb == other.__nr_pb