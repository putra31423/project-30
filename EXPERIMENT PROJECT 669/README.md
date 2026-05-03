# Surf Instructor Website

A responsive website for a Surf Instructor built with Python (Flask), SQLite, and vanilla HTML/CSS/JS.

## Features

- **Responsive Design**: Works on mobile, tablet, and desktop.
- **Booking System**: Inquiries are saved to a local SQLite database.
- **Services & Packages**: Display of surf lessons and pricing.
- **Reviews**: Student testimonials.
- **Social Media**: Quick links to WhatsApp, Instagram, TikTok, and YouTube.

## Prerequisites

- Python 3.x installed.

## Setup & Installation

1.  **Install Dependencies**
    Open your terminal and run:

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: If `pip` doesn't work, try `python3 -m pip install -r requirements.txt`)_

2.  **Run the Application**
    Start the Flask server:

    ```bash
    python3 app.py
    ```

3.  **Access the Website**
    Open your browser and go to:
    0 [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Database

The application uses a SQLite database (`surf_instructor.db`) which is automatically created when you run the app for the first time.

## Project Structure

- `app.py`: Main Flask application.
- `models.py`: Database models.
- `templates/`: HTML files.
- `static/`: CSS and JavaScript files.
