import unittest

from Controller.servicii import ServiceStudenti, ServiceProbleme, ServiceLaboratoare
from Domain.entity_laborator import Laborator
from Domain.entity_problema import Problema
from Domain.entity_student import Student
from Domain.exceptii import RepoError, ValidError, ServError
from Domain.sortari import Sortari
from Domain.validatoare import ValidatorStudent, ValidatorProblema, ValidatorLaborator
from Repository.repo_laborator import FileRepositoryLaborator
from Repository.repo_problema import FileRepositoryProbleme
from Repository.repo_student import FileRepositoryStudenti
from Tests.testare import Teste


class TesteVechi(unittest.TestCase):
    def testeaza(self):
        self.old = Teste()
        self.old.run_all()

class TestCaseRepos(unittest.TestCase):
    def setUp(self):
        import os

        #os.mkdir(os.getcwd() + "\\Fisiere")
        #self.file_stud = open("Fisiere\\test_studenti.txt", "w")
        #self.file_prob = open("Fisiere\\test_probleme.txt", "w")
        #self.file_lab = open("Fisiere\\test_laboratoare.txt", "w")

        self.repo_stud = FileRepositoryStudenti("test_studenti.txt")
        self.repo_prob = FileRepositoryProbleme("test_probleme.txt")
        self.repo_lab = FileRepositoryLaborator("test_laboratoare.txt")

        self.stud = Student(1,"Sami",216)
        self.prob = Problema(1,"Clase",9)

    def tearDown(self):
        import shutil, os
        #self.file_stud.close()
        #self.file_prob.close()
        #self.file_lab.close()

        shutil.rmtree(os.getcwd() + "\\Fisiere")

    def test_adaugaStudent(self):
        self.assertEqual(len(self.repo_stud), 0)
        self.repo_stud.adauga(self.stud)
        self.assertEqual(len(self.repo_stud),1)
        self.assertEqual(str(self.stud),"ID: 1, nume: Sami, grupa: 216")
        self.stud_duplicat = Student(1,"Alex",215)
        self.assertRaisesRegex(RepoError,"Student existent !\n",self.repo_stud.adauga,self.stud_duplicat)

        self.lista_stud = self.repo_stud.get_all()
        self.assertEqual(len(self.lista_stud),1)
        self.assertEqual(self.lista_stud[0].get_id_stud(),1)
        self.assertEqual(self.lista_stud[0].get_nume(),"Sami")
        self.assertEqual(self.lista_stud[0].get_grup(),216)
        self.stud2 = Student(2, "Alex", 215)
        self.repo_stud.adauga(self.stud2)
        self.assertEqual(len(self.repo_stud),2)

    def test_adaugaProblema(self):
        self.assertEqual(len(self.repo_prob), 0)
        self.repo_prob.adauga(self.prob)
        self.assertEqual(len(self.repo_prob), 1)
        self.assertEqual(str(self.prob), "Nr. problema: 1, descriere: Clase, deadline: 9")
        self.prob_duplicata = Problema(1, "Clase2", 10)
        self.assertRaisesRegex(RepoError, "Problema existenta !\n", self.repo_prob.adauga, self.prob_duplicata)

        self.lista_prob = self.repo_prob.get_all()
        self.assertEqual(len(self.lista_prob), 1)
        self.assertEqual(self.lista_prob[0].get_nr_pb(), 1)
        self.assertEqual(self.lista_prob[0].get_descriere(), "Clase")
        self.assertEqual(self.lista_prob[0].get_deadline(), 9)
        self.prob2 = Problema(2, "Fisiere", 10)
        self.repo_prob.adauga(self.prob2)
        self.assertEqual(len(self.repo_prob), 2)

    def test_adaugaLaborator(self):
        self.assertEqual(len(self.repo_lab), 0)
        self.lab = Laborator(self.stud, self.prob, 0)
        self.repo_lab.adauga(self.lab)
        self.assertEqual(str(self.lab), "Studentul #1 Sami gr:216 nu a primit nota la problema 1")
        self.assertEqual(len(self.repo_lab), 1)

    def test_modifica_student(self):
        self.repo_stud.adauga(self.stud)
        self.stud_modif = Student(1,"Alex",215)
        self.repo_stud.modifica(self.stud_modif)
        self.lista_stud = self.repo_stud.get_all()
        self.assertEqual(len(self.lista_stud), 1)
        self.assertEqual(self.lista_stud[0].get_id_stud(), 1)
        self.assertEqual(self.lista_stud[0].get_nume(), "Alex")
        self.assertEqual(self.lista_stud[0].get_grup(), 215)

    def test_modifica_problema(self):
        self.repo_prob.adauga(self.prob)
        self.prob_modif = Problema(1, "Fisiere", 10)
        self.repo_prob.modifica(self.prob_modif)
        self.lista_prob = self.repo_prob.get_all()
        self.assertEqual(len(self.lista_prob), 1)
        self.assertEqual(self.lista_prob[0].get_nr_pb(), 1)
        self.assertEqual(self.lista_prob[0].get_descriere(), "Fisiere")
        self.assertEqual(self.lista_prob[0].get_deadline(), 10)

        self.prob_inex = Problema(5, "ceva", 45)
        self.assertRaisesRegex(RepoError,"Problema inexistenta !\n",self.repo_prob.modifica,self.prob_inex)

    def test_sterge_student(self):
        self.repo_stud.adauga(self.stud)
        self.assertEqual(len(self.repo_stud), 1)
        self.repo_stud.sterge(1)
        self.assertEqual(len(self.repo_stud), 0)
        self.assertRaisesRegex(RepoError,"Student inexistent !\n",self.repo_stud.sterge,1)

    def test_sterge_problema(self):
        self.repo_prob.adauga(self.prob)
        self.assertEqual(len(self.repo_prob), 1)
        self.repo_prob.sterge(1)
        self.assertEqual(len(self.repo_prob), 0)
        self.assertRaisesRegex(RepoError,"Problema inexistenta !\n",self.repo_prob.sterge,1)

    def test_cauta_student(self):
        self.stud2 = Student(2, "Alex", 217)
        self.repo_stud.adauga(self.stud2)
        self.repo_stud.adauga(self.stud)
        self.gasit = self.repo_stud.cauta_id(1)
        self.assertEqual(self.stud,self.gasit)
        self.assertEqual(self.stud.get_id_stud(), self.gasit.get_id_stud())
        self.assertEqual(self.stud.get_nume(), self.gasit.get_nume())
        self.assertEqual(self.stud.get_grup(), self.gasit.get_grup())

        self.gasit_recursiv = self.repo_stud.cauta_id_recursiv(1)
        self.assertEqual(self.stud, self.gasit_recursiv)
        self.assertEqual(self.stud.get_id_stud(), self.gasit_recursiv.get_id_stud())
        self.assertEqual(self.stud.get_nume(), self.gasit_recursiv.get_nume())
        self.assertEqual(self.stud.get_grup(), self.gasit_recursiv.get_grup())
        self.assertRaisesRegex(RepoError, "Student inexistent !\n", self.repo_stud.cauta_id_recursiv,10)

    def test_cauta_problema(self):
        self.prob2 = Problema(2, "Fisiere", 10)
        self.repo_prob.adauga(self.prob2)
        self.repo_prob.adauga(self.prob)
        self.gasit = self.repo_prob.cauta_nr_pb(1)
        self.assertEqual(self.prob,self.gasit)
        self.assertEqual(self.prob.get_nr_pb(), self.gasit.get_nr_pb())
        self.assertEqual(self.prob.get_descriere(), self.gasit.get_descriere())
        self.assertEqual(self.prob.get_deadline(), self.gasit.get_deadline())

        self.gasit_recursiv = self.repo_prob.cauta_nr_pb_recursiv(1)
        self.assertEqual(self.prob, self.gasit_recursiv)
        self.assertEqual(self.prob.get_nr_pb(), self.gasit_recursiv.get_nr_pb())
        self.assertEqual(self.prob.get_descriere(), self.gasit_recursiv.get_descriere())
        self.assertEqual(self.prob.get_deadline(), self.gasit_recursiv.get_deadline())
        self.assertRaisesRegex(RepoError, "Problema inexistenta !\n", self.repo_prob.cauta_nr_pb_recursiv, 10)

