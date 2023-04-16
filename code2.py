
       
def petiteenigme (Mot, listelettre) :
    for i in range(len(Mot)) :
        if Mot[i] in listelettre : 
            return f'La {i}e lettre est {Mot[i]}', False
    return 'Tu sait deja toutes les lettres du mot', False





            


   

