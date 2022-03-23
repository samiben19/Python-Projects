class Student(object):
    def __init__(self, id_stud, nume, grup):
        self.__id_stud = id_stud
        self.__nume = nume
        self.__grup = grup

    def get_id_stud(self): return self.__id_stud
    def get_nume(self): return self.__nume
    def get_grup(self): return self.__grup

    def set_nume(self, value): self.__nume = value
    def set_grup(self, value): self.__grup = value

    def __str__(self):
        return "ID: " + str(self.__id_stud) + ", nume: " + self.__nume + ", grupa: " + str(self.__grup)

    def __eq__(self, other):
        return self.__id_stud == other.__id_stud

# import json
#
# a = Student(1,"Alex",216)
# x = []
# #x.append(a)
#
# def dumper(obj):
#     try:
#         return obj.toJSON()
#     except:
#         return obj.__dict__
#
# #with open("json.txt", 'w') as f_out:
#     #f_out.write(json.dumps(x, default=dumper))
#
# def citeste():
#     with open("json.txt", 'r') as f_in:
#         return json.loads(f_in.read())
#
# x=citeste()
# print(x)