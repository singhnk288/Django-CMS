# Django CMS

## Features of CMS
* Multi-lingual Support
* Login System
* User Master
* Permission Management
* State and Country Master
* 403 Permission Denied Page

## Screenshots


# [Demo Video:](https://drive.google.com/open?id=1HMP0J7Cc1eVJgUE8Y4I-xI0gVeEcmyC5)

## Git setup
Install [Git](https://git-scm.com/)

Go to directory you want to work on

Clone Repository : 

    https://github.com/singhnk288/Django-CMS.git

## Python Setup 

    https://www.python.org/downloads/
    
## Activate Virtual Environment [more..](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)    
    
    venv\Scripts\activate    
    
Download all dependency if any missing:

    pip install -r requirements.txt    
    
    
CMS is platform independent so If you want to setup with SQL or NoSql then there is no any issue at all.

## Setup with MongoDb from -> django-cms\djfirst\settings.py find DATABASES
        
        DATABASES = {
            'default': {
                'ENGINE': 'djongo',
                'NAME': 'django-cms2',
                'HOST': 'mongodb://neeraj:neeraj@127.0.0.1:27017/?authSource=admin',
                'USER': 'neeraj',
                'PASSWORD': 'neeraj',
            }
    }
    
We Use djongo engine: NAME,HOST,USER,PASSWORD, please change according to your database

### Download djongo engine
        
        pip install djongo
        
## DB Migration 

        python manage.py migrate
        
## Create Super-User

        python manage.py createsuperuser
        
Enter Username:
Enter Password:
Enter Email:

## Run Django Project

        python manage.py runserver
        
        
### Screenshots

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/language_add.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/add_country.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/view_country.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/view_group.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/edit_permission.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/view_state_language1.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/view_state_language2.PNG)

![image](https://raw.githubusercontent.com/singhnk288/Django-CMS/master/django-screenshot/view_user.PNG)
