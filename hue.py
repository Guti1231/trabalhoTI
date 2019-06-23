
import numpy as np
import array as arr

class hufftree:
    def __init__(self,esqu,dire,galhos):
        self.esqu = esqu
        self.dire = dire
        self.galhos = galhos
    def filho(self):
        return((self.esqu, self.dire,self.galhos))



def atribuircodigo (node,pat='') :       # Associa as folhas a cada codeword
    global codes, nodes                #lembrar de trocar alguns nomes pq eu copiei de um site, n consegui pensar nisso T.T
    if type(node) == type("") :
        nodes , codes = np.append(nodes,node),np.append(codes,pat)

    else  :
        (l,r,galho) = node.filho()
        atribuircodigo(l, pat+"0")    # Branch point. Do the left branch
        atribuircodigo(r, pat+"1")    # Branch point. Do the right branch


def ordporcoluna(matriz,coluna):            # ordenar por coluna
    matrizord = matriz[matriz[:,coluna].argsort()]
    return (matrizord)


def createhufftree (matrfreq):

    linhas = matrfreq.shape[0]
    for j in range(0,linhas-1):
        matrfreq = ordporcoluna(matrfreq,0)
        matrfreq[1,0]= matrfreq[0,0]+matrfreq[1,0]
        if isinstance(matrfreq[0,1], str) and isinstance(matrfreq[1,1], str):            # esse bando de if acho que não precisava mas eu queria que a arvore ficasse bonitinha
            matrfreq[1,1] = hufftree(matrfreq[1,1],matrfreq[0,1],1)
        elif isinstance(matrfreq[0,1], str):
            matrfreq[1,1] = hufftree(matrfreq[0,1],matrfreq[1,1],matrfreq[1,1].galhos+1)

        elif isinstance(matrfreq[1,1], str):
            matrfreq[1,1] = hufftree(matrfreq[1,1],matrfreq[0,1],matrfreq[0,1].galhos+1)

        elif (matrfreq[0,1].galhos>=matrfreq[1,1].galhos):
            matrfreq[1,1] = hufftree(matrfreq[1,1],matrfreq[0,1],max(matrfreq[0,1].galhos,matrfreq[1,1].galhos)+1)
        else:
            matrfreq[1,1] = hufftree(matrfreq[0,1],matrfreq[1,1],max(matrfreq[0,1].galhos,matrfreq[1,1].galhos)+1)

        matrfreq = np.delete(matrfreq, [0], axis=0)

    return matrfreq







#abre e le o arquivo
with open( 'teste.txt','rb' ) as f:
    data = f.read()

# coloca os simbolos e a quantidade que eles se repetem numa matriz
freq = np.zeros((256,2),dtype= list)
for i in range(0, 256):
    freq[i,0] = data.count(i)
    freq[i,1] = bin(i)
# print(freq)
#ordena a matriz pela coluna 0
freq = ordporcoluna(freq,0)
# print(frequ)
# tira todas as linhas com zeros
naozeros = np.count_nonzero(freq[:,0],axis=0)
zeros = 256 - naozeros
for j in range(0,zeros):
    frequ = np.delete(freq, [0], axis=0)


# print(frequ)

# cria a arvore
frequ = createhufftree(frequ)

# associa os simbolos as codewods
codes = list()
nodes = list()
atribuircodigo(frequ[0,1])

#coloca os simbolos e as codewords numa matriz, btw se tiver um jeito melor de fazer isso me ensina pf
codewords= np.zeros((naozeros,2),dtype= list)
for i in range(0,naozeros):
    codewords[i,0] = int(codes[i], 2)
    codewords[i,1]= nodes[i]

#ordena a matriz pela coluna 0 que agora é no formato int
codewords = ordporcoluna(codewords,0)

#converte int para binario
for i in range(0,naozeros):
    codewords[i,0] = bin(codewords[i,0])



print(codewords)


# proxima coisa a fazer é escrever bit a bit, no arquivo
# tambem calcular o comprimento medio para perguntar para o prof se está certo ou comparar com os colegas



map = map(bin,data)
data = ' '.join(map)
with open('text.txt','wt') as h:
    h.write(str(freq))
