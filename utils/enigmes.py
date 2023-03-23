from bs4 import BeautifulSoup
import requests
from random import randint
import tkinter as tk


def homonyme(bs):
        '''Cherche la definition de l'homonyme du mot'''

        res = bs.find('a', 'lienarticle').text
        definition = make_request(res, 'definition')
        if definition[1]=='error':
             res = definition[0]
             #print(res, definition )
        else:
             res = ["La definition de l'homonyme de ce mot est la suivante:",
                definition[2].split('Synonymes')[0], 'homonyme']
             #print(res, definition)
        return res

def locution1(bs, mot):
        '''Cherche la locution avec le mot donne'''
        res_valide = False
        index_invalid = True
        max_index = 8

        res = bs.find('ul', 'ListeLocutions').text[:1000].split('.')
        while index_invalid:
            try:
                res1 = res[randint(1,max_index)]
                index_invalid = False
            except IndexError:
                  max_index-=1

        while res_valide == False:
                index_invalid = True
                if len(res1)<20:
                        while index_invalid:
                            try:
                                res1 = res[randint(1,max_index)]
                                index_invalid = False
                            except IndexError:
                                max_index-=1
                else:
                        res_valide = True
                res1 = res1.split(' ')
                res = ''
                for i in res1:
                        if i.lower().__contains__(mot):
                            i = '...'
                        res+=i
                        res+=' '
                res = ['Voici une locution avec ce mot:', res[:-1]+'.', 'locution']
        return res

def locution(bs, mot):
        '''Cherche la locution avec le mot donne'''
        res_valide = False
        index_invalid = True
        max_index = 8

        res1 = bs.find('li', 'Locution').text.split(' ')
        print(res1)
        res = ''
        for i in res1:
            if i.lower().__contains__(mot):
                i = '...'
            res+=i
            res+=' '
        res = ['Voici une locution avec ce mot:', res[:-1]+'.', 'locution']
        return res

def citation(bs, mot):
        '''cherche la citation avec le mot donne'''

        res = [bs.find('span', 'AuteurCitation').text]
        res.append(bs.find('span', 'TexteCitation').text)
        res.append(bs.find('span', 'InfoCitation').text)
                    
        res[1] = res[1].split(' ')
        res1 = ''
        for i in res[1]:
                if i.lower().__contains__(mot):
                        i = '...'
                res1+=i
                res1+=' '
        res = ['Voici une citation avec ce mot:', res[0],
                res1[:-1]+'.', res[2], 'citation']
                    
        return res

def enigme(sous_action, bs, mot=None):
        try:
                if sous_action == 'homonymes':
                        return homonyme(bs)

                elif sous_action == 'locutions':
                        return locution(bs, mot)
                        
                else:    
                        return citation(bs, mot)

        
        except AttributeError:
                return None

def make_request(mot, action, sous_action = None):
    '''make a request to the Larous dictionnary to get the definition
    of a word or a complement information'''

    url = 'https://www.larousse.fr/dictionnaires/francais/' + mot
    #attention timeout 
    response = requests.get(url, timeout = 15)

    try:
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'html.parser')
            
            if action == 'definition':
                try:
                    mot_f_m = bs.find('p', 'CatgramDefinition')
                    #print(mot_f_m)
                    #definitions = bs.find('ul', 'Definitions')
                    definitions = bs.find('li', 'DivisionDefinition')
                    return [mot, mot_f_m.text, definitions.text.split('.\xa0')[1].split('\r')[0]]
                except AttributeError:
                     print(definitions.text)
                     return [mot, '', definitions.text]
                except IndexError:
                    print(definitions.text)
                    return ["Oh! Ce mot est trop complique! On ne peut pas trouver sa definition.", 'error']

            elif action == 'enigme':
                actions = ['homonymes', 'locutions', 'citation']
                if sous_action == None:
                    ca_marche = False
                    while len(actions)>=1:
                        sous_action = actions.pop(randint(0, len(actions)-1))
                        res = enigme(sous_action, bs, mot)
                        if res!=None:
                            return res

                    if  res == None:
                        return ["Oh! Ce mot est trop complique! "+\
                              "On ne peut pas trouver d'enigme.", 'error']
                
                else:
                    res = enigme(sous_action, bs, mot)
                    if res==None:
                        return ["Cet action est indisponible pour ce mot. "+\
                              "Veillez de choisir une autre action.", 'error']
                    else:
                        return res
                    

        else:
            return ['Errer! Status code:'+ response.status_code, 'error']

    except TimeoutError:
        return ['Verifiez la connection internet.\n Status code:'+ response.status_code, 'error']

