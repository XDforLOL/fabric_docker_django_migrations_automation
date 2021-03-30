import sys
import os
from getpass import getpass
from fabric import Connection, Config

import fabric


class FabricConnectionSetup():

    def __init__(self, cmd) -> None:
        if cmd == 'start':
            self.config = Config(overrides={
                'user': input("What is your user?"),
                # TODO .read from ssh create hidden maybe
                'connect_kwargs': {'password': getpass("Sudo password?\n")}
            })

            self.connection_host = Connection(input("Insert Host to connect: *host_name/IP*"), config=self.config)

            print('connection established')

        else:
            quit()

    def docker_check(self) -> bool:
        print('--- Docker check ---')
        docker_v = self.connection_host.run("docker -v")
        if "The program 'docker' is currently not installed." in docker_v.stdout:
            try:

                self.connection_host.run("sudo apt-get update")
                self.connection_host.run("sudo apt-get install docker-ce docker-ce-cli containerd.io")
                return True
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return False

        else:
            return True

    def create_docker_container(self) -> bool:
        if self.docker_check():
            print('--- Creating variables for OS.environment ---')

            self.DB_NAME = input('insert DB_name: ')
            self.DB_SECRET = getpass('insert mysecretpassword: ')
            self.DB_USER = input('insert DB_USER: ')
            self.DB_HOST = input('insert Host name or IP: ')
            self.SECRET_KEY = getpass('insert django_secret: ')
            self.DB_PORT = input('port:port ')

            print('--- Creating new PSQL docker container ---')

            self.connection_host.run(
                f"sudo docker run -d -p {self.DB_PORT} "
                f"--name {input('Insert: docker_name')} "
                f"-e POSTGRES_PASSWORD={self.DB_SECRET} "
                f"-e POSTGRES_DB={self.DB_NAME} "
                f"-e POSTGRES_USER={self.DB_USER} postgres"
            )
            return True

    def set_django_environment_vars(self) -> bool:
        if self.create_docker_container():
            from_port, to_port = self.DB_PORT.split(':', )

            exported_environments = [
                f"DB_NAME='{self.DB_NAME}'",
                f"DB_USER='{self.DB_USER}'",
                f"DB_SECRET='{self.DB_SECRET}'",
                f"DB_HOST='{self.DB_HOST}'",
                f"DJANGO_SECRET_KEY='{self.SECRET_KEY}'",
                f"DB_PORT='{to_port}'"
            ]
            print('--- Creating a new dir, attempting to pull project ---')

            self.connection_host.run('mkdir django_project')
            self.connection_host.run(
                f"cd ./django_project/ && git clone {input('insert: github_URL')}"
            )
            self.connection_host.run("cd ./django_project/crm__showcase/django_retail_crm/ && touch .env")

            for environment in exported_environments:
                self.connection_host.run(f"""cd ./django_project/crm__showcase/django_retail_crm/ && 
                echo "{environment}" >> .env""")
            
        return True

    def pull_django_project_migrations(self):

        git_check = self.connection_host.run('git --version')

        if 'not installed' in git_check.stdout:
            self.connection_host.run('sudo apt install git-all')

        elif self.set_django_environment_vars():

            print('Attempting to install pip requirements.txt')

            self.connection_host.run(
                'cd ./django_project/ &&'
                ' python3 -m venv venv &&'
                ' source venv/bin/activate &&'
                ' cd ./crm__showcase/ && pip3 install -r requirements.txt'
            )

            print('--- Attempting to makemigrations, and migrate  ---')
            anisble_check_and_run_playbook()


def anisble_check_and_run_playbook():
    ansible_check = os.popen('ansible --version')
    if 'not installed' in ansible_check.read():
        os.popen("sudo apt-get update")
        os.popen(
            "sudo apt install software-properties-common && "
            "sudo apt-add-repository --yes --update ppa:ansible/ansible && "
            "sudo apt install ansible"
        )
        run_playbook = os.popen('cd ./ansible-main && ansible-playbook -i HOSTS -k ./playbook.yml', 'w')
        run_playbook.write(input('Sudo pass: '))
        print('DONE!')
    else:
        run_playbook = os.popen('cd ./ansible-main && ansible-playbook -i HOSTS -k ./playbook.yml', 'w')
        run_playbook.write(input('Sudo pass: '))
        print('DONE!')


if __name__ == "__main__":
    FabricConnectionSetup('start').pull_django_project_migrations()

