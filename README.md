Online Library
=======================
This website represents an online library with a backend and a frontend.
The page is responsive, which means it can be viewed on mobile devices.

Backend
--------------------
In the backend (.../admin) the admin user can search for items which are grouped into categories. 

**Category: Auth**

The admin user can search for groups and users. 
Groups and users can be added or deleted. 
The user's details can be edited and assigned to groups.
A user can be deactivated as well.

**Category: Booklib**

The admin user can search for Authors, Books and Categories.
Authors can be added, edited and deleted.
Books can be added, edited, deleted, Authors can be assigned and the image as well as the file can be uploaded.
Categories can be added, edited, deleted and deactivated.
The order of categories can be defined.
Categories can have a parent category.

**Category:Registration**

The user ID and the Activation Key of the currently registered users can be found in 'Registration Profiles'.
Registrations can be added, deleted, activated and the activation email can be resent again.

**Category: Sites**

Under Sites the links are stated which provide access to the website.
It is used to provide the right link in the registration process.
Those links can be added, edited and deleted. 

The admin user can change his password in the backend and he can logout as well.


Frontend
--------------------
In the frontend a user can either register or login on the home page.
A user who is not logged in can search and browse for books, but cannot access the details page. 

**Menu point: Search**

The user can search for book titles, authors, categories and text passages in the description of the book. 
By clicking on the title or the book image, the user is navigated to the details view of the book.

**Menu point: Browse**

In the browse view, all books are listed grouped by their category.
On the left hand menu, the categories are listed. 
In brackets, the number of books in the corresponding category is displayed.
By clicking on the title or the book image, the user is navigated to the details view of the book.

**Details view**

In the details view, the cover image, title, authors, description and the category are displayed.
A book can be added to the favorites (or removed if it is already a favorite).
The book can be downloaded as PDF file.
A user has 10 free downloads per month (the number of downloads left is displayed next to the download button).
	
**Menu point: Profile (user name)**

In the profile, the user can take a look at his favorites. 
By clicking on the title, the user is navigated to the details view of the book.
A favorite can also be deleted in the profile.
In the settings tab of the profile, the user can change his password.

Technical Directions
---------------------
**Openshift**

Openshift offers hosting possibilities for various applications for free. It is possible to log in via ssh, and use port-forwarding for the database.

In order to use Openshift, an account is necessary. Afterwards, the rhc-app has to be installed:
https://www.openshift.com/developers/rhc-client-tools-install

With that, port-forwarding can be used:

	rhc port-forward –a python

The ssh-link is visible on the Openshift page within the application.

In the setup.py file, all the installed apps are listed. They are used on the Openshift server, but this file is also useful for local development.


**Database**

A MySQL database hosted on Openshift is used. Port-forwarding has to be enabled for local development.

phpMyAdmin is also installed on Openshift, in case a look into the database is desired.

In the settings.py the port is specified and may have to be adjusted depending on the port-forwarding.

**Search**

The search relies on Whoosh (a python search engine) and haystack as a middle layer. In order for the search index to rebuild, the following command has to be used in order to add new books:

	manage.py update_index


**E-Mails**
A gmail-account is used to send e-mails instead of an own smtp-server. The data is specified in the settings.py file.


**Setup.py**
Here, additional apps have to added in order to work on Openshift when pushing it on the server.







