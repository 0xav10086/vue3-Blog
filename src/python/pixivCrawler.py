f = open('a.txt','r',encoding='utf-8')
s = f.read()
ls = s.split('。')
f.close()
print(ls)
ff = open('b.txt','w')
for i in ls:
    ff.write(i)
    print(i)
    ff.close