class TestCaseServs(unittest.TestCase):
    def setUp(self):
        import os
        #os.mkdir(os.getcwd() + "\\Fisiere")
        #self.file_stud = open("Fisiere\\test_studenti.txt", "w")
        #self.file_prob = open("Fisiere\\test_probleme.txt", "w")
        #self.file_lab = open("Fisiere\\test_laboratoare.txt", "w")

        self.valid_stud = ValidatorStudent()
        self.valid_prob = ValidatorProblema()
        self.valid_lab = ValidatorLaborator()

        self.repo_stud = FileRepositoryStudenti("test_studenti.txt")
        self.repo_prob = FileRepositoryProbleme("test_probleme.txt")
        self.repo_lab = FileRepositoryLaborator("test_laboratoare.txt")

        self.srv_stud = ServiceStudenti(self.valid_stud,self.repo_stud)
        self.srv_prob = ServiceProbleme(self.valid_prob,self.repo_prob)
        self.srv_lab = ServiceLaboratoare(self.valid_lab,self.repo_stud,self.repo_prob,self.repo_lab)

        self.id_stud = 1
        self.nume = "Sami"
        self.grup = 216

        self.nr_pb = 1
        self.descriere = "Clase"
        self.deadline = 9

        self.assertEqual(len(self.srv_stud.Get_studenti()), 0)
        self.srv_stud.Adauga_student(self.id_stud, self.nume, self.grup)
        self.assertEqual(len(self.srv_stud.Get_studenti()), 1)

        self.assertEqual(len(self.srv_prob.Get_probleme()), 0)
        self.srv_prob.Adauga_problema(self.nr_pb, self.descriere, self.deadline)
        self.assertEqual(len(self.srv_prob.Get_probleme()), 1)

    def tearDown(self):
        #self.file_stud.close()
        #self.file_prob.close()
        #self.file_lab.close()

        import os, shutil

        shutil.rmtree(os.getcwd() + "\\Fisiere")
        #os.remove("Fisiere\\test_studenti.txt")
        #os.remove("Fisiere\\test_probleme.txt")
        #os.remove("Fisiere\\test_laboratoare.txt")

        #os.rmdir(os.getcwd() + "\\Fisiere")

    def test_AdaugaStudent(self):
        self.assertEqual(len(self.srv_stud.Get_studenti()), 1)
        self.assertRaisesRegex(RepoError,"Student existent !\n",self.srv_stud.Adauga_student,1,"Nume",213)
        self.assertRaisesRegex(ValidError,"ID invalid !\nNume invalid !\nGrup invalid !\n",self.srv_stud.Adauga_student,-self.id_stud,"",220.3)
        self.srv_stud.Adauga_student(self.id_stud+1, self.nume, self.grup)
        self.assertEqual(len(self.srv_stud.Get_studenti()), 2)

    def test_AdaugaProblema(self):
        self.assertEqual(len(self.srv_prob.Get_probleme()), 1)
        self.assertRaisesRegex(RepoError,"Problema existenta !\n",self.srv_prob.Adauga_problema,1,"Desc",43)
        self.assertRaisesRegex(ValidError,"Numar de problema invalid !\nDescriere invalida !\nDeadline invalid !\n",self.srv_prob.Adauga_problema,-self.nr_pb,"",220.3)
        self.srv_prob.Adauga_problema(self.nr_pb+1, self.descriere, self.deadline)
        self.assertEqual(len(self.srv_prob.Get_probleme()), 2)

    def test_ModificaStudent(self):
        self.assertEqual(self.srv_stud.Get_studenti()[0].get_nume(), "Sami")
        self.assertEqual(self.srv_stud.Get_studenti()[0].get_grup(), 216)
        self.srv_stud.Modifica_student(self.id_stud,"Alex",213)
        self.lista_stud = self.srv_stud.Get_studenti()
        self.assertEqual(self.lista_stud[0].get_nume(),"Alex")
        self.assertEqual(self.lista_stud[0].get_grup(),213)
        self.assertRaisesRegex(RepoError,"Student inexistent !\n",self.srv_stud.Modifica_student,5,"Nume",212)

    def test_ModificaProblema(self):
        self.assertEqual(self.srv_prob.Get_probleme()[0].get_descriere(), "Clase")
        self.assertEqual(self.srv_prob.Get_probleme()[0].get_deadline(), 9)
        self.srv_prob.Modifica_problema(self.nr_pb,"Fisiere",10)
        self.assertEqual(self.srv_prob.Get_probleme()[0].get_descriere(), "Fisiere")
        self.assertEqual(self.srv_prob.Get_probleme()[0].get_deadline(), 10)

    def test_StergeStudent(self):
        self.assertEqual(len(self.srv_stud.Get_studenti()), 1)
        self.srv_stud.Sterge_student(1)
        self.assertEqual(len(self.srv_stud.Get_studenti()), 0)
        self.assertRaisesRegex(RepoError,"Student inexistent !\n",self.srv_stud.Sterge_student,1)

    def test_StergeProblema(self):
        self.assertEqual(len(self.srv_prob.Get_probleme()), 1)
        self.srv_prob.Sterge_problema(1)
        self.assertEqual(len(self.srv_prob.Get_probleme()), 0)
        self.assertRaisesRegex(RepoError,"Problema inexistenta !\n",self.srv_prob.Sterge_problema,1)

    def test_CautaStudent(self):
        self.gasit = self.srv_stud.Cauta_student_id(1)
        self.assertEqual(self.gasit.get_id_stud(), 1)
        self.assertEqual(self.gasit.get_nume(), "Sami")
        self.assertEqual(self.gasit.get_grup(), 216)
        self.assertRaisesRegex(RepoError,"Student inexistent !\n",self.srv_stud.Cauta_student_id,2)

    def test_CautaProblema(self):
        self.gasit = self.srv_prob.Cauta_problema_nr(1)
        self.assertEqual(self.gasit.get_nr_pb(), 1)
        self.assertEqual(self.gasit.get_descriere(), "Clase")
        self.assertEqual(self.gasit.get_deadline(), 9)
        self.assertRaisesRegex(RepoError,"Problema inexistenta !\n",self.srv_prob.Cauta_problema_nr,2)

    def test_Asignare(self):
        self.srv_lab.Asignare(1, 1)
        self.labs = self.srv_lab.Get_laboratoare()
        self.assertEqual(len(self.labs), 1)
        self.assertEqual(self.labs[0].get_nota(), 0)

        self.assertRaisesRegex(ServError,"Student inexistent !\nProblema inexistenta !\n",self.srv_lab.Asignare,5,5)

        self.stud_gresit = Student(-1, "Nume", 214)
        self.prob_gresita = Problema(-1, "desc", 6)
        self.lab_gresit = Laborator(self.stud_gresit, self.prob_gresita, 11)
        self.assertRaisesRegex(ValidError,"ID invalid !\nNumar de problema invalid !\nNota invalida !\n", self.valid_lab.valideaza,self.lab_gresit)
        self.assertRaisesRegex(RepoError,"Laborator deja asignat studentului cu ID-ul 1 !\n",self.srv_lab.Asignare,1,1)

        self.srv_stud.Modifica_student(1,"Alex",214)
        self.srv_lab.Update()
        self.assertEqual(len(self.srv_lab.Get_laboratoare()), 1)

        self.srv_stud.Sterge_student(1)
        self.srv_lab.Update()
        self.assertEqual(len(self.srv_lab.Get_laboratoare()),0)


    def test_AsignareNota(self):
        self.assertRaisesRegex(RepoError,"Studentul dat nu are asignata problema introdusa !\n",self.srv_lab.Asignare_nota,1,1,10)
        self.srv_lab.Asignare(1, 1)
        self.assertRaisesRegex(ValidError,"Nota invalida !\n",self.srv_lab.Asignare_nota,1,1,11)

        self.srv_lab.Asignare_nota(1, 1, 10)
        self.labs = self.srv_lab.Get_laboratoare()
        self.assertEqual(len(self.labs), 1)
        self.assertEqual(self.labs[0].get_nota(), 10)
        self.assertEqual(str(self.labs[0]), "Studentul #1 Sami gr:216 a primit nota 10.0 la problema 1")

        #self.srv_stud.Modifica_student(1, "Alex", 214)
        #self.assertEqual(str(self.labs[0]), "Studentul #1 Alex gr:214 a primit nota 10.0 la problema 1")

    def test_AsignareGrupa(self):
        self.srv_stud.Adauga_student(2,"Alex",213)
        self.srv_stud.Adauga_student(3,"Tab",216)

        self.srv_lab.Asignare_grupa(216,1)
        self.assertEqual(len(self.srv_lab.Get_laboratoare()), 2)
        self.assertRaisesRegex(ServError,"Laborator deja asignat studentului cu ID-ul 1 !\nLaborator deja asignat studentului cu ID-ul 3 !\n",self.srv_lab.Asignare_grupa,216,1)

    def test_ModificaNota(self):
        self.assertRaisesRegex(RepoError,"Studentul dat nu are asignata problema introdusa !\n",self.srv_lab.Modifica_nota,1,1,5.5)
        self.srv_lab.Asignare(1, 1)
        self.assertRaisesRegex(ServError,"Studentul cu ID-ul dat nu are inca nota la problema precizata !\n",self.srv_lab.Modifica_nota,1,1,5.5)
        self.srv_lab.Asignare_nota(1, 1, 10)
        self.assertEqual(self.srv_lab.Get_laboratoare()[0].get_nota(), 10)
        self.srv_lab.Modifica_nota(1, 1, 5.5)
        self.assertEqual(self.srv_lab.Get_laboratoare()[0].get_nota(), 5.5)

    def test_StergeAsignare(self):
        self.srv_lab.Asignare(1, 1)
        self.assertEqual(len(self.srv_lab.Get_laboratoare()), 1)
        self.srv_lab.Sterge(1, 1)
        self.assertEqual(len(self.srv_lab.Get_laboratoare()), 0)
        self.assertRaisesRegex(RepoError,"Studentul cu ID-ul 1 nu are asignata problema 1 !\n",self.srv_lab.Sterge,1,1)

    def test_Notalaproblema(self):
        self.srv_stud.Adauga_student(2, "Alex", 216)
        self.srv_stud.Adauga_student(3, "Tab", 216)

        self.srv_lab.Asignare_grupa(216,1)
        self.srv_lab.Asignare_nota(1,1,10)
        self.srv_lab.Asignare_nota(2,1,9.5)
        self.srv_lab.Asignare_nota(3,1,9.9)
        self.note = self.srv_lab.Nota_la_problema(1)
        self.assertEqual(len(self.note),3)
        self.assertEqual(self.note[0].get_nota(),10)
        self.assertEqual(self.note[0].get_stud().get_nume(),"Sami")
        self.assertEqual(self.note[1].get_nota(), 9.9)
        self.assertEqual(self.note[1].get_stud().get_nume(), "Tab")
        self.assertEqual(self.note[2].get_nota(), 9.5)
        self.assertEqual(self.note[2].get_stud().get_nume(), "Alex")
        self.assertRaisesRegex(RepoError,"Problema inexistenta !\n",self.srv_lab.Nota_la_problema,2)

    def test_Mediemaimica(self):
        self.srv_stud.Adauga_student(2, "Alex", 216)
        self.srv_stud.Adauga_student(3, "Tab", 216)

        self.srv_lab.Asignare_grupa(216, 1)
        self.srv_lab.Asignare_nota(1, 1, 10)
        self.srv_lab.Asignare_nota(2, 1, 7)
        self.srv_lab.Asignare_nota(3, 1, 4)

        self.assertEqual(len(self.srv_lab.Medie_mai_mica(4, 10)), 3)
        self.assertEqual(str(self.srv_lab.Medie_mai_mica(4, 10)[0]), "Studentul #1 Sami gr:216 are media 10.0")
        self.assertEqual(len(self.srv_lab.Medie_mai_mica(7, 10)), 2)
        self.assertEqual(len(self.srv_lab.Medie_mai_mica(10, 10)), 1)
        self.assertEqual(len(self.srv_lab.Medie_mai_mica(5, 6)), 0)
        self.assertRaisesRegex(ValidError,"Interval invalid !\n",self.srv_lab.Medie_mai_mica,-1,5)