def fermer_fenetre_def_eni_root(def_eni_root):
    def_eni_root.destroy()


def create_fenetre_def_eni_root(mot, action, sous_action = None):
    '''cree une fenetre qui affiche la definition
    ou l'enigme'''
    res = make_request(mot, action, sous_action)

    def_eni_root = tk.Tk()

    if res[-1]=='error':
        def_eni_root.title('error')
        t_text1 = tk.Label(def_eni_root, text = res[0])

    elif action == 'enigme':

        def_eni_root.title('enigme')
        t_title = tk.Label(def_eni_root, text = 'Enigme')

        t_text1 = tk.Label(def_eni_root, text = res[0])
        t_text2 = tk.Label(def_eni_root, text = res[1])
        
        if res[-1] == 'citation':
            t_text3 = tk.Label(def_eni_root, text = res[2])
            t_text4 = tk.Label(def_eni_root, text = res[3])

            t_text3.grid(row=3, column=1)
            t_text4.grid(row=4, column=1)
        
        t_title.grid(row=0, column=0, columnspan = 2)
        t_text2.grid(row=2, column=1)


    else:
        def_eni_root.title('definition')
        t_title = tk.Label(def_eni_root, text = res[0].capitalize())
        t_text1 = tk.Label(def_eni_root, text = res[1])
        t_text2 = tk.Label(def_eni_root, text = res[2])

        t_title.grid(row=0, column=0, columnspan = 2)
        t_text2.grid(row=2, column=1)
        
    t_text1.grid(row=1, column=1)

    b_quitter = tk.Button(def_eni_root, text = 'Quitter', command = lambda: fermer_fenetre_def_eni_root(def_eni_root))
    b_quitter.grid(column = 2, row = 5)


    def_eni_root.mainloop()




sous_action = None

def choisir_sous_action(s_action):
    global sous_action
    sous_action = s_action

def create_bouton_ask_eni(mot, ask_eni_root):
    '''Affiche le bouton qui affiche des enigmes et un bouton
    qui permet de choisir le type d'enigme '''
    global sous_action
    #ask_eni_root = tk.Tk()

    ask_eni_bouton = tk.Button(ask_eni_root, text='Enigme', command = lambda: create_fenetre_def_eni_root(mot, 'enigme', sous_action))
    ask_eni_bouton1 =  tk.Menubutton(ask_eni_root, text = "Choisir le type d'enigme", relief = 'ridge',fg='white', bg='green' )
    ask_eni_bouton1.menu = tk.Menu(ask_eni_bouton1, tearoff = 0 )
    ask_eni_bouton1["menu"] =  ask_eni_bouton1.menu

    ask_eni_bouton1.menu.add_command(label = 'Homonyme', command = lambda : choisir_sous_action('homonymes'))
    ask_eni_bouton1.menu.add_command(label = 'Citation',  command = lambda : choisir_sous_action('citations'))
    ask_eni_bouton1.menu.add_command(label = 'Locution', command = lambda : choisir_sous_action('locutions'))
    ask_eni_bouton1.menu.add_command(label = 'Tout', command = lambda : choisir_sous_action(None))

    ask_eni_bouton.place(x = 450+(40*int(len(mot)/2))+50, y=445)
    ask_eni_bouton1.place(x = 450+(40*int(len(mot)/2))+50, y=465)

    #ask_eni_root.mainloop()



    