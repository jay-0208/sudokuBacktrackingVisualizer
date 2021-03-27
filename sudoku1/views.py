from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
import math
import requests
def check(grid,xx,yy,s,num,sr):
    xt,yt=(xx//sr)*sr,(yy//sr)*sr
    for i in range(xt,xt+sr):
        for j in range(yt,yt+sr):
            if grid[i][j]==num:
                return False
    for i in range(s):
        if grid[xx][i]==num or grid[i][yy]==num:
            return False
    return True
def home(request):
    url = 'http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=%d&level=%d'
    params = {'size': 9, 'level': 2}
    r = requests.get(url, params=params)
    b = r.json()
    print(b)
    s=9
    sr=3
    square=[]
    x=[[-1 for i in range(s)] for j in range(s)]
    for i in range(len(b['squares'])):
        x[b['squares'][i]['x']][b['squares'][i]['y']]=b['squares'][i]['value']
        square.append([b['squares'][i]['x'],b['squares'][i]['y'],b['squares'][i]['value']])
    bit = [[1 for i in range(s)] for j in range(s)]
    emp=[]
    for i in range(s):
        for j in range(s):
            if x[i][j] == -1:
                emp.append([i, j])
    check1 = [-1] * len(emp)
    it = 0
    ans = True
    path=[]
    while (it < len(emp)):
        for i in range(bit[emp[it][0]][emp[it][1]], s + 1):
            state = check(x, emp[it][0], emp[it][1], s, i, sr)
            if state == True:
                bit[emp[it][0]][emp[it][1]] = i
                x[emp[it][0]][emp[it][1]] = i

                path.append([emp[it][0],emp[it][1],i])
                it += 1
                break
            elif i == s:
                bit[emp[it][0]][emp[it][1]] = 1
                x[emp[it][0]][emp[it][1]] = -1
                path.append([emp[it][0], emp[it][1], i])
                it -= 1
        if it == -1:
            ans = False
            break
    print(ans)
    print(x)
    if ans==True:
        js=[1,square,path]
        b={'js' : js}
        return render(request, 'main.html',b)
    else:
        js=[0]
        b = {'js': js }
        return render(request, 'main.html', b)
