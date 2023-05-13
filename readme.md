# Querill

Querill is a GitHub project that provides a Django server for that allows you to search through your documents, ask a LLM questions about them and eventually it will speed up your entire worflow. This readme file will guide you on how to set up and run the Django server locally.

## Prerequisites

Before running the Querill Django server, make sure you have the following dependencies installed:

    Python 3 (recommended version: 3.7 or higher)
    pip package manager
    Django
    VDBForGenAI
    accelerate

Installation

To install the required dependencies, follow these steps:

    Clone the Querill repository from GitHub:


git clone https://github.com/jakubjdolezal/querill

Change into the project directory:


    cd querill

Create a virtual environment (optional, but recommended):

    python3 -m venv Querill

Activate the virtual environment:

For Windows:

    venv\Scripts\activate

For Unix/Linux:



    source venv/bin/activate

Install the required Python packages:

    pip install VDBForGenAI

Also follow the instructions as to how to get your Vicuna or other large language model.
How to get Vicuna can be found here:
https://github.com/lm-sys/FastChat

## Configuration

Before running the Django server, you need to configure the application. Follow these steps to set up the configuration:

    Open the config.json file in a text editor.

    Modify the configuration variables to match your environment. For example.

Running the Server

To start the Django server, follow these steps:

Activate the virtual environment (if you haven't done so already): 
For Windows:

    venv\Scripts\activate

For Unix/Linux:

    source venv/bin/activate

Run the database migrations to set up the database schema:

    python manage.py migrate

Start the Django server:

    python manage.py runserver

    Open your web browser and navigate to http://localhost:8000 to access the Querill application.

## Usage

Once the Django server is running, you can use the Querill application. Refer to the application's documentation or project-specific instructions for details on how to use the features provided by Querill.
## Contributing

If you would like to contribute to Querill, please follow the guidelines outlined in the project's CONTRIBUTING.md file.
## License

Querill is open-source software released under the MIT License. Please refer to the LICENSE file for more details.
## Support

If you encounter any issues or have questions regarding Querill, please create a new issue on the project's GitHub repository.
Acknowledgments

Querill relies on various open-source libraries and frameworks. We would like to express our gratitude to the developers and contributors of these projects for their valuable work.