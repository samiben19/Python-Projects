from Domain.entity_laborator import Laborator
from Domain.entity_student import Student
from Domain.entity_problema import Problema
from Domain.validatoare import ValidatorStudent, ValidatorProblema, ValidatorLaborator
from Repository.repo_laborator import RepositoryLaborator
from Repository.repo_problema import RepositoryProbleme
from Repository.repo_student import RepositoryStudenti
from Controller.servicii import ServiceStudenti, ServiceLaboratoare, ServiceProbleme
from Domain.exceptii import ValidError, RepoError

class Teste:
    def __test_domeniu_stud(self):
        id_stud = 1
        nume = 'Alin'
        grup = 216
        student = Student(id_stud, nume, grup)
        assert (student.get_id_stud() == id_stud)
        assert (student.get_nume() == nume)
        assert (student.get_grup() == grup)
        assert (str(student) == "ID: 1, nume: Alin, grupa: 216")
        student2 = Student(id_stud,'Calin',210)
        assert (student == student2)

        nr_pb = 1
        descriere = "Folosiți dezvoltarea iterativă bazat pe funcționalități"
        deadline = 5

        problema_lab = Problema(nr_pb, descriere, deadline)
        assert (problema_lab.get_nr_pb() == nr_pb)
        assert (problema_lab.get_descriere() == descriere)
        assert (problema_lab.get_deadline() == deadline)

    def __test_validare_stud(self):
        valid_stud = ValidatorStudent()
        student_rau = Student(-34,"",23.2)
        try:
            valid_stud.valideaza(student_rau)
            #assert (False)
        except ValidError as ve:
            assert (str(ve) == "ID invalid !\nNume invalid !\nGrup invalid !\n")

        valid_problema = ValidatorProblema()
        problema_rea = Problema(3.3,"",6.3)
        try:
            valid_problema.valideaza(problema_rea)
            #assert (False)
        except ValidError as ve:
            assert (str(ve) == "Numar de problema invalid !\nDescriere invalida !\nDeadline invalid !\n")

    def __test_repo_student(self):
        repo = RepositoryStudenti()
        assert (len(repo) == 0)
        id_stud = 1
        nume = 'Alin'
        grup = 216
        student = Student (id_stud, nume, grup)
# adauga
        repo.adauga(student)
        assert (len(repo) == 1)
        try:
            repo.adauga(student)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student existent !\n")
# cauta
        gasit = repo.cauta_id(id_stud)
        assert (gasit.get_nume() == nume)
        assert (gasit.get_grup() == grup)
        try:
            repo.cauta_id(id_stud+5)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")
# modifica
        student_nou = Student(id_stud,"Marcel",210)
        repo.modifica(student_nou)
        gasit = repo.cauta_id(id_stud)
        assert (gasit.get_nume() == "Marcel")
        assert (gasit.get_grup() == 210)
        student_nou_rau = Student(id_stud+5, "Marcel", 210)
        try:
            repo.modifica(student_nou_rau)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")
# get_all
        all = repo.get_all()
        assert (len(all) == 1)
        assert (all[0].get_id_stud() == id_stud)
        assert (all[0].get_nume() == "Marcel")
        assert (all[0].get_grup() == 210)
# sterge
        repo.sterge(id_stud)
        assert (len(repo) == 0)
        try:
            repo.sterge(id_stud)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")


    def __test_controller_stud(self):
        valid = ValidatorStudent()
        repo = RepositoryStudenti()
        srv = ServiceStudenti(valid,repo)
# Adaugare
        id_stud = 23
        nume = "Petru"
        grup = 216
        srv.Adauga_student(id_stud, nume, grup)
        studenti = srv.Get_studenti()   # Get all
        assert (len(studenti) == 1)
        try:
            srv.Adauga_student(id_stud, nume, grup)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student existent !\n")

        try:
            srv.Adauga_student(-id_stud, nume, -grup)
            #assert (False)
        except ValidError as ve:
            assert (str(ve) == "ID invalid !\nGrup invalid !\n")
# Modificare
        nume = "Alin"
        grup = 211
        srv.Modifica_student(id_stud, nume, grup)
        studenti = srv.Get_studenti()
        assert (studenti[0].get_nume() == nume)
        assert (studenti[0].get_grup() == grup)
        try:
            srv.Modifica_student(id_stud+5, nume, grup)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")
# Sterge
        srv.Sterge_student(id_stud)
        studenti = srv.Get_studenti()
        assert (len(studenti) == 0)
        try:
            srv.Sterge_student(id_stud)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")
