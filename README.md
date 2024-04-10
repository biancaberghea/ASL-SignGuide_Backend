# ASL E-Learning App

## 🚀 Description

This is an application that facilitates the learning process of the American Sign Language. The learning content is first divided in categories corresponding to differents parts of speech and then in corresponding categories for their meaning (eg: animals, colors, feelings). The learning process consists in watching videos where different people perform a sign for a given word. The app also offers a quiz functionality, where users have to perform a sign for a given word, which will be recorded by the device camera and evaluated as correct or incorrect with the help of an AI.

## 🖥️ Technologies
* `Angular`
* `Typescript`
* `HTML & CSS`
* `MySQL`
* `Python`
* `Flask`


    
## 🗝️ API architecture


The following is the top-level directory structure:
* App - Initialize flask app
* Db - Initialize the database connection with SQLAlchemy
* Model - Defines DTO and the tables to access with SQLAlchemy
* Repository - Communication with the database
* Service - Business logic layer
* Controller - Presentation layer containing the endpopints
* Config - Contains the configuration files for the entire application
	
⚙️ Database layer: The database layer stores data in a structured format that can be easily accessed and queried by the application layer.The application layer sends requests for data to the database layer through the data access layer. 

⚙️ Data layer: The data access layer is responsible for interacting with the data storage system, such as a database or file system.This will contain all entities, enums, exceptions, interfaces, types and logic specific to this layer.It provides an interface for the application layer to read and write data to the storage system.

⚙️ Business logic layer: This layer is responsible for implementing the business logic of the software system. It receives data from the presentation layer, processes it, and sends it to the data access layer for storage.This contains the interfaces of the services, that are used in the API layer, the services implementation, all the helpers classes, custom exceptions, guard clauses, domain events, handlers, basically all the business of the application.

⚙️ Presentation layer: The presentation layer is the topmost layer of a software system, responsible for rendering user interfaces and interacting with users. It communicates with the business logic layer to receive and send data.

⚙️ Client: The client refers to the user interface or the front-end of the application. It is responsible for presenting data and information to the user and for accepting user inputs.



## 🗝️ WEB architecture
The following is the top-level directory structure:

* Assets - global static assets like photos, svgs
* App - contains following folders:
    * Apps:contains all the components from the application,organized in modules, which enables lazy loading.
    * Auth:contains the login and register component
    * Utils:contains the roles directive, interceptor and guard

