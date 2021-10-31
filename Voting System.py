import datetime
import hashlib
import json
from flask import Flask, jsonify, render_template,request
exit_vote = False
A=0
B=0
C=0
Nota=0
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data=None,proof=1, previous_hash='0')

    def create_block(self,data, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'data':data,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1

        return True
app = Flask(__name__)
blockchain = Blockchain()
@app.route('/recieve_data',methods=['POST'])
def get_id():
   vote = request.form['vote']
   cast_vote(vote)
   return f'<h1>Vote has been casted to:{vote}</h1> <h2>Go back to home page:?</h2> <form action="/"><button type="submit">Home</button></form>'
def cast_vote(data):
    global A,B,C,Nota
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(data, proof, previous_hash)
    if data =="A":
        A+=1
    elif data == "B":
        B+=1
    elif data == "C":
        C+=1
    else:
        Nota+=1
    return block
@app.route('/',methods=['GET', 'POST'])
def home():
    if exit_vote == True:
        return "<h1>Voting is Over</h1>"
    return render_template('index.html')
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
@app.route('/exit_voting',methods=['GET'])
def exit():
    global exit_vote,A,B,C,Nota
    exit_vote=True
    print ("Exit voting system")
    if Nota>A and Nota>B and Nota>C:
        return ("<h1>Re election</h1>")
    elif A>B:
        if A>C:
            return (f"<h1>A is the winner by getting {A} votes</h1>")
        else:
            return (f"<h1>C is the Winner by getting {C} votes</h1>")
    elif B>C:
        return (f"<h1>B is the Winner by getting {B} votes</h1>")
    elif A==B==C:
        return ("<h1>Tie</h1>")
    else:
        return (f"<h1>C is the Winner by getting {C} votes</h1>")

app.run(host='127.0.0.1', port=7000)

