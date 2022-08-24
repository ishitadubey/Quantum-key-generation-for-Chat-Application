from flask import Flask,request
import blowfish
from flask_cors import CORS
from qiskit import QuantumCircuit, Aer, transpile, assemble
from numpy.random import randint
import numpy as np
import base64

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
envAuthKey = "123authkey123"

@app.route('/')
def home():
  return "I like food better than your face"

  
@app.route('/generate')
def send_key():
  auth_key = request.headers.get("authKey")
  if(auth_key!=envAuthKey):
    return {
      "msg":"Access Denied!!!"
    }
  block = alice()
  key = b"123secretkey123"
  b1 = bytes(listToString(block[0:8]),'utf-8')
  b2 = bytes(listToString(block[8:16]),'utf-8')
  b3 = bytes(listToString(block[16:24]),'utf-8')
  b4 = bytes(listToString(block[24:32]),'utf-8')
  cipher = blowfish.Cipher(key)
  ciphertext1 = cipher.encrypt_block(b1)
  ciphertext2 = cipher.encrypt_block(b2)
  ciphertext3 = cipher.encrypt_block(b3)
  ciphertext4 = cipher.encrypt_block(b4)
  ciphertext = ciphertext1+ciphertext2+ciphertext3+ciphertext4
  ct = base64.b64encode(ciphertext)
  return ct
  
def listToString(s):   
  str1 = ""   
  for ele in s:
    str1 += str(ele)  
  return str1

def alice():
  np.random 
  global n
  n = 100
  alice_bits = randint(2, size=n)
  alice_bases = randint(2, size=n)
  message = encode_message(alice_bits, alice_bases)
  bob_bases = randint(2, size=n)
  bob_results = measure_message(message, bob_bases)
  alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
  bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
  sample_size = 32
  bit_selection = randint(n, size=sample_size)
  bob_sample = sample_bits(bob_key, bit_selection)
  alice_sample = sample_bits(alice_key, bit_selection)
  return alice_sample


def encode_message(bits, bases):
  message = []
  for i in range(n):
    qc = QuantumCircuit(1,1)
    if bases[i] == 0: 
      if bits[i] == 0:
        pass 
      else:
        qc.x(0)
    else: 
      if bits[i] == 0:
        qc.h(0)
      else:
        qc.x(0)
        qc.h(0)
    qc.barrier()
    message.append(qc)
  return message

def measure_message(message, bases):
  backend = Aer.get_backend('qasm_simulator')
  measurements = []
  for q in range(n):
    if bases[q] == 0: 
      message[q].measure(0,0)
    if bases[q] == 1: 
      message[q].h(0)
      message[q].measure(0,0)
    qasm_sim = Aer.get_backend('qasm_simulator')
    qobj = assemble(message[q], shots=1, memory=True)
    result = qasm_sim.run(qobj).result()
    measured_bit = int(result.get_memory()[0])
    measurements.append(measured_bit)
  return measurements

def remove_garbage(a_bases, b_bases, bits):
  good_bits = []
  for q in range(n):
    if a_bases[q] == b_bases[q]:
      good_bits.append(bits[q])
  return good_bits

def sample_bits(bits, selection):
  sample = []
  for i in selection:
    i = np.mod(i, len(bits))
    sample.append(bits.pop(i))
  return sample


if __name__ == "__main__":
    app.run(debug=False)
