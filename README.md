# Udacity Fullstack Developer -Item catalog project

This is the last project in the Full Stack Web Developer nanodegree

## Overview

You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Software requirements

* [Python](https://www.python.org/downloads/release/python-2712/) - The code uses ver 2.7.12 or greater\
* [Vagrant](https://www.vagrantup.com/) - A virtual environment builder and manager\
* [VirtualBox](https://www.virtualbox.org/) - An open source virtualiztion product.\

Vagrant and VirtualBox are used to spin up an Ubuntu virtual machine containing Python 2.7.12 and PostgreSQL 9.5.19.

## JSON endpoints

The application provides the following json endpoints:
* http://localhost:5000/category/JSON - to list all categories
* http://localhost:5000/category/1/item/JSON - to list all items in a category
* http://localhost:5000/category/1/item/1/JSON - to list a specific item
* http://localhost:5000/catalog.json - to provide a list of all items in all categories

## How to run the project

1. Install VirtualBox from https://virtualbox.org
2. Install Vagrant from https://vagrantup.com
3. Install git-scm if you are using Windows environment
4. Clone the following git repo: https://github.com/udacity/fullstack-nanodegree-vm.
5. Open a terminal and go to the vagrant directory and run the command `vagrant up`
6. When the installation is done run `vagrant ssh` command to enter the vm.
7. Run `cd /vagrant`
8. Clone this repository inside that directory
9. Install the python modules needed by running `sudo pip install -r requirements.txt`
10. Setup the database by running `python project.py --setup`
11. Source the .env file or run `export GITHUB_OAUTH_CLIENT_ID=ff58f642022a20c8c7c1; export GITHUB_OAUTH_CLIENT_SECRET=8be86f808fb1234777f5c0152807e479848661b9`

12. Run this application with the command `python project.py`
13. Check the application by pointing your browser to 'http://localhost:5000'


## Known issues

* the .env file should not be commited to the repo but I added it so you can use it with ease instead of having to configure your own GitHub app.
* flashes were not implemented for actions on all pages
* duplicate items are allowed by design. (a simple check in the db with a flash message would fix this)
* the project requirements do not ask for the ability to add, edit or delete a cateogory so these features must be done via the database.
