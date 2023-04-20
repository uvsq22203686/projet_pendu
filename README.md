# Jeu du pendu
## Groupe: LDDBI Charlene ZETLAOUI, Maryatou KANTE, Daria KURGANSKAYA https://github.com/uvsq22201683/projet_pendu/
### Joues et vois si tu vas echapper a la pendaison!

![img de l'app](https://github.com/uvsq22201683/projet_pendu/blob/main/interface/pendu_img.png)

*Il s’agit d’un jeu de societe ou un mot est choisi au hasard et le joueur doit deviner a chaque tour une des lettres qui composent ce mot.*

Mode d'utilisation:
- Lancer le fichier interface.py
- Cliquer sur commencer le jeu
- Choisir le mot a deviner en indiquant soit sa longeur soit sa categorie
(eventuellement le joueur peut choisir le nombre de tentatives pour augmenter ou diminuer la difficulte du jeu)
- Jouer!!!

Durant le jeu tu peux:
- Avoir une indication sur le mot. Pour cela choisis le type d'enigme dans le menu deroulant, puis appuyes 
sur "enigme". Verifies ta connection internet avant de le faire.
- T'authentifier (onglet en haut a gauche de l'ecran). On sauvegarde tes tentatives et le nombre de tes victoires. 
Si tu t'est autentifie, tu pourra acceder a la statistique de tes resultats.
- Voir ton Score. Tu verras le nombre de tes gains, ton nombre de tentatives moyen par mot et tes tentatives pour les 5 derniers mots.
- Relancer le jeu. Si le mot ne te plait pas, n'hesite pas a relancer le jeu! Il vaut mieux recommencer le jeu que le quitter et le lancer de nouveau 
car on devra de nouveau telecharger les dictionnaires avec les mots et ca prend du temps.


Information d'instalation:
- N'oublies pas d'installer toutes les libraries necessaires pour pouvoir jouer: $ pip install -r requiremets.txt
- On utilise le spacy lemmanizer, pour cela merci d'installer $ python -m spacy download fr_core_news_md


Pour faire ce projet, on a regarde les exemples de code sur https://pypi.org/project/tkvideoplayer/, https://habr.com/ru/articles/568334/, https://github.com/sammous/spacy-lefff, https://www.tutorialspoint.com/python/tk_menu.htm
