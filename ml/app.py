"""

Flask
Internal api

"""

#import Core
import nltk
nltk.download('stopwords')
from flask import Flask,render_template,request,redirect,url_for,Response
import json
import senti as S
import tfidf 
import wordsimilarity as Ws
# import word_sim as spsim
import random

ch = "abcdefghijklmnopqrstuvwxyz123456789"
app = Flask(__name__)

class node():
   def __init__(self,na):
      self.id= randomnamegenarator()
      self.name = na

   def getID(self):
      return self.id

# class edges():
#    def __init__(self,n1,n2):
#       self.id = randomnamegenarator()
#       self.n1= n1
#       self.n2 = n2
   
#    def getN1(self):
#       return self.n1.getID()

#    def getN1(self):
#       return self.n2..getID()

# @app.route('/')
def happy():
   return "Running happily :)" 

@app.route('/api',methods = ['POST'])
def login():
   res = request.get_json()
   uID  = res["userId"]
   tID = res["therapistId"]
   notes = res["notes"]
   A = []
   for i in notes:
      A.append(senti_helper(i))
   B={
      "therapistId": tID,
      "userId": uID,   
   }
   X = CombSep(notes)
   X = tfidf.tfidf(X)
   X = Pairs(X)

   J =  Three_Ka_thing(notes)
   #return Response(json.dumps(user,indent=2),mimetype='application/json')
   print(len(J),len(notes))
   print(J)
   Z=[]
   for i in range(len(notes)-2):
      Z.append({"noteId":notes[i]["_id"],"time":notes[i]["date"],"words":J[i]})
   return Response(json.dumps({**B,"sentiment":A,"wordAnalysis":Z,**X}),mimetype='application/json')

def senti_helper(post):
   A = S.sentiment_analysis(post["content"])
   temp = {
      "noteId":post["_id"],
      "time":post["date"],
      "score":A
   }
   return temp

def CombSep(notes):
   B = []
   for i in notes:
      B.append(i["content"])
   return B

def breaker(A):
   Y = {0.05:0, 0.1:1, 0.3:2, 0.5:3, 0.7:4, 0.9:5}
   for i in Y:
      if A < i:
         return Y[i]

def Pairs(arr):
   B = []
   print(len(arr))
   arr = {k: v for k, v in sorted(arr.items(), key=lambda item: item[1])}
   print("here")
   Limit = 20
   for i in arr:
      print("in")
      if len(B) > Limit:
         break
      if arr[i] > 1:
         B.append(node(i))

   C = []
   print(len(B))
   for j in range(len(B)):
      for i in range(j,len(B)):
         if i!=j:
            tem = breaker(Ws.similar(B[i].name,B[j].name))
            
            if tem == None:
               tem =0

            if tem >= 4: 
               C.append({"id":randomnamegenarator(),
                "from":B[j].id,
                "to":B[i].id,
                "value":tem})

   Send = {"network":{
      "nodes":[{"id":i.id, "label":i.name} for i in B],
      "edges": C
   }}
   return Send

def randomnamegenarator():
   return "".join([random.choice(ch) for i in range(5)])

def Three_Ka_thing(notes):
   A = 3
   U = []
   for i in range(len(notes) - (A-1)):
      x = tfidf.tfidf(CombSep(notes[i:i+A]))
      y = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
      U.append(list(y.keys())[-5:])
   return U


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000,debug=True)


   #print(helper(T,tfidf.tfidf))
   
   #print(breaker(0.41))
   #print(ThreeKathing([I,J,K,L,M]))

