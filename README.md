Table of Contents
1.	Project Overview
2.	Features
3.	Technologies Used
4.	System Requirements
5.	Installation Guide
6.	Database Schema
7.	API Endpoints
8.	User Roles and Permissions
9.	Notification System
10.	Testing
11.	Deployment
12.	Future Enhancements
13.	Screenshots
14.	Project Repository
15.	Project Overview
The Child Vaccination-Immunization Programme is a web application aimed at managing and tracking child vaccination schedules. The system allows hospital admins and users to register children, update their information, and notify parents about upcoming vaccinations.
Features
•	Child registration and information management
•	Admin and user authentication and management
•	Vaccination scheduling and tracking
•	Automatic email notifications for upcoming vaccinations
•	User-friendly interface for hospital staff and parents
Technologies Used
•	Backend: Python, Django
•	Frontend: HTML, CSS, JavaScript
•	Database: MySQL
•	Task Queue: Celery
•	Message Broker: Redis
•	Version Control: GitHub

16.
System Requirements
•	Python 3.8 or higher
•	MySQL 5.7 or higher
•	Redis server
•	Celery 5.3.6
•	Django 5.0.1

17.
Installation Guide
1.	Clone the repository:
git clone https://github.com/ROHITKUMBHAR6800/children_vaccination
cd children_vaccination
2.	Create a virtual environment and activate it:
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
3.	Install the required packages:
pip install -r requirements.txt
4.	Set up the MySQL database:
CREATE DATABASE child_vaccination;
5.	Update the settings.py file with your database credentials.
6.	Apply migrations:
python manage.py migrate
7.	Run the development server:
python manage.py runserver
8.	Start Redis server and Celery worker:
redis-server
celery -A PRIMARY_HEALTH_CENTER worker --loglevel=info
18.
Database Schema
The project uses the following database schema:
Admin
•	admin_id: CharField (Primary Key)
•	hospital_name: CharField
•	mobile_no: CharField
•	email: EmailField
•	area_add: CharField
•	village_town: CharField
•	pincode: CharField
•	tehsil: CharField
•	district: CharField
•	state: CharField
•	password: CharField
•	email_verify: CharField
•	otp: CharField
Users
•	user_id: CharField (Primary Key)
•	admin_id: CharField
•	user_name: CharField
•	middle_name: CharField
•	surname: CharField
•	gender: CharField
•	mobile_no: CharField
•	email: EmailField
•	home_add: CharField
•	village: CharField
•	pincode: CharField
•	tehsil: CharField
•	district: CharField
•	state: CharField
•	password: CharField
•	email_verify: CharField
•	otp: CharField
Child
•	child_id: CharField (Primary Key)
•	register_by: CharField
•	child_name: CharField
•	father_name: CharField
•	surname: CharField
•	mother_name: CharField
•	birth_date: DateField
•	gender: CharField
•	mobile_no: CharField
•	email: EmailField
•	home_add: CharField
•	village: CharField
•	pincode: CharField
•	tehsil: CharField
•	district: CharField
•	state: CharField
•	email_verify: CharField
•	otp: CharField
ChildVaccination
•	child: ForeignKey (to Child)
•	email: EmailField
•	vaccination_1month: CharField
•	vaccination_2month: CharField
•	vaccination_3month: CharField
•	vaccination_6month: CharField
•	vaccination_7month: CharField
•	vaccination_8month: CharField
•	vaccination_9month: CharField
•	vaccination_12month: CharField
•	vaccination_15month: CharField
•	vaccination_18month: CharField
•	vaccination_24month: CharField
•	vaccination_36month: CharField
•	vaccination_48month: CharField
•	vaccination_60month: CharField
19.
API Endpoints
The following are some of the key API endpoints:
•	GET /adminLoginForm/: Admin login form
•	POST /signupAdmin/: Admin registration
•	GET /userLoginForm/: User login form
•	POST /signupUser/: User registration
•	POST /signupChild/: Child registration
•	POST /vaccRemainderMail/: Send vaccination reminder email
User Roles and Permissions
Admin
•	Register and manage users
•	Register and manage children
•	Update vaccination schedules
•	View and delete user and child information
User
•	Register children
•	View and update child information
•	Receive vaccination reminders
Notification System
•	The system uses Celery to schedule and send email notifications.
•	Notifications are sent based on the vaccination schedule to remind parents of upcoming vaccinations.
•	Redis is used as the message broker for Celery tasks.
Testing
•	Unit tests for models, views, and forms
•	Integration tests for API endpoints
•	Use Django's built-in testing framework for running tests
Deployment
•	Ensure MySQL and Redis servers are running
•	Use Gunicorn or uWSGI for serving the Django application
•	Configure Nginx as a reverse proxy
Future Enhancements
•	SMS notifications in addition to email notifications
•	Multi-language support for the user interface
•	Detailed analytics and reports on vaccination coverage
•	Mobile application for easier access
Project Repository
•	GitHub Repository

