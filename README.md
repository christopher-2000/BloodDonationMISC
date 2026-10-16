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



## Initiatives
Sahayavartha
Sahayavartha – A Small Act, A Greater Hope
Sahayavartha is a charitable initiative led by MISC Youth League, Ernakulam, with the aim of supporting those in need. Through this initiative, old newspapers are collected from church members and sold to scrap dealers. The funds raised are distributed among underprivileged and financially struggling individuals and families.
All church members are requested to bring their old newspapers to the church during the last week of every month and deposit them in the designated collection box.
Through this simple initiative, we turn unused newspapers into meaningful support for those in need, promoting charity, compassion, and community responsibility. Together, even a small contribution can make a big difference in someone's life.


Excellence Awards- The MISC Youth League Ernakulam annually organizes an appreciation programme to encourage and motivate students from our church community who have successfully completed their SSLC (10th) and Plus Two (12th) examinations. This initiative recognizes their academic achievements, celebrates their hard work and dedication, and inspires them to pursue higher education and achieve greater success in the future. Through this programme, the Maisy Youth League aims to support and motivate young minds to build a bright future.

Medical Camp - Youth League annually organizes a free medical check-up camp at the church premises for church members and people from the local community and nearby areas. This initiative aims to promote health awareness, encourage preventive healthcare, and provide access to basic medical check-ups for everyone. Through this community service, the Youth League strives to care for the well-being of people and serve society with compassion.

Carol Bells - Carol Bells is the annual Christmas celebration organized by the MISC Youth League Ernakulam, spreading the joy and blessings of Christmas throughout the church community. The programme begins in the first week of December, with the carol team visiting the homes of church members until December 24th. Each visit includes prayers led by the priest and melodious Christmas carol songs performed by the choir team. The celebration concludes on December with a vibrant Christmas roadshow through the church locality, bringing people together in the spirit of love, peace, unity, and Christmas joy.

The Youth League organized a grand Onam celebration at our church on Atham day. Everyone dressed in traditional Kerala attire to embrace the spirit of Onam. The celebration included many fun games and exciting activities, including tug-of-war, making the event joyful, memorable, and a wonderful opportunity for everyone to come together.