# Dynamic Pluggable Microservices Framework - Deploy your own LAMBDA

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

### LAMDBA

This is exacly how AWS Lambda works.  You upload a module that contains a Python function and they magically expose that function via the web or they run it in response to some kind of event.
Either way, this is the magic behind AWS Lamdba for RESTful web services.  Serverless deployment of web services.  Build a Docker Container and put this framework inside and then spin-up your own Serverless Deployment of Python functions. Lamda.

This form of Lambda Serverless Deployment can be done with any Language or runtime that can be executed via a command line by crafting a function that issues a command line to run a Java class or a Node web head or almost any other type of runtime.

### Java or any other language other than Python

Keep in mind you can easily deploy Java or whatever functions using this Lamda framework by using Python to run your non-Python functions.  Again, this is an easy way to get your non-Python functions deployed via RESTful goodness.  Obviously there is a performance hit when running non-Python functions but that's life in the big city, so to speak.

### Docker Support coming soon.

See the docker image you can use to kick the tires or maybe use it to deploy.

```
docker pull raychorn/microservices-framework:version-tag
```
login to the docker container as root, there is no password.

Issue the following command to refresh the git clone:

```
git pull origin main
```

### URL Parameter Mapper

Refer to the .env file for the following:

```
NUM_URL_PARMS = 10  # Can be any number however the default is 10.
URL_PARM1 = parm_1  # Do not use dashes ("-") for parameter names. 
URL_PARM2 = parm_2
URL_PARM3 = parm_3
URL_PARM4 = parm_4
URL_PARM5 = parm_5
URL_PARM6 = parm_6
URL_PARM7 = parm_7
URL_PARM8 = parm_8
URL_PARM9 = parm_9
URL_PARM10 = parm_10
```

Now consider the following REST POST, this cannot be done for GET but can be done for PUT and DELETE:

```
POST http://127.0.0.1:8088/rest/services/v1/sample-one/1/2/3/4/5/6/7/8/9/10/?a=1&b=2&c=3&d=4 HTTP/1.1
content-type: application/json

{
    "args": [1,2,3,4,5,6],
    "name1": "one",
    "name2": "two",
    "name3": "three",
    "name4": "four",
    "__map__" : {
        "parm_1" : "p1",
        "parm_2" : "p2",
        "parm_3" : "p3",
        "parm_4" : "p4",
        "parm_5" : "p5",
        "parm_6" : "p6",
        "parm_7" : "p7",
        "parm_8" : "p8",
        "parm_9" : "p9",
        "parm_10" : "p10"
    }
}
```

The __map__ tells the system to remap all the URL Parameters from their old names to their new names.  This should make it easier for people to intigrate this framework into their current code-base.  The __map__ is stripped from the payload for the response.  This means you can remap every request, if necessary.


### Module Aliasing

Place the following in your modules to create an alias for your module.

```
__alias__ = "v1"  # this is the module's alias wwhich couldl also be a version identifier to support API Versioning.
```

Now you have API Versioning or the ability to hide the names of your modules from the outside world.

### Multiple HTTP Methods

Consider the following function signature:

```
@expose.endpoint(method='GET|PUT|POST', API='hello-world')
def foo(*args, **kwargs):
    pass
```

Notice the multiple HTTP Methods listed for the "method=" parameter.

The following function signature is also supported:

```
@expose.endpoint(method='GET|PUT|POST'.split('|'), API='hello-world')
def foo(*args, **kwargs):
    pass
```

Notice the multiple HTTP Methods listed for the "method=" parameter that is presented as a list.

Therefore the following function signature is also supported:

```
@expose.endpoint(method=['GET', 'PUT', 'POST'], API='hello-world')
def foo(*args, **kwargs):
    pass
```

Notice the multiple HTTP Methods listed for the "method=" parameter that is now stated to be a list.

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

HTTP Methods:

```
GET
The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.

GET is supported.
```

HEAD is not supported.
The HEAD method asks for a response identical to that of a GET request, but without the response body.

```
POST
The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.

POST is supported.
```

```
PUT
The PUT method replaces all current representations of the target resource with the request payload.

PUT is supported.
```

