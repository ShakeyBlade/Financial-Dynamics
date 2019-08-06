#linear regression and data plotting algorithm


#third priority is integrating threading such that both processes run concurrently
#fourth priority is making a GUI
#fifth and final priority is implementing machine learning techniques
import krakenex
import time
import datetime
import threading
from tkinter import *
from queue import Queue
key = krakenex.API()
key.load_key('kraken.key')
pair = 'XXBTZUSD'
init_price = 0
init_quant = 0
iterator = 1
root = Tk()
run_tot_price = 0
run_tot_quant = 0
pq_ratio = 0
prev_ratio = 0
count = 1
def updateGUI(text):
    GUISTR = Label(root, text = text)
    GUISTR.pack()

def compute_variance(price, quantity, average_price, average_quant):
    price_variance = price - average_price
    quant_variance = quantity - average_quant
    Least_Square_quant = (quant_variance)**2
    Least_Square_Price = (price_variance)*(quant_variance)
    final_Gradient = Least_Square_Price/Least_Square_quant
    final_offset = average_price - (final_Gradient * average_quant)
    print('Gradient:', final_Gradient, '          Offset:', final_offset )
    
def average(price, quantity, iterator):
    global run_tot_price
    run_tot_price += price
    global run_tot_quant
    run_tot_quant += quantity
    if(iterator > 2):
        run_avg_price = run_tot_price/iterator
        run_avg_quant = run_tot_quant/iterator
        compute_variance(price, quantity, run_avg_price, run_avg_quant)
    
def get_ticker_info(side):
    global pq_ratio
    global prev_ratio
    global iterator
    ticker_info = key.query_public('Depth', {'pair': pair})
    ticker_info = ticker_info['result'][pair][side] 
    ticker_price = float(ticker_info[0][0]) * float(ticker_info[0][1])
    ticker_quant = float(ticker_info[0][1])
    pq_ratio = ticker_price/ticker_quant
    if(pq_ratio != prev_ratio):
        print('recent trade:', ticker_info[0])
        print('trade no. ', iterator)
        average(ticker_price, ticker_quant, iterator)
        iterator+= 1  
        prev_ratio = pq_ratio
    return ticker_info
while True:
    get_ticker_info('asks')

updateGUI('relationship:')