class TesteSortari(unittest.TestCase):
    def setUp(self):
        self.sort = Sortari()
        self.st1 = Student(1, "Sami", 216)
        self.st2 = Student(2, "Dragos", 212)
        self.st3 = Student(3, "Ilie", 211)
        self.st4 = Student(4, "Alex", 217)
        self.x = []
        self.x.append(self.st4)
        self.x.append(self.st2)
        self.x.append(self.st1)
        self.x.append(self.st3)

    def test_selectionSort(self):
        self.sort.selectionSort(self.x,key=lambda x:x.get_id_stud())
        self.assertEqual(self.x[0], self.st1)
        self.assertEqual(self.x[1], self.st2)
        self.assertEqual(self.x[2], self.st3)
        self.assertEqual(self.x[3], self.st4)
        # Reversed
        self.sort.selectionSort(self.x, key=lambda x: x.get_id_stud(), reversed=True)
        self.assertEqual(self.x[0], self.st4)
        self.assertEqual(self.x[1], self.st3)
        self.assertEqual(self.x[2], self.st2)
        self.assertEqual(self.x[3], self.st1)

    def test_gnomeSort(self):
        self.sort.gnomeSort(self.x, key=lambda x: x.get_id_stud())
        self.assertEqual(self.x[0], self.st1)
        self.assertEqual(self.x[1], self.st2)
        self.assertEqual(self.x[2], self.st3)
        self.assertEqual(self.x[3], self.st4)
        # Reversed
        self.sort.gnomeSort(self.x, key=lambda x: x.get_id_stud(), reversed=True)
        self.assertEqual(self.x[0], self.st4)
        self.assertEqual(self.x[1], self.st3)
        self.assertEqual(self.x[2], self.st2)
        self.assertEqual(self.x[3], self.st1)

class TesteSortari2(unittest.TestCase):
    def setUp(self):
        self.sort = Sortari()
        self.st1 = Student(1, "A", 17)
        self.st2 = Student(2, "B", 7)
        self.st3 = Student(3, "B", 17)
        self.st4 = Student(4, "C", 12)
        self.x = []
        self.x.append(self.st1)
        self.x.append(self.st2)
        self.x.append(self.st3)
        self.x.append(self.st4)

    def test_selectionSort(self):
        self.sort.selectionSort(self.x,key=lambda x: (x.get_grup(),x.get_nume()), reversed=True)
        self.assertEqual(self.x[0], self.st3)
        self.assertEqual(self.x[1], self.st1)
        self.assertEqual(self.x[2], self.st4)
        self.assertEqual(self.x[3], self.st2)