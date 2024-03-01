# Designing Data Intensive Applications

I just write down some notes here from reading the book.

## Chapter 1: Reliable, Scalable and Maintainable Applications

Definition of the terms that we want to have for good data intensive applications:

Reliable: works as expected even in special situations e.g. faults in other systems
Scalable: can easily be adapted to work for higher load/more data. Important what kind of load
Maintainability: easy to operate, easy to understand for people maintaining it and easy to extend

## Chapter 2: Data Models and Query Languages

Rise of SQL in the 80s. Dominant data type until 2010 when NoSQL alternatives grew.
Criticism of SQL: object-relational mismatch. Usually we deal with objects that need information
from many different tables and thus we need an Object relational mapping (ORM) to get from the
relational table structure to the objects that we need in the application.

Alternative document store: e.g. store a json representation of the object. These are usually worse
with joining/referencing other data.

Graph DataBases: Consisting of nodes and edges and fast traversal of the graph is possible.
Every node and edge can store additional data key value.

Cypher: query language for neo4j. You can do queries where you can say follow the edges until you find something.
Since this path can have different length this is similar to a variable amount of joins in sql which needs recursive join feature.

triple storage: (joe, likes, Anna) only stores subject, predicate, object like edges or attributes of an object.

semantic web: idea to create a standard machine readable format and all websites store their data in
that format to be easily readable.

## Chapter 3: Storage and Retrieval

## Chapter 4: Encoding and Evolution
we often want to make changes to the data/schema/structure but its hard to make an instant switch.
Especially users might not immediately update. So we need forward and backward compatibility.
To send objects over the network or write them into a file you need to encode (serialize) them.
Whats the best way of doing so?
Serialize the byte object e.g. pickle
1)you commit to deserialize with the same programming language
2)the code is going to instantiate arbitrary classes -> security concern
3)versioning and can be slow e.g. java

Other human readable formats:
JSON:
- has problems with large numbers and byte strings (encode base64)
XML: i hate this format. verbose
csv: vague

there are binary encodings of json like Messagepack, BSON, BJSON ...
Messagepack:
If you want to encode {"user":"foo"}
you start with 8 for object? and then 1 for one field in json model (user). -> 81
Then specify with a that a string is next and that it has 4 letters -> a4
next 4 bytes are asci of the string. dont know by heart.
then a3 for next string with 3 letters and 3 ascii
81 a4 12 23 34 45 a3 12 23 34
integer get something else instead of a but basically this is how it works.

Thrift, Protofol Buffers: binary encoding with schema
See thrift_parser.py. Define the schema with type of data and order of fields.
Then you do not need to repeat the name of every field in the message.
You can specify the length of the numbers to save some space for small numbers to go to compact encoding.
We specify the index in the message so that we can send only some fields and also are able to extend.
(yes i did not implement this)

Avro: we dont specify numbers for the fields. But writer and reader schema can be different!
either specify the writer schema at the start of a large file
have version numbers and both applications no for each version number the evolution of the schema
good for database backup

data outlives code:
Be careful if an old application is updating a record that some new field the old application doesnt
know about is not removed since the old code doesnt know about it.

Rest: philosophy
simple formats, human radable, http features
Openapi/swagger to define the format

SOAP: using XML enoguh said

RPC: Remote Procedure Call -> like calling a function but somewhere else, idea hiding that this is a network call
-> network calls are different and fail often you need to anticipate
- if you dont get a response you dont know if the call succeeded
- speed slow and varies
