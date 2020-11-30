# Dynamic Pluggable Microservices Framework

I was told this particular Microservices Framework was just not possible unless it generated code dynamically but dynamic code generation, 
as cool as that can be, is just not required to get pluggable modules exposed as RESTful APIs.  Who knows maybe the Author, that's me,
might just know something about Python after-all.

Also keep in mind, this level of pluginess with minimal code without having to recompile the code as might be the case with Java, for instance,
is just not required for Python.

This Demo, is delivered without source to keep the real interesting bits hidden while focusing on the pluggability aspects.  One sample source file
is provided to show how to use the Framework to expose your functions via REST.  Only two HTTP Methods are currently supported and they are: GET and POST.
If there is enough interest in the Framework then the rest of the missing HTTP Methods will be added along with end-to-end security in the form of Encryption.

For security.  Dynamic Random Encryption can be provided to support Temporal Single-Use Tokens that work much like TOTP but are encrypted such that each
and every token is unique with a limited lifespan and single-use.

For database support.  MongoDB can be easily added and supported.  AWS DynamoDB can also be added and supported. And of course, any Database backend
supported by Django can also be added and supported.

You can expect to see this git repo to appear in a Docker Image soon. Stay tuned.

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

The beauty of this MicroService Architecture is the sheer simplicity of how it works.

Everything this MicroService Architecture does is done via pure Python and introspection.  

Everything in Python can be introspected including Modules.  Python can introspect a module to
learn about all the functions in the module.  Once you have all the functions you can use a decorator
to generate some META data to identify how each function can be accessed via the RESTful Interface.

The RESTful interface is also very simple.  One Object called a ServiceRunner and one RestAPI sub-class.  That's it.  Simple.

Some of the work done by the ServiceRunner is not well documented in the Python docs but it was also not difficult to cobble
together from various sources.

The current version supports GET and POST.  Future versions will support the rest of the HTTP Methods however it is more than possible to
build a working RESTful interface with just GET and POST, believe it or not.  Oh, I know there are those out there who have very definite
feelings about this but trust me when I say I was more than able to build a complete CRUD Interface using just one POST endpoint.  Doing this
made the code smaller and easier to maintain than the alternatives.

Rules:

GET functions take parameters as follows:

    GET http://127.0.0.1:8080/rest/services/hello-world/?a=1&b=2&c=3&d=4 HTTP/1.1

POST functions take parameters as follows:

    POST http://127.0.0.1:8080/rest/services/sample-one/ HTTP/1.1
    content-type: application/json

    {
        "args": [1,2,3,4,5,6],
        "name1": "one",
        "name2": "two",
        "name3": "three",
        "name4": "four"
    }

The typical Pythonic method for passing variable arguments to a function can be seen in this sample but this would have to be done
if one wished to publish functions via a RESTful Interface.

Any functions beginning with "__" will not be exposed as RESTful Endpoints.

Objects in the form of classes will not be exposed as RESTful Endpoints however you can add classes to yuour modules and then code
functions that can be exposed that can use any classes via their instances.  Again, this is how one would go about using Objects via
a RESTful Interface.

This interface is fully pluggable which means you can use whatever method you desire to plug new modules into the system and those modules
will be dynamically imported at run-time each time any endpoint is issued.

You may use the following endpoint to discover modules and endpoints known to the system:

    GET http://127.0.0.1:8080/rest/services/__dir__/ HTTP/1.1
    
Plugins:

Plug your modules into the folder called "plugins".  While the "plugins" folder could be placed anywhere it was placed under the "views" folder to facilitate
uploading modules via a RESTful Interface, at some point, however the version you are using does not support this.  A future version may have this feature in
the form on uploading specially encrypted modules to keep unwanted modules from being uploaded.  At present, you must install your "plugins"  manually which
should not pose any issues for you in case you wish to deploy this Microservices Architecture in Production.

Future Development:

Token-based Security.  Temporal Tokens, Randomly Encrypted.  Every token is unique.  Tokens are valid for a limite time, typically 60 seconds.  Tokens can only be used once.  This
type of Security is more secure than Oauth because Oauth Tokens require some time to invaidate and they can be used more than once.  For browser-based clients the Tokens are
generated by WASM code running deep in your browser.

Contact the developer (raychorn@gmail.com) for any specific requirements you may have for your deployments.

## Getting Started <a name = "getting_started"></a>

Make a virtual environment for Python. See the makevenv.sh file; point it at the Python, 3.8 or later, of your choice and then proceed with getting started.

Clone the git repo (git clone ...).

Install the requirements.txt via "pip install -r requirements.txt".

Cd microservices_framework

Run the server via "./runserver.sh".

See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

Install the requirements.txt via "pip install -r requirements.txt".

```
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

See [About](#about) for usage notes.

## Deployment <a name = "deployment"></a>

Deploy as you wish.
