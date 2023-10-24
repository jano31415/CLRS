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
