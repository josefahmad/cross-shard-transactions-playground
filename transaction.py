from pymongo import MongoClient
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo import ReadPreference

# For a replica set, include the replica set name and a seedlist of the members in the URI string; e.g.
# uriString = 'mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017/?replicaSet=myRepl'
# For a sharded cluster, connect to the mongos instances; e.g.
# uriString = 'mongodb://mongos0.example.com:27017,mongos1.example.com:27017/'

client = MongoClient("mongodb://127.0.0.1:27017/")
wc_majority = WriteConcern("majority", wtimeout=1000)

# Step 1: Define the callback that specifies the sequence of operations to perform inside the transactions.
def callback(session):
    collection = session.client.test.c

    # Important:: You must pass the session to the operations.
    collection.insert_one({'a': -1}, session=session)
    collection.insert_one({'a': 0}, session=session)

# Step 2: Start a client session.
with client.start_session() as session:
    # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or abort on error).
    session.with_transaction(
        callback, read_concern=ReadConcern('local'),
        write_concern=wc_majority,
        read_preference=ReadPreference.PRIMARY)
