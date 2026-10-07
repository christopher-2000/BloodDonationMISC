# Blood Donation Forum (MKB Blood Donation Forum)

A Django website where the public can register as blood donors and search
for donors by blood group and location.

## Project structure

```
BloodDonation/
├── blooddonation/          # project settings/urls/wsgi
├── core/                   # main app
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── register.html
│   │   ├── search_donors.html
│   │   ├── about.html
│   │   └── success.html
│   ├── static/
│   │   ├── css/styles.css
│   │   ├── js/main.js
│   │   └── images/         # logos/images go here
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── models.py
│   └── admin.py
├── manage.py
└── db.sqlite3
```

## Pages

| URL            | Description                              |
| -------------- | ---------------------------------------- |
| `/`            | Home page                                |
| `/register/`   | Public donor registration form           |
| `/register/success/` | Registration confirmation          |
| `/donors/`     | Search donors by blood group + location  |
| `/about/`      | About the forum                          |
| `/admin/`      | Admin panel (manage donors)              |

## Setup

```bash
conda activate TEDLens
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Donor fields

Name, Age (18–65), House/Shop name, Blood group, Current location,
Phone, Last donated date.
