# Overview

I am exploring new software tools to increase my knowledge and ability to solve unique software challenges.

This application serves as an address book. It provides a simple terminal interface allowing you to create, edit, delete, or view addresses. It uses a cloud database to persist the address book among instances of the application.

This project was created to explore the the capabilities and implementation of a cloud database.

[Software Demo Video](https://youtu.be/y8quUpUVkJQ)

# Cloud Database

This application utilizes a Cloud Firestore from Google Firebase.

A single collection represents the address book. Each document in the collection represents a single address. Each document has a city, state, street, and zip_code field.


# Development Environment

* Python 3.10.7 32 bit
* Firebase Admin SDK for Python (5.3.0)
* Visual Studio Code
* Git / Github

# Useful Websites

* [Cloud Firestore Quickstart](https://firebase.google.com/docs/firestore/quickstart)
* [Google Service Accounts Info](https://cloud.google.com/iam/docs/service-accounts)
* [Cloud Firestore Docs](https://firebase.google.com/docs/firestore)

# Future Work

* Implement pagination of display all addresses
* Implement a GUI
* Option to open address in Google Maps