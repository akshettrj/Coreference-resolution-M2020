from __future__ import unicode_literals
from isc_parser import Parser
parser = Parser(lang='hin')
text = '''कम्प्यूटर बाबा पर कार्रवाई:शिवराज सरकार के खिलाफ यात्रा निकालने वाले कम्प्यूटर बाबा का आश्रम तोड़ा , बाबा को जेल भेजा
मध्य प्रदेश के इंदौर में नामदेव दास त्यागी ( कम्प्यूटर बाबा ) के खिलाफ रविवार को अवैध कब्जे के मामले में कार्रवाई की गई । 
बाबा के गोम्मट गिरी वाले आश्रम को प्रशासन ने तोड़ दिया और बाबा को प्रिवेंटिव डिटेंशन के तहत हिरासत में लेकर जेल भेज दिया । 
कम्प्यूटर बाबा वही हैं जिन्होंने हाल ही में मध्य प्रदेश की 28 सीटों पर हुए उपचुनाव में शिवराज सरकार के खिलाफ लोकतंत्र बचाओ यात्रा भी निकाली थी ।
प्रशासन ने 2 महीने पहले नोटिस दिया था
इंदौर में एयरपोर्ट रोड पर जम्बूडी हप्सी गांव में बाबा का आश्रम था । 
आरोप हैं कि गौशाला की 46 एकड़ जमीन पर कब्जा कर इसमें से 2 एकड़ जमीन पर आश्रम बना दिया गया । 
प्रशासन ने 2 महीने पहले कंप्यूटर बाबा को नोटिस देकर कागज पेश करने को कहा था । 
2 हजार रुपए का फाइन लगाकर कब्जा हटाने के लिए भी कहा था ।
बाबा की तरफ से न तो कागज पेश किए गए, न ही कब्जा हटाया गया । 
ऐसे में ADM अजयदेव शर्मा रविवार सुबह नगर निगम की टीम और पुलिस के साथ मौके पर पहुंचे और आश्रम तुड़वा दिया । 
विरोध की आशंका को देखते हुए पुलिस ने बाबा और उनके 4 सहयोगियों को पहले ही हिरासत में ले लिया था ।
कम्प्यूटर बाबा ने दिग्विजय सिंह के लिए यज्ञ करवाया था'''
origText = text
text = text.split('।')
for t in range(len(text)):
    text[t] = text[t].replace(":", " : ").replace(",", " , ")

mention = []
allmention = []
#MENTION-DETECTION SIEVE
print("------------MENTIONS FOUND-----------")

for i in text:
    tree = parser.parse(i.split())
    #print('\n'.join(['\t'.join(node) for node in tree]))
    for node in tree:
        newmention = ''
        #print(node[1])
        if (node[4]=='NN' or node[4]=='NNP' or node[4]=='NNPC' or node[4]=='NST') and (tree[int(node[6])-2][4]=='NST' or tree[int(node[6])-2][4]=='NNP' or tree[int(node[6])-2][4]=='NNPC' or tree[int(node[6])-2][4]=='NP'):
            for x in range(int(node[0])-1, int(tree[int(node[6])][0])-1):
                newmention += (tree[x][1].replace(')', '').replace('(', "") + ' ')
            mention.append(newmention)
            allmention.append(newmention)
        elif (node[4]=='NN' or node[4]=='NNP' or node[4]=='NNPC' or node[4]=='NST'):
            b=False
            for m in mention:
                if (node[1]== m):
                    b = True
                    break
            if(not b) and node[1] != "":
                mention.append(node[1])
            allmention.append(node[1])
for men in allmention:
    print(men)

# CLUSTERING-SIEVE
print("------------CLUSTERS FOUND-----------")

cluster=[]
for m1 in mention:
    for m2 in mention:
        if m1 != m2 and m1 != "" and m2 != "":
            if m1.find(m2) != -1:
                clusterExists = False
                for i in cluster:
                    if m1 in i or m2 in i:
                        i.add(m1)
                        i.add(m2)
                        clusterExists = True
                        break
                if not clusterExists:
                    cluster.append(set({m1, m2}))
for i in cluster:
    print(i)
            

# EXACT-MATCH SIEVE      
print("------------EXACT MATCHES FOUND-----------")

for i in allmention:
    #tree = parser.parse(i.split())
    #for node in tree:
    if i in mention:
        print('EXACT MATCH FOUND IN TEXT:-')
        print('Coreferent:', i)
        print('Mention:', i)




# RELAXED-MATCH SIEVE                
print("------------RELAXED MATCHES FOUND-----------")

for men1 in mention:
    for men2 in mention:
        if men1 != men2 and men1 != "" and men2 != "":
            if men1.find(men2) != -1:
                print(men1, "and", men2, "have a match")

#tree = parser.parse(text)

#print('\n'.join(['\t'.join(node) for node in tree]))