# README #

### What is this repository for? ###

* User Directory


This project contains the following modules.

  * App
    * User


### How do I get set up? ###

* How to setup local environment
  - Here we need to create a virtual environment (using virtualenv with python3 version) so that the packages we install doesn't effect the local machine packages.
    ```sh
      $ virtualenv -p python3 env
    ```
    - This generates the env with python3 version.
  - We need to activate the env using source command.
    ```sh
      $ source env/bin/activate
    ```

* Summary of set up

* Configuration
  * Here we decide what technolgies we use with which version.
    - Django with 3.0.6
    - python with 3.7


* Dependencies
    * Install the project pip dependencies by executing the below command.
      ```sh
        $ pip install -r requirements.txt
      ```
    - This will install all the required dependencies for User Directory project to get started.


* Deployment instructions

  ```sh
    $ python manage.py makemigrations

    $ python manage.py migrate

    $ python manage.py createsuperuser

    $ python manage.py runserver
  ```

  * We need to run the below management commands to generate default `Users`
    ```sh
      $ python manage.py create_users
    ```
    * Admin Credentials email - "admin@gmail.com", password - "Qwerty@12"
* Dashboard
  * "http://localhost:8000/dashboard/"

* Admin panel
  * "http://localhost:8000/admin-page/"

* Profile
  * "http://localhost:8000/profile/"

* Change Password
  * "http://localhost:8000/change-password/"
### Who do I talk to? ###

#### Repo Owner: Teja Reddy Muvva
