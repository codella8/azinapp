# AZIN GROUP — Corporate Digital Platform

A professional Django-based corporate platform developed for **AZIN GROUP** to showcase company services, digital solutions, projects, and business capabilities.

The platform provides a structured content management system with multilingual support, custom administration tools, portfolio management, and a modern responsive interface designed for business presentation.

---

## Overview

AZIN GROUP is built with **Django 5** and provides a scalable foundation for corporate websites that require:

- Professional company presentation
- Service management
- Project portfolio showcase
- Multilingual content support
- Media management
- Custom admin dashboard
- Structured content management

The project separates business logic, content management, and presentation layers to maintain clean and maintainable architecture.

---

# Features

## Corporate Website

- Modern company landing pages
- Service presentation
- Business information sections
- Portfolio showcase
- Responsive user interface
- Structured content pages

---

## Portfolio & Project Management

- Dynamic project showcase
- Project categories
- Project images and media
- Admin-controlled portfolio content
- Flexible content updates

---

## Multilingual Support

The platform supports multilingual content management using:

- Persian
- English
- Tajik

Translation management is implemented using Django model translation features.

---

## Custom Administration System

The project includes a customized Django administration experience with:

- Content management
- Service management
- Portfolio management
- Media handling
- Improved admin interface using Django Jazzmin

---

# Technology Stack

## Backend

- Python
- Django 5
- Django ORM
- PostgreSQL / MySQL support

## Frontend

- HTML5
- CSS3
- JavaScript
- Responsive Design

## Libraries & Tools

- django-modeltranslation
- django-jazzmin
- Pillow
- WhiteNoise
- psycopg2
- PyMySQL

---

# Project Architecture




AZIN GROUP
│
├── azingroup/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── azinapp/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── admin.py
│ ├── templates/
│ └── static/
│
├── locale/
│ ├── fa/
│ ├── en/
│ └── tg/
│
├── media/
├── staticfiles/
├── manage.py
└── requirements.txt


---

# Admin & Content Management

The platform uses Django Admin as a content management system.

Administrators can manage:

- Company information
- Services
- Projects
- Images
- Website content
- Translated fields

The customized admin interface improves usability and makes content updates easier for non-technical users.

---

# Installation & Setup

## Clone Repository

git clone https://github.com/yourusername/azingroup.git

cd azingroup

# Create Virtual Environment
python -m venv .venv

source .venv/bin/activate

#For Windows:
.venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Apply Database Migrations
python manage.py migrate

# Create Admin Account
python manage.py createsuperuser

# Run Development Server
python manage.py runserver

# The application will be available at:
http://127.0.0.1:8000/

# Deployment

The project includes:

WSGI support
ASGI support
Static file handling with WhiteNoise
Database adapter support

It can be deployed using common Django production environments such as:

Gunicorn
Uvicorn
Nginx
VPS hosting solutions

# Purpose

This project demonstrates the development of a modern corporate platform using Django with:

Clean backend architecture
Database-driven content
Multilingual support
Custom administration tools
Professional business presentation

# Developer
Shamsia Mohammadi

Python Django Backend Developer

# Specialized in:

Django Applications
ERP Systems
Business Platforms
E-commerce Solutions
Database-driven Applications
License

This project is developed for AZIN GROUP.
