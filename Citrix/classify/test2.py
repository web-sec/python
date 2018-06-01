for i in csv_data[::-1]:
    if len(i)<14:
        n+=1
        csv_data.remove(i)

for i in csv_data[::-1]:
    illegal_data = ['No Applicable Component','Unspecified','Desktop VDA','Server VDA']
    if i[1] in illegal_data :
        n+=1
        csv_data.remove(i)
        print(n)

for i in csv_data[::-1]:
    illegal_data = ['n/a','N/A']
    if i[3] in illegal_data or i[4] in illegal_data:
        n+=1
        csv_data.remove(i)
        print(n)




title = csv_data[0]
csv_data.pop(0)
l = len(csv_data)
for i in range(l):
    print(i)
    description = ''
    resolution = ''
    token1 = get_final_tokens(csv_data[i][11])
    token2 = get_final_tokens(csv_data[i][12])
    for j in range(len(token2)):
        if rule.search(token2[j]):
            number = rule1.findall(token2[j])[0]
            token2[j] = re.sub(rule, number, token2[j])
        else:
            token2[j] = token2[j].replace('ctx','')
    for x in token1:
        description = description+' '+x
    for y in token2:
        resolution = resolution+' '+y
    csv_data[i][11] = description
    csv_data[i][12] = resolution
csv_data.insert(0,title)