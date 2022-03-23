import unittest

from Entity.jucator_entity import Jucator
from Entity.validatori import ValidatorJucator
from Repository.repo_jucatori import RepoJucatori
from Service.srv_jucatori import ServiceJucatori
from erori import ValidError, RepoError


class Teste(unittest.TestCase):
    def setUp(self):
        self.repo = RepoJucatori("test_jucatori.txt")
        self.valid = ValidatorJucator()
        self.srv = ServiceJucatori(self.valid, self.repo)

        self.j1 = Jucator("Sami", "Sami", 190, "pivot")
        self.j2 = Jucator("Alex", "Sami", 150, "fundas")
        self.j3 = Jucator("Andrei", "Sami", 130, "fundas")
        self.j4 = Jucator("Alin", "Sami", 160, "extrema")
        self.j5 = Jucator("Petru", "Sami", 189, "extrema")
        self.j6 = Jucator("Denis", "Sami", 169, "fundas")

        self.jRau = Jucator("", "", 0, "atacant")

    def tearDown(self):
        with open("test_jucatori.txt","w"):pass

    def test_Adauga(self):
        self.assertEqual(len(self.srv.Get_jucatori()),0)
        self.srv.Adauga_jucator(self.j1.get_nume(),self.j1.get_prenume(),self.j1.get_inaltime(),self.j1.get_post())
        self.assertEqual(len(self.srv.Get_jucatori()),1)
        self.assertEqual(self.j1.get_nume(),"Sami")
        self.assertEqual(str(self.j1), "Sami Sami 190 pivot")

        self.assertRaisesRegex(ValidError, "Nume invalid !\nPrenume invalid !\nInaltime invalida !\nPost invalid !\n", self.srv.Adauga_jucator, self.jRau.get_nume(),self.jRau.get_prenume(),self.jRau.get_inaltime(),self.jRau.get_post())
        self.assertRaisesRegex(RepoError, "Jucator deja existent !\n", self.srv.Adauga_jucator, self.j1.get_nume(),self.j1.get_prenume(),self.j1.get_inaltime(),self.j1.get_post())

    def test_Modifica(self):
        self.assertEqual(len(self.srv.Get_jucatori()), 0)
        self.srv.Adauga_jucator(self.j1.get_nume(), self.j1.get_prenume(), self.j1.get_inaltime(), self.j1.get_post())
        self.srv.Adauga_jucator(self.j2.get_nume(), self.j2.get_prenume(), self.j2.get_inaltime(), self.j2.get_post())
        self.srv.Adauga_jucator(self.j3.get_nume(), self.j3.get_prenume(), self.j3.get_inaltime(), self.j3.get_post())
        self.srv.Adauga_jucator(self.j4.get_nume(), self.j4.get_prenume(), self.j4.get_inaltime(), self.j4.get_post())

        self.assertEqual(len(self.repo), 4)

        self.assertEqual(self.srv.Get_jucatori()[0].get_inaltime(), 190)
        self.srv.Modifica_jucator("Sami","Sami", 250)
        self.assertEqual(self.srv.Get_jucatori()[0].get_inaltime(), 250)

        self.assertRaisesRegex(RepoError, "Jucator inexistent !\n", self.srv.Modifica_jucator, "Alinel", "Mititel", 125)

    def test_Echipa(self):
        self.assertEqual(len(self.srv.Get_jucatori()), 0)
        self.srv.Adauga_jucator(self.j1.get_nume(), self.j1.get_prenume(), self.j1.get_inaltime(), self.j1.get_post())
        self.srv.Adauga_jucator(self.j2.get_nume(), self.j2.get_prenume(), self.j2.get_inaltime(), self.j2.get_post())
        self.srv.Adauga_jucator(self.j3.get_nume(), self.j3.get_prenume(), self.j3.get_inaltime(), self.j3.get_post())
        self.srv.Adauga_jucator(self.j4.get_nume(), self.j4.get_prenume(), self.j4.get_inaltime(), self.j4.get_post())

        self.assertRaisesRegex(ValidError, "Prea putini jucatori in lista, trebuie minim 5 !\n", self.srv.Cerinta3)

        self.srv.Adauga_jucator(self.j6.get_nume(), self.j6.get_prenume(), self.j6.get_inaltime(), self.j6.get_post())

        self.assertRaisesRegex(ValidError, "Nu s-au gasit destui jucatori din fiecare post !\n", self.srv.Cerinta3)

        self.srv.Adauga_jucator(self.j5.get_nume(), self.j5.get_prenume(), self.j5.get_inaltime(), self.j5.get_post())
        self.echipa = self.srv.Cerinta3()
        self.assertEqual(self.echipa[0], self.j5)
        self.assertEqual(self.echipa[1], self.j4)
        self.assertEqual(self.echipa[2], self.j6)
        self.assertEqual(self.echipa[3], self.j2)
        self.assertEqual(self.echipa[4], self.j1)

    def test_Import(self):
        self.assertEqual(len(self.srv.Get_jucatori()), 0)
        self.srv.Adauga_jucator(self.j1.get_nume(), self.j1.get_prenume(), self.j1.get_inaltime(), self.j1.get_post())
        self.srv.Adauga_jucator(self.j2.get_nume(), self.j2.get_prenume(), self.j2.get_inaltime(), self.j2.get_post())
        self.srv.Adauga_jucator(self.j3.get_nume(), self.j3.get_prenume(), self.j3.get_inaltime(), self.j3.get_post())
        self.srv.Adauga_jucator(self.j4.get_nume(), self.j4.get_prenume(), self.j4.get_inaltime(), self.j4.get_post())
        self.srv.Adauga_jucator(self.j5.get_nume(), self.j5.get_prenume(), self.j5.get_inaltime(), self.j5.get_post())
        self.srv.Adauga_jucator(self.j6.get_nume(), self.j6.get_prenume(), self.j6.get_inaltime(), self.j6.get_post())

        self.nume_fisier_import = "test_import.txt"
        self.assertEqual(self.srv.Importa(self.nume_fisier_import), 4)
        self.assertEqual(self.srv.Importa(self.nume_fisier_import), 0)
