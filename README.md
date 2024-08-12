# Fruit Store Application

## Overview

The **Fruit Store Application** is a web application developed using FastAPI. It allows customers to log in, view a list of available fruits, add fruits to their cart, and view a summary of their cart. Owners can log in to manage the fruit inventory.

## Features

- **User Authentication:** Users can register and log in to the application.
- **Customer Dashboard:** Customers can view available fruits, add them to their cart, and see a summary of their selections.
- **MongoDB Integration:** The application uses MongoDB to store user data and fruit information.

## Directory Structure

```plaintext
Brit_Assesment/
│
├── .elasticbeanstalk/      # Elastic Beanstalk configuration files
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── Procfile                # Process file for deploying the application
├── README.md               # This README file
├── requirements.txt        # Python dependencies
├── app/                    # Main application code
│   ├── __init__.py
│   ├── auth.py             # Authentication utilities
│   ├── auth_routes.py      # Routes related to user authentication
│   ├── customer.py         # Routes for customer functionalities
│   ├── config.py           # Configuration and environment variables
│   ├── main.py             # Application entry point
│   ├── models.py           # Pydantic models for data validation
│   ├── static/             # Static files (CSS, JavaScript)
│   │   └── styles.css      # Stylesheet
│   ├── templates/          # HTML templates
│   │   ├── __init__.py
│   │   ├── customer_dashboard.html
│   │   ├── login.html
│   │   └── summary.html
│   └── routes/
             auth_routes.py #longin and register end points
             customer.py # user_dashboard, add_cart, view_cart and clear_cart
             
│
