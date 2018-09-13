API ArubaOS Switch Demo 

This is an API Demo that queries an Aruba OS Switch and allows the end-user to change which VLAN they are using for each port configured in the script. This script is a web frontend intend to show the power of our API with our switches. For more details on the demo, please see  the Arubapedia article.

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

Prerequisites

What software you need to install before running the script.

    Python 3.5+
    pip3
    pipenv
    A switch running 16.04+
    

Installing

The following are the steps to download and install the script.

    git clone https://github.hpe.com/michael-rose/API-Switch-Demo
    
    pipenv install 
    

Start-Up

First start the pipenv shell. Remember, this project is only intended to be used in a Demo or POC. It should not be used in Production.

    pipenv shell
    

Then start the Flask development webserver:

    python3 web.py

Configuration

Once the server is running, open the page in your browser: http://127.0.0.1:5000/config.

From here you'll edit the username, password, switch IP and other information. These settings are necessary to connect the webfrontend script to your switch. I highly recommend setting the port range to display otherwise, you'll list all 48 ports, which doens't look as clean.

The ports also need to be configured with one of the allowed VLANs. If you have ignored the VLANS (see below), this app will not let you make changes via this frontend. Please connect to your switch and configure the necessary VLAN ID, ports, etc before  using this app.

Click on Configure Ignored VLANS to hide VLANs that you don't want displayed. For example, your uplink or ports used in your lab for other items.

Built With

- Flask - The web framework used
- Bootstrap - Dependency Management

Contributing

When contributing to this repository, please first discuss the change you wish to make by posting in GitHub issues or email with the owners of this repository before making a change and requesting a pull request.

If you're interested in being a contributor, please let Michael Rose Jr know.

Authors

- Michael Rose Jr. - HPE GitHub

License

This project is licensed under the MIT License - see the LICENSE file for details

Acknowledgments

- Thanks for the SwitchingBot team for creating the initial python module that this frontend uses. 


