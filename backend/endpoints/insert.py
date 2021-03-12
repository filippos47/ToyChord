from flask import Response
from flask_restful import Resource, Api
from flask import Flask,request
from utils.common import compute_sha1_hash,check_responsible_set
from models import ChordNode,KeyValuePair
from database import db
import requests


class Insert(Resource):
    def post(self):
        key=request.args.get('key')
        value=request.args.get('value')
        hashed_key=compute_sha1_hash(key)
        my_identity = ChordNode.query.filter_by(hashed_id = compute_sha1_hash(request.host)).first()
        node_id=int(my_identity.hashed_id)
        pred_id=int(compute_sha1_hash(my_identity.predecessor))
        succ_id=int(compute_sha1_hash(my_identity.successor))

        if(check_responsible_set(node_id,pred_id,succ_id,hashed_key )):
          record=KeyValuePair.query.filter_by(hashed_id = str(hashed_key)).first()
          if  record == None:
                 record = KeyValuePair(chordnode_id = my_identity.id,hashed_id = str(hashed_key),value = value ,key=key)
                 db.session.add(record)
                 print(KeyValuePair.query.all())
                 db.session.commit()
                 return "record inserted"
                 
          else:
                 db.session.delete(record)
                 record = KeyValuePair(chordnode_id = my_identity.id,hashed_id = str(hashed_key),value = value,key=key)
                 db.session.add(record)
                 print(KeyValuePair.query.all())
                 db.session.commit()
                 return "record updated"

        ip_port=(my_identity.successor).split(":") 
        r = requests.post('http://'+ip_port[0]+':'+ip_port[1]+'/insert',params = {'key':key,'value':value})    
        return Response(r.text, status=200)
        



       