```
DELETE
The DELETE method deletes the specified resource.

DELETE is supported.
```

CONNECT is not supported.
The CONNECT method establishes a tunnel to the server identified by the target resource.

OPTIONS is not supported.
The OPTIONS method is used to describe the communication options for the target resource.

TRACE is not supported.
The TRACE method performs a message loop-back test along the path to the target resource.

PATCH is not supported.
The PATCH method is used to apply partial modifications to a resource.


### Rules:

GET functions take parameters as follows:

    GET http://127.0.0.1:8080/rest/services/hello-world/?a=1&b=2&c=3&d=4 HTTP/1.1

    OR

    GET http://127.0.0.1:8080/rest/services/hello-world/slug-or-numbers/ HTTP/1.1

    where the kwargs will have the query string or the extra parameters.


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
    
### Plugins:

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

See [About](#about) for more usage notes.

### URL Parameters  - See the .env file

```
NUM_URL_PARMS is the number of URL parameters - the default is 10 however this number can be adjusted.
```

### Named URL Parameters - See the .env file

The following states there are 10 URL Parameters and they are named.  By default all URL Parameters are of type "slug" which means they can be numbers, letters or dashes or any combination of these.

```
NUM_URL_PARMS = 10  # Can be any number however the default is 10.
URL_PARM1 = parm_1  # Do not use dashes ("-") for parameter names. 
URL_PARM2 = parm_2
URL_PARM3 = parm_3
URL_PARM4 = parm_4
URL_PARM5 = parm_5
URL_PARM6 = parm_6
URL_PARM7 = parm_7
URL_PARM8 = parm_8
URL_PARM9 = parm_9
URL_PARM10 = parm_10
```

These values can be dynamically modified via a POST, for instance, or PUT (PUTs are handled like POSTs).

URL Parameters are presented to your functions in the form of **kwargs, much like Query Parameters and POST/PUT/DELETE payload variables.

### API Versioning for a single API

Put your Version 1 functions in a module named v1 and then use the following URL Pattern:

```
GET http://127.0.0.1:8080/rest/services/v1/api-name/update/123456789/?a=1&b=2&c=3&d=4 HTTP/1.1
```

Put your Version 2 functions in a module named v2 and then use the following URL Pattern:

```
GET http://127.0.0.1:8080/rest/services/v2/api-name/update/123456789/?a=1&b=2&c=3&d=4 HTTP/1.1
```

### API Versioning for multiple APIs

Put your Version 1 functions in a module named product_v1 and then use the following URL Pattern:

```
GET http://127.0.0.1:8080/rest/services/product_v1/api-name/update/123456789/?a=1&b=2&c=3&d=4 HTTP/1.1
```

Put your Version 2 functions in a module named product_v2 and then use the following URL Pattern:

```
GET http://127.0.0.1:8080/rest/services/product_v2/api-name/update/123456789/?a=1&b=2&c=3&d=4 HTTP/1.1
```

API Versioning is optional however it can also be used to disambiguate API Names that may be the same in multiple modules however "API=" can also be used to 
differentiate and resolve this same issue.

### Unit Tests

Issue runserver.sh to start the server.

Issue run-tests.sh to run the tests.

Running tests works best via VsCode with the server running side-by-side with the tests in two different terminals.

The tests are known to execute with 100% success in my development environment.

## Deployment <a name = "deployment"></a>

Deploy as you wish.

### oAuth

If you want oAuth you may deploy oAuth via a Reverse-Proxy. oAuth is not sufficient for web-based security and it will not be supported by any frameworks published via [raychorn @ github](https://github.com/raychorn).

Whenever github sponsorship allows this repo to be sponsored you may have the option of sponsoring a strong form of web security in the form of Signed (Randomly encrypted) Single-Use Temporal Tokens that remain valid for a short period of time, say 30 seconds.  This option will be delivered with a Command Line interface to produce tokens for those who have clients not running via a browser. For browser-based clients there will be a WASM module that produces Tokens and of course the RESTFul Interface will be configurable to either require tokens or not.

The major weakness of oAuth is the lack of a Temporal component.

The client and server should work together using an mutually agreeable method of both validating and producing Tokens on the fly.  This is not the way oAuth works.
