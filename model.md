# Document Project Model

This is the document that contains all the project information. It is divided by `components`, `models` and `flow`.

~~~json
{
    "project": "",
    "description": "",
    "components": [],
    "models": [],
    "flow": []
}
~~~

## Components

The whole set of instructions that make up the system are components.
Each screen is a component that contains n components. Each component contains a `name` and `parameters`.

~~~json
"components": [
    {
        "name": "myComponent",
        "parameters":{
            "foo": "bar",
            "myParam": "myValue",
        }
    }    
]
~~~

## Models

Here have the information persistence. Can be database, nosql and files. Each template is composed of the name and fields. Each field has its `field` name, `type` and `parameters`.

~~~json
"models": [
    {
        "name": "users",
        "fields": [
            {"field": "id", "type": "number",
                "parameters": {
                    "foo": "bar",
                    "myParam": "myValue"
                }
            },
            {"field": "name", "type": "string",
                "parameters": {
                    "tagTemplate": "input",
                    "typeElement": "text",
                    "label": "Name:"
                }
            },
            {"field": "password", "type": "string",
                "parameters": {
                    "tagTemplate": "input",
                    "typeElement": "password",
                    "label": "Password:"
                }
            }
        ]
    }    
]
~~~

## Flow

All connections between components.

~~~json
"flow": [
    {
        "componentIn": "screenDashboard",
        "componentOut": "screenUsers",
        "parameters": []       
    }    
]
~~~

## Parametros

Parameters differ according to the interpreter. Exist in `components`, `models` and `flow`
