from extensions import Klient
import paho.mqtt.client as mqtt
import json
import sqlalchemy as sal

#Establishing connection to the database
engine=sal.create_engine("mysql+pymysql://sql4452256:jrzZ6YuNTR@sql4.freemysqlhosting.net/sql4452256")

#Establishing a connection to the database
engine.connect()



#@Klient.on_connect()
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    #books =User.query.filter(User.borrowed.any(Book.borrow==True)).first()
    #print(books.email)
    Klient.subscribe("libraryUUIDs")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

#@Klient.on_message()
def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    #reference from db and return the following
    bytes_value=msg.payload
    my_json=bytes_value.decode('utf8').replace("'", '"')
    data=json.loads(my_json)
    print(data)
    Dout=data["UUID"]
    print(Dout)
    data=Dout.replace(" ","")
    data2="' '"
    dataDisp=data2.replace(" ",data)
    q=f"SELECT * FROM book RIGHT JOIN user ON user.id=book.user_id WHERE tag={dataDisp}"
    r=engine.execute(q)
    k=r.fetchone()
    print(k)
    buzz=False
    if k is not None:
        bookname=k[2]
        username=k[6]
        meas = {"borrowerName":username,"book":bookname, "buzzer":buzz}
        ret= Klient.publish("libraryResponse",json.dumps(meas))
        return ret
    else:
        meas = {"borrowerName":"no user","book":"book not borrowed", "buzzer":buzz}
        ret= Klient.publish("libraryResponse",json.dumps(meas))
        return ret
    


Klient = mqtt.Client("testing")  # Create instance of client with client ID “digi_mqtt_test”
Klient.on_connect = on_connect  # Define callback function for successful connection
Klient.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
Klient.connect('broker.hivemq.com', 1883)
Klient.loop_forever()  # Start networking daemon