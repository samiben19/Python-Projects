from Domain.exceptii import ValidError

class ValidatorStudent:
     def valideaza(self, student):
        erori = ""
        if student.get_id_stud() < 0 or abs(student.get_id_stud() - int(student.get_id_stud())) >= 0.0001:
            erori += "ID invalid !\n"
        if student.get_nume() == "":
            erori += "Nume invalid !\n"
        if student.get_grup() < 0 or abs(float(student.get_grup()) - int(student.get_grup())) >= 0.0001:
            erori += "Grup invalid !\n"
        if len(erori) > 0:
            raise ValidError(erori)

class ValidatorProblema:
    def valideaza(self, problema):
        erori = ""
        if problema.get_nr_pb() < 0 or problema.get_nr_pb() - int(problema.get_nr_pb()) >= 0.00001:
            erori += "Numar de problema invalid !\n"
        if problema.get_descriere() == "":
            erori += "Descriere invalida !\n"
        if problema.get_deadline() < 0 or problema.get_deadline() - int(problema.get_deadline()) >= 0.00001:
            erori += "Deadline invalid !\n"
        if len(erori) > 0:
            raise ValidError(erori)

class ValidatorLaborator:
    def valideaza(self, laborator):
        erori = ""
        if laborator.get_id_stud() < 0 or laborator.get_id_stud() - int(laborator.get_id_stud()) >= 0.00001:
            erori += "ID invalid !\n"
        if laborator.get_nr_pb() < 0 or laborator.get_nr_pb() - int(laborator.get_nr_pb()) >= 0.00001:
            erori += "Numar de problema invalid !\n"
        if laborator.get_nota() < 0 or laborator.get_nota() > 10:
            erori += "Nota invalida !\n"
        if len(erori) > 0:
            raise ValidError(erori)
    def are_nota(self, laborator):
        if laborator.get_nota() != 0:
            raise ValidError("Studentul dat are deja nota la problema introdusa !\n")
