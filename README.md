# Farm App

Welcome to the Farm App repository! This README provides essential information for setting up and using the Farm App project.
The project is written on Python and JavaScript in Pycharm. I am using Django framework.

## Table of Contents
- [Introduction](#introduction)
- [Files and Directories](#files-and-directories)
- [Setup and Installation](#setup-and-installation)
- [License](#license)
- [Contacts](#contacts)

## Introduction

The Farm App is store site for farmers and customers. In the site you can add various of farm products and then they can be bought. All the informations for product and orders is stored in your profile.

## Files and Directories

- `.idea`: This directory typically contains configuration files for JetBrains IDEs like PyCharm or IntelliJ IDEA. It's recommended to include this in your `.gitignore` file to avoid committing IDE-specific settings.
- `farm_app`: This directory contains the source code and files for Farm App project.
- `.gitignore`: This file specifies intentionally untracked files that Git should ignore. It's used to avoid including certain files in the repository, such as IDE configuration files or sensitive information.
- `LICENSE`: This file contains the license for the project
- `Procfile`: This file is used by Heroku to specify the commands that are executed by the app on startup.
- `requirements.txt`: This file lists the dependencies required by your Python project, typically used with pip for package management.
- `docker-compose.yml` : Defines the services, networks, and volumes for Docker Compose.

## Setup and Installation

If you want to see the full potential of the app like how the products are visualize, the profile of the farmer and his cart and orders - first you should set up the project, you need to create a profile and add products and then with another profile you can buy the existing products.

You need Docker, Bash CMD and existing database in PostgreSQL.

To set up and run the Farm App locally, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Sadito16/farm-repository-project.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd farm-repository-project/farm_app
    ```
3. **Ensure the Setup Script is Executable:**

   If you are using Git Bash or a similar terminal, make the `setup.sh` script executable:
    ```bash
    chmod +x setup.sh
    ```

4. **Run the Setup Script:**

    ```bash
    ./setup.sh
    ```

5. **Edit the `.env` File with Your Credentials Using the Examples:**

    Open the `.env` file in a text editor:
    ```bash
    vim .env
    ```
    You can use any text editor to modify the `.env` file as needed.

6. **Build Docker Containers:**

    ```bash
    docker-compose build
    ```

7. **Run Docker Containers:**

    ```bash
    docker-compose up -d
    ```

8. **Apply Migrations:**

    ```bash
    docker-compose run web python manage.py migrate
    ```

10. **Open Your Browser:**
   Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the app.

## Usage
Once the application is running, you can:

  - Add Products: Use the web interface to list farm products.
  - Manage Orders: Track and manage orders through you profile.
  - User Profiles: Create and manage user profiles


## License

This project is licensed under the [MIT License](LICENSE).

## Contacts

If you have any questions or feedback, feel free to reach out via email:

sadiahmedova02@gmail.com
