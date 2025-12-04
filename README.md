# Pathshala-LMS 
Learning management system -LMS, built with **Django Rest Framework**, featuring **Role-Base Access Control (RBAC)**, ensuring secure authentication with **JWT Auth** and complete set of API endpoints for managing users, courses, enrollments, progress tracking, and interactions.
## Features

* **Role-Based Access Control (RBAC):** Supports three distinct user roles: **Admin**, **Teacher**, and **Student**.
* **Course Management:** Full CRUD operations for Courses, Modules, and Lessons managed by Admins/Teachers.
* **Enrollments:** Students can enroll in courses, access permissions and their enrollment status is tracked.
* **Progress Tracking:** Tracks student's lesson completion and calculates overall course progress.
.
* **Student Interaction:** Includes Q&A sections, course reviews and ratings, and certificate generation upon course completion.

## Architecture Overview

The backend is organized into five **Django apps** for maximum modularity and clean separation of concerns:

| App Name | Description | Key Models | Permissions |
| :--- | :--- | :--- | :--- |
| **`users`** | Manages the custom user model, authentication logic, and role-based access control. | `User` | Admin-only for user management; users manage their own profiles. |
| **`courses`** | Defines the entire course ecosystem, including categories, courses, modules, and lessons. | `Category`, `Course`, `Module`, `Lesson` | Admins create &  Admin/Teacher manage content; Students have read-only access. |
| **`enrollments`** | Handles student enrollments and payment tracking. | `Enrollment`, `Transaction` | Students manage their own enrollments. |
| **`progress`** | Tracks student progress through lessons and calculates course completion status. | `Progress` | Students update their own progress. Read-only for Teachers |
| **`interaction`** | Q&A, Reviews, and Certificates. | `Question`, `Answer`, `CourseReview`, `Certificate` | Mixed: Students ask questions and review courses; Teachers answer; Admins oversee certificates. |

## Tech Stack

* **Backend Framework:** Python 3.10+ , Django 5.x
* **API Framework:** **Django REST Framework (DRF)**
* **Database:** Configured for **SQLite** (local development) but easily scalable to **PostgreSQL**.
* **Authentication:** JWT  Authentication.

## Setup and Installation

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### 1. Clone the repository

```bash
git clone https://github.com/ImranChowdhury00/Pathshala-LMS.git
cd lms_project
```
### 2. Create and active virtual environment
```bash
pip install virtualenv
virtualenv env
Source ./env/Scripts/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Database migration
* Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
* (optinal) create superuser for admin panel
```bash
py manage.py createsuperuser
```
### 5. Run the server
```bash
python manage.py runserver
```
* open your browser or postman and navigate to : `http://127.0.0.1:8000/`


## Role-Based Access Control (RBAC)

The LMS uses Role-Based Access Control (RBAC) to ensure secure and organized access across the platform.


### Role Overview

* **Admin** – Full system control. Manages users, courses, categories, and certifications.

* **Teacher** – Manages course content and interacts with students and give answers.

* **Student** – Self registration. enrolls in courses, tracks progress, and engages through Q&A and reviews.
            
### RBAC Permissions 


| Action | Admin | Teacher | Student |
| :--- | :--- | :--- | :--- |
| **User Management** | **✓** | **✗** | **✗** |
| **Create Teacher Accountsr** | **✓** | **✗** | **✗** |
| **Self Registration** | **✗** | **✗** | **✓** |
| **Create Course & Category** | **✓** | **✗** | **✗** |
| **Create Modules & Lessons** | **✓** | **✓** | **✗** |
| **Enroll in Courses** | **✗** | **✗** | **✓** |
| **Update Own Progress** | **✗** | **✗** | **✓** |
| **Transaction** | **✓** | **✗** | **✓** |
| **Ask question** | **✗** | **✗** | **✓** |
| **Answer questions** | **✓** | **✓** | **✓** |
| **Course Review** | **✗** | **✗** | **✓** |
| **Issue Certificate** | **✓** | **✗** | **✗** |
| **View Own Data** | **✓** | **✓** | **✓** |


## 🔗 API Endpoints

All API endpoints are prefixed with `http://127.0.0.1:8000/`.

| Module | Resource | Method | Description |
| :--- | :--- | :--- | :--- |
| **Users** | `/users/register/` | GET, POST | Student registration. |
| **Users** | `/users/management/` | POST | All user management, creation. |
| **Courses** | `/courses/` | GET, POST, PUT, DELETE | CRUD for Courses, Modules, Lessons. |
| **Enrollments** | `/enrollments/` | GET, POST | Enroll a student into a course. |
| **Progress** | `/progress/` | GET, POST, PUT | Track and update lesson completion status. |
| **Interaction** | `/interaction/questions/` | GET, POST | Submit or retrieve course-related questions. |
| **Interaction** | `/interaction/answers/` | GET, POST | Submit or retrieve course-related answers. |
| **Interaction** | `/interaction/reviews/` | GET, POST | Course reviews and ratings. |
| **Interaction** | `/interaction/certificates/` | GET, POST | View certificates (Owner) or Issue certificates (Admin). |