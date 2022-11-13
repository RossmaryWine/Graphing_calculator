import turtle
import re
import math
import string

#*****************************************************************************

list_num = []
list_sign = []
semi_list = []
scr = turtle.Screen()
scr.bgcolor("white")
scr.title("Turtle")
sket = turtle.Turtle()
sket.speed(10000)

def graph(): #draws the graph grids
  
  limit = 41
  
  sket.ht()
  sket.pu()
  sket.goto(-300, -300)
  sket.pd()
  x = sket.xcor()
  y = sket.ycor()
  
  for i in range(limit):
    if i == 0 or i == int(limit/2) or i == limit - 1:
      sket.pensize(3)
    else:
      sket.pensize(1)
    sket.fd(600)
    sket.pu()
    sket.goto(x, y + 15)
    sket.pd()
    y += 15
  
  sket.pu()
  sket.rt(90)
  y -= 15
  sket.goto(x, y)
  
  for i in range(limit):
    if i == 0 or i == int(limit/2) or i == limit - 1:
      sket.pensize(3)
    else:
      sket.pensize(1)
    sket.pd()
    sket.fd(600)
    sket.pu()
    sket.goto(x + 15, y)
    sket.pd()
    x += 15

  sket.pu()
  sket.goto(5, 0)
  sket.write("0")
  sket.goto(-1,304)
  sket.write("y")
  sket.goto(306, -5)
  sket.write("x")


#*****************************************************************************

def split(word): #splits a string into individual chars in a list
  return [char for char in word]

def extract(string_1, delimiters): # obtain all the delimiters in the order of their appearence in a list
  Temp = []
  temp2 = []
  temp2 = split(string_1)
  for i in range(1, len(temp2)):
    for j in range(len(delimiters)):
      if string_1[i] == delimiters[j]:
	      Temp.append(string_1[i])
  return Temp

#*****************************************************************************

def num_turn(strin): # returnes a float number excluding "x"
  return float(strin.translate({ord('x'): None}))


def element_calc(strin, x): # calculates each individual terms
  
  digits = list(string.digits)
  coefficient = 0
  power = 1
  temp = split(strin)
  
  if temp[0] == "x": # if only x exists without coefficients in the beninging
    strin = "1" + strin
  
  elif temp[0] == "-" and temp[1] == "x": # if only -x exists without coefficients in the beninging
    temp2 = strin.find("x")
    strin = strin[:temp2] + "1" + strin[temp2:]
  
  if "/" in strin:
    list_1 = strin.split("/")
    temp = split(list_1[1])
    
    if temp[0] not in digits: # used to handle ex: 1/x where the part after division is x with no coefficient
      list_1[1] = "1" + list_1[1]

    if "^" in list_1[1] and "x" in list_1[1]: #if the part after the division have both a power and x (*)
      temp = split(list_1[1])
      if temp[0] != "1":
        list_1[1] = list_1[1].split("^")
        coefficient = float(list_1[0])/(num_turn(list_1[1][0]))
        print(str(list_1[1][1]))
        power = float(list_1[1][1])
      else:
        res = element_calc(list_1[1], x)
        coefficient = element_calc(list_1[0], x)
        res = coefficient/res
        return res
    
    elif "^" in list_1[1]: # if the part after only have a power with no x*
      list_1[1] = list_1[1].split("^")
      coefficient = 1/pow((float(list_1[1][0])),float(list_1[1][1]))
      res = element_calc(list_1[0], x)
      res /= coefficient
      return res
    
    elif "x" in list_1[1]: # if the part after only have x with no power (*)
      temp = split(list_1[1])
      if temp[0] == "1":
        return element_calc(list_1[0],x)/x
      else:
        coefficient = element_calc(list_1[0],x)/num_turn(list_1[1])
      
    
    else: # if there is no special symbol after the division sign
      list_1[0] = list_1[0].split("^")
      coefficient = num_turn(list_1[0][0])/(num_turn(list_1[1]))
      if len(list_1[0]) > 1:
        power = float(list_1[0][1])

  else:
    list_1 = strin.split("^")
    # print(list_1), this line of code is used for debugging purposes
    coefficient = num_turn(list_1[0])
    if len(list_1) > 1:
      power = num_turn(list_1[1])

  if "x" in strin:
    res = pow(x, power)
    res *= coefficient
  else:
    res = pow(coefficient, power)

  return res

def get_tog(list_1, list_2):
  res = float(list_1[0])
  for i in range(len(list_2)):
    if list_2[i] == "+":
      res += float(list_1[i + 1])
    else:
      res -= float(list_1[i + 1])
  return res

#*****************************************************************************

def final_res(x, list_num, list_sign):
  final_list = []
  for i in range(len(list_num)):
    num = element_calc(list_num[i], x)
    final_list.append(num)
  res = get_tog(final_list, list_sign)
  return res

def draw(y1, y2):
    if res < -20:
      if y1 > y2 or (y1 < y2 and y2 > 20): 
        sket.goto(x*15, -300)
        sket.pu()
      else:
        sket.pu()
        sket.goto(x*15, -300)
        sket.pd()       
    elif res > 20:
      if y1 > y2 and y2 < -20:
        sket.goto(x*15, 300)
        sket.pu()          
      elif y1 > y2:
        sket.pu()
        sket.goto(x*15, 300)
        sket.pd()
      else:
        sket.goto(x*15, 300)
        sket.pu()  

graph()
delimiters = ["+", "-"]
res = 0

print("welcome to the graphing calculator,\
please input any polynomail functions\n")
listt = input("input the equation in the form of\n\
ax^n + bx^k +...+ c.  a, n, b, k, c could be any number\n")

temp = split(listt)

if temp[0] == "-":
  listt.replace('-', '', 1)

cut = '|'.join(map(re.escape, delimiters))
list_num = re.split(cut, listt, maxsplit=0)
list_sign = extract(listt, delimiters)

if temp[0] == "-":
  list_num.pop(0)
  list_num[0] = "-" + list_num[0]

x = -20
sket.pu()
sket.pensize(2)
sket.pencolor("red")
while x <= 20:
  res = final_res(x, list_num, list_sign)
  if res >= -20 and res <= 20:
    sket.goto(x*15, res*15)
    sket.pd()
  else:
    y1 = final_res(x, list_num, list_sign)
    y2 = final_res(x + 0.05, list_num, list_sign)

    draw(y1, y2)

  print(str(x) + "," + str(res))

  x += 0.1

#*****************************************************************************
