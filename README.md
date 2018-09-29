# Web Application Project

I have created a structure for presenting items(objects) on a web page.
It could have been any presentation (Shop, Storage information, etc.), but I chose to present a list of phones which in my opinion, 
everyone should consider if they are looking to get a good deal. The smartphones market has gone up tremendously in the last years, 
and instead of paying for an overpriced phone, I think people should consider the chinese alternatives as they have the same hardware
capabilites but are much cheaper.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Specification for the project:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Languages used: Python, HTML, CSS, JS
Applications used: Flask, MongoDB, DataTables


- A local Database, preferably using a NOSQL approach, and for which I chose MongoDB. (others include CouchDB, CouchBase, etc.)

- The application is held running on a local fast deployment server called Flask, which I manage using Python.

- Dinamically generated web pages (using Flask), based on the URL accesed or the requests I'm getting from the user.

- The data is being extracted from the database using views. (the query method of NOSQL) 

- Then, the data is presented in tables, and for that I chose DataTables. (easy to use plug-in to present your data)

