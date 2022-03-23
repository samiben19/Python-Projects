# class Laborator:
#     def __init__(self,id_stud,nr_pb,nota):
#         self.__id_stud = id_stud
#         self.__nr_pb = nr_pb
#         self.__nota = nota
#
#     def get_id_stud(self): return self.__id_stud
#     def get_nr_pb(self): return self.__nr_pb
#     def get_nota(self): return self.__nota
#
#     def set_nota(self): return self.__nota
#
#     def __str__(self):
#         if self.__nota == 0:
#             return "Studentul cu ID-ul " + str(self.__id_stud) + " nu a primit la laboratorul numarul " + str(self.__nr_pb) + " nota. "
#         else:
#             return "Studentul cu ID-ul " + str(self.__id_stud) + " are la laboratorul numarul " + str(self.__nr_pb) + " nota: " + str(self.__nota)
#
#     def __eq__(self, other):
#         return self.__id_stud == other.__id_stud and  self.__nr_pb == other.__nr_pb

class Laborator:
    def __init__(self,stud,prob,nota):
        self.__stud = stud
        self.__prob = prob
        self.__nota = nota

    def get_stud(self): return self.__stud
    def get_prob(self): return self.__prob
    def get_id_stud(self): return self.__stud.get_id_stud()
    def get_nr_pb(self): return self.__prob.get_nr_pb()
    def get_nota(self): return self.__nota

    def set_nota(self, nota_noua): self.__nota = nota_noua
    def set_stud(self, stud_nou): self.__stud = stud_nou
    def set_prob(self, prob_noua): self.__prob = prob_noua

    def __str__(self):
        if self.__nota == 0:
            return "Studentul #" + str(self.__stud.get_id_stud()) + " " + self.__stud.get_nume() + " gr:" \
                   + str(self.__stud.get_grup()) + " nu a primit nota la problema " + str(self.__prob.get_nr_pb())
            #return "Studentul cu ID-ul " + str(self.__stud.get_id_stud()) + " nu a primit la laboratorul numarul " + str(self.__prob.get_nr_pb()) + " nota. "
        else:
            return "Studentul #" + str(self.__stud.get_id_stud()) + " " + self.__stud.get_nume() + " gr:"\
                   + str(self.__stud.get_grup()) + " a primit nota " + str(self.__nota) + " la problema " + str(self.__prob.get_nr_pb())
            #return "Studentul cu ID-ul " + str(self.__stud.get_id_stud()) + " are la laboratorul numarul " + str(self.__prob.get_nr_pb()) + " nota: " + str(self.__nota)

    def __eq__(self, other):
        return self.__stud.get_id_stud() == other.__stud.get_id_stud() and  self.__prob.get_nr_pb() == other.__prob.get_nr_pb()

class MedieDTO:
    def __init__(self,stud,medie):
        self.__stud = stud
        self.__medie = medie

    def get_stud(self): return self.__stud
    def get_medie(self): return self.__medie

    def __str__(self):
        return "Studentul #" + str(self.__stud.get_id_stud()) + " " + self.__stud.get_nume() + " gr:" \
               + str(self.__stud.get_grup()) + " are media " + str(self.__medie)