# Cauta
        try:
            srv.Cauta_student_id(id_stud)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Student inexistent !\n")
        srv.Adauga_student(id_stud, nume, grup)
        stud = srv.Cauta_student_id(id_stud)
        assert (stud.get_id_stud() == id_stud)
        assert (stud.get_nume() == nume)
        assert (stud.get_grup() == grup)

    def __test_repo_lab(self):
        repo_stud = RepositoryStudenti()
        repo_pb = RepositoryProbleme()
        repo_lab = RepositoryLaborator()
        id_stud = 1
        nume = 'Alin'
        grup = 216
        student = Student(id_stud, nume, grup)
        repo_stud.adauga(student)
        nr_pb = 1
        desc = 'Clase'
        deadline = 9
        problema = Problema(nr_pb,desc,deadline)
        repo_pb.adauga(problema)
        nr_pb = 2
        desc = 'Clase2'
        deadline = 3
        problema2 = Problema(nr_pb, desc, deadline)
        repo_pb.adauga(problema2)

        laborator = Laborator(student,problema,0)
        laborator2 = Laborator(student,problema2,0)
        # adauga
        repo_lab.adauga(laborator)
        assert (len(repo_lab) == 1)
        repo_lab.adauga(laborator2)
        assert (len(repo_lab) == 2)
        try:
            repo_lab.adauga(laborator)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Laborator deja asignat studentului cu ID-ul 1 !\n")
        # cauta dupa id
        laboratoare = repo_lab.cauta_id_stud(id_stud)
        assert (len(laboratoare) == 2)
        assert (laboratoare[0] == laborator)
        assert (laboratoare[1] == laborator2)
        try:
            repo_lab.cauta_id_stud(id_stud+5)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Nu exista niciun laborator asignat studentului cu acest ID !\n")
        # cauta exact
        repo_lab.cauta_exact(1,1)
        repo_lab.cauta_exact(1,2)
        try:
            repo_lab.cauta_exact(1,3)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Studentul dat nu are asignata problema introdusa !\n")
        # modifica
        student = Student(1, 'Alin', 216)
        problema = Problema(1, 'Clase', 9)
        lab_nota_noua = Laborator(student, problema, 10)
        repo_lab.modifica(lab_nota_noua)
        gasit = repo_lab.cauta_exact(1,1)
        assert (gasit.get_nota() == 10)
        assert (gasit.get_stud().get_nume() == "Alin")
        assert (gasit.get_stud().get_grup() == 216)
        student2 = Student(2, 'Calin', 216)
        lab_rau = Laborator(student2, problema, 10)
        try:
            repo_lab.modifica(lab_rau)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Nu exista acest laborator asignat studentului cu ID-ul dat!\n")
        # get_all
        all = repo_lab.get_all()
        assert (len(all) == 2)
        assert (all[0].get_id_stud() == 1)
        assert (all[0].get_stud().get_nume() == "Alin")
        assert (all[0].get_stud().get_grup() == 216)
        assert (all[0].get_nr_pb() == 1)
        assert (all[0].get_prob().get_descriere() == "Clase")
        assert (all[1].get_nr_pb() == 2)
        assert (all[1].get_prob().get_descriere() == "Clase2")
        # sterge
        repo_lab.sterge(1,1)
        assert (len(repo_lab) == 1)
        try:
            repo_lab.sterge(1,1)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Studentul cu ID-ul 1 nu are asignata problema 1 !\n")

    def __test_controller_lab(self):
        valid_stud = ValidatorStudent()
        repo_stud = RepositoryStudenti()
        srv_stud = ServiceStudenti(valid_stud, repo_stud)

        valid_prob = ValidatorProblema()
        repo_prob = RepositoryProbleme()
        srv_prob = ServiceProbleme(valid_prob, repo_prob)

        valid_lab = ValidatorLaborator()
        repo_lab = RepositoryLaborator()
        srv_lab = ServiceLaboratoare(valid_lab,repo_stud,repo_prob,repo_lab)
        # Asignare
        srv_stud.Adauga_student(1, "Sami", 216)
        srv_prob.Adauga_problema(1, "Clase", 9)
        srv_prob.Adauga_problema(2, "Clase2", 10)
        srv_prob.Adauga_problema(3, "Clase3", 11)
        srv_lab.Asignare(1,1)
        try:
            srv_lab.Asignare(1,1)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Laborator deja asignat studentului cu ID-ul 1 !\n")
        # Asignare nota
        srv_lab.Asignare_nota(1,1,7)
        try:
            srv_lab.Asignare_nota(1,1,3)
            #assert (False)
        except ValidError as ve:
            assert (str(ve) == "Studentul dat are deja nota la problema introdusa !\n")
        try:
            srv_lab.Asignare_nota(1,1,30)
            #assert (False)
        except ValidError as ve:
            assert (str(ve) == "Nota invalida !\n")
        try:
            srv_lab.Asignare_nota(1,2,7)
            #assert (False)
        except RepoError as re:
            assert (str(re) == "Studentul dat nu are asignata problema introdusa !\n")
        # Stat1, Stat2
        assert len(srv_lab.Medie_mai_mica(0.0001,5)) == 0
        srv_lab.Asignare(1, 2)
        srv_lab.Asignare_nota(1,2,1)
        medii = srv_lab.Medie_mai_mica(0.0001,5)
        note = srv_lab.Nota_la_problema(1)
        assert len(note) == 1
        assert len(medii) == 1
        assert medii[0].get_medie() == 4


    def run_all(self):
        self.__test_domeniu_stud()
        self.__test_validare_stud()
        self.__test_repo_student()
        self.__test_controller_stud()
        self.__test_repo_lab()
        self.__test_controller_lab()
