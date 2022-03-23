from Entity.validatori import ValidatorJucator
from Interface.consola import UI
from Repository.repo_jucatori import RepoJucatori
from Service.srv_jucatori import ServiceJucatori

if __name__ == '__main__':
    valid = ValidatorJucator()
    repo = RepoJucatori("jucatori.txt")
    srv = ServiceJucatori(valid, repo)
    consola = UI(srv)
    consola.run()