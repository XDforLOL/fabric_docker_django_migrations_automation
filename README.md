# Automated Docker creation and Django Migration
## With fabric and ansible

A fabric Ansible script for automating the setup of a docker container from local_host to a remote host

### Prerequisite

- knowladge in unix oprating systems
- ansible playbook 
- docker 
- and django 
- git
## Description

#### Welcome to the docker automation script

in this project I aim to automate the requirements, docker and PSQL DB creation for a Django web application
The creation of .env variables with only the needed input for starting a docker container.


## Host server setup
ensure that you have a unix based system host to run the setup from(Tested on ubuntu 20.04)

* `git clone <this repository>`  
* `cd <./ThisProjectRoot>` 
* create a venv `python3 -m venv <name>` after your venv is up it needs to be activated 
* `source venv/bin/activate`
* after activating the environment you need to pip install requirements `pip install -r requirements.txt`

### Deploy

Open Hosts with the desired editor `./ansible-main/HOSTS` and change `[name]` `<insert hostname/IP>` 
* run `python start_stack.py`
* 
### run-time

while the script is runing,
it will prompt you with important variables for SSHing to a server with a Password.
*the sudo password/secrets do not echo to commmand line*
After running the inital setup you will be prompted for a github django project github URL

### After everything ran successfully

![InkedCapture5_LI](https://user-images.githubusercontent.com/47694559/113005053-c90d5b00-917c-11eb-9907-e8347ecaeaa4.jpg)
you can SSH into your remote server, `cd <into ./manage.py directory root>` and `python manage.py runserver`

## Project tree
* Remote Host
```
├──django_project
    ├── crm__showcase
    │    ├── crm_retail
    │    ├── django_retail_crm
    │    ├── example.log
    │    ├── lib
    │    ├── manage.py
    │    ├── products_shopping_cart
    │    ├── __pycache__
    │    ├── pyvenv.cfg
    │    ├── README.md
    │    ├── read_me_screenshots
    │    ├── requirements.txt
    │    ├── Scripts
    │    └── static
    └──.venv
```
* Local Host
```
├── ansible-main
│    ├── ansible.cfg
│    ├── HOSTS
│    └── playbook.yml
├── README.md
├── requirements.txt
└── start_stack.py
```
