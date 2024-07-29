# Medical Missions to Peru Website

## Description
This project is a web application for Medical Missions to Peru. It allows an admin user to create and edit text and image blocks on the website.

## Features
- Admin login and authentication
- Create, edit, and delete text blocks
- Upload, edit, and delete image blocks
- Responsive design for mobile and desktop

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.7 or higher
- You have a basic understanding of Flask
- You have installed [any other required software or tools]

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/medical-missions-peru.git
    cd medical-missions-peru
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration
1. Create a `.env` file in the root directory and add the following configuration variables:
    ```ini
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```

2. Modify the `init_database.py` file with the admin email and password to set up the initial admin account.

## Running the Application
1. Run the Flask development server:
    ```sh
    flask run
    ```

2. Open a web browser and go to `http://127.0.0.1:5000`.

## Admin Access
1. To log in as an admin, go to the home page and add `/login` to the URL: `http://127.0.0.1:5000/login`.
2. Use the admin credentials specified in the `init_database.py` file.

## Testing
1. To run the tests, use the following command:
    ```sh
    pytest
    ```

## Deployment
To deploy this application, you can use platforms such as Heroku, AWS, or any other cloud provider. Please refer to their respective documentation for deployment instructions.

## Contributing
To contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Create a pull request.

## Contact
If you want to contact us, you can reach us at:
- Jorge Núñez Paucar: jorge.nunez.paucar@ucsp.edu.pe
- Oscar Quispe Mallma: oscar.quispe.mallma@ucsp.edu.pe
