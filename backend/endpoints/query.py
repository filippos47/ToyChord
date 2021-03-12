from flask import Response
from flask_restful import Resource, Api
from flask import Flask,request
from utils.common import compute_sha1_hash,check_responsible_set
from models import ChordNode,KeyValuePair
from database import db
import requests
import json

class Query(Resource):
    def get(self):
       key=request.args.get('key')
       hashed_key=compute_sha1_hash(key)
       my_identity = ChordNode.query.filter_by(hashed_id = compute_sha1_hash(request.host)).first()
       node_id=int(my_identity.hashed_id)
       pred_id=int(compute_sha1_hash(my_identity.predecessor))
       succ_id=int(compute_sha1_hash(my_identity.successor))
       ip_port=(my_identity.successor).split(":")
       #  Normal Query
       if key != '*':

          if(check_responsible_set(node_id,pred_id,succ_id,hashed_key )):
              record=KeyValuePair.query.filter_by(hashed_id = str(hashed_key)).first()
              if  record == None:
                    return "no such record"      
              else:
                    print(hashed_key)
                    return record.key+" "+record.value

          r = requests.get('http://'+ip_port[0]+':'+ip_port[1]+'/query',params = {'key':key})    
          return Response(r.text, status=200)
     #  Return all songs per node
       else:
            if request.args.get('id') == None:    
               accumulator={}
               node_data={}
               data=KeyValuePair.query.all()
               for record in data:
                  accumulator[record.hashed_id]=(record.key,record.value)
               node_data["Node id "+str(node_id)] =accumulator
               r=requests.get('http://'+ip_port[0]+':'+ip_port[1]+'/query',params={'key':key,'id':str(node_id)},json= node_data)  
               return r.json()
            else:
             if request.args.get('id')==str(node_id):
                  return request.json
             else:
                request_data=request.json
                node_data={}
                returned={}
                data=KeyValuePair.query.all()
                for record in data:
                    node_data[record.hashed_id]=(record.key,record.value)
                returned["Node id "+str(node_id)]=node_data
                merged={**returned,**request_data}
                r=requests.get('http://'+ip_port[0]+':'+ip_port[1]+'/query',params={'key':key,'id':request.args.get('id')},json= merged)
                return r.json()
               

            

