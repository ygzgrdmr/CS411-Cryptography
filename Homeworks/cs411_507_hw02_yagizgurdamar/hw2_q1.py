import random
import requests

import math
API_URL = 'http://harpoon1.sabanciuniv.edu:9999/'

# Change your id here
my_id = 22534


def getQ1():
  endpoint = '{}/{}/{}'.format(API_URL, "Q1", my_id )
  response = requests.get(endpoint) 	
  if response.ok:	
    res = response.json()
    print(res)
    n, t = res['n'], res['t']
    return n,t
  else: print(response.json())

print(getQ1())
'''
def checkQ1a(order):   #check your answer for Question 1 part a
  endpoint = '{}/{}/{}/{}'.format(API_URL, "checkQ1a", my_id, order)
  response = requests.put(endpoint) 	
  print(response.json())

def checkQ1b(g):  #check your answer for Question 1 part b
  endpoint = '{}/{}/{}/{}'.format(API_URL, "checkQ1b", my_id, g )	#gH is generator of your subgroup
  response = requests.put(endpoint) 	#check result
  print(response.json())

def checkQ1c(gH):  #check your answer for Question 1 part c
  endpoint = '{}/{}/{}/{}'.format(API_URL, "checkQ1c", my_id, gH )	#gH is generator of your subgroup
  response = requests.put(endpoint) 	#check result
  print(response.json())

'''


def phi(n):
  amount = 0
  for k in range(1, n + 1):
    if math.gcd(n, k) == 1:
      amount += 1
  return amount

def checkQ1a(order):   #check your answer for Question 1 part a
  endpoint = '{}/{}/{}/{}'.format(API_URL, "checkQ1a", my_id, order)
  response = requests.put(endpoint)
  print(response.json())


checkQ1a(phi(433))
print("my answer is 433 for Q1 A")

def checkQ1b(g):  #check your answer for Question 1 part b
  endpoint = '{}/{}/{}/{}'.format(API_URL, "checkQ1b", my_id, g )	#gH is generator of your subgroup
  response = requests.put(endpoint) 	#check result
  print(response.json())


