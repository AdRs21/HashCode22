import sys
import time
from math import exp
import random
import numpy as np

def main(lettre) :
    #FONCTIONS
    def lecture(nomFichier=lettre+'.txt') :
        with open(nomFichier,"r") as fichier :
            nbContributeurs, nbProjets = map(int,fichier.readline().split())
            infoContr = []
            setSkills = set()
            for i in range (nbContributeurs) :
                nom, nbSkills = fichier.readline().split()
                nbSkills = int(nbSkills)
                skillsC = []
                for idSkill in range (nbSkills) :
                    nomS, niveauS = fichier.readline().split()
                    niveauS = int(niveauS)
                    skillsC.append([nomS,niveauS])
                    setSkills.add(nomS)
                infoContr.append([nom, nbSkills,skillsC])
            infoProj = []
            for i in range (nbProjets) :
                nom, duree, score, dateLim, nbRole = fichier.readline().split()
                duree, score, dateLim, nbRole = int(duree),int(score),int(dateLim),int(nbRole)
                besoins = []
                for idB in range (nbRole) :
                    skill, niveau = fichier.readline().split()
                    besoins.append([skill,int(niveau)])
                    setSkills.add(skill)
                infoProj.append([nom,duree,score,dateLim,nbRole,besoins])
        return (nbContributeurs,nbProjets,infoContr,infoProj,setSkills)
    def high_scores() :
        lettres = ['a','b','c','d','e','f']
        records = dict()
        with open('high_scores_v3.txt','r') as fichier :
            for i in range (len(lettres)) :
                records[lettres[i]] = int(fichier.readline())
        return records
    def maj_high_scores(records=[0]*5) :
        lettres = ['a','b','c','d','e','f']
        with open('high_scores_v3.txt','w') as fichier :
            for i in range (len(lettres)) :
                fichier.write(str(records[lettres[i]])+"\n")
    def trouveScore() :
        rep = 0
        return rep
    def estPossible(roles,infoContr,occupe,t) :
        #on met juste les collaborateurs dans l'ordre
        nbContributeurs = len(infoContr)
        solution = []
        estPris = [0]*nbPers
        bonus = 0
        niveauMentor = [0]*nbSkills
        ordre = [(i,roles[i]) for i in range (len(roles))]
        random.shuffle(ordre)
        for i in range (len(roles)) :
            idR,(nomS,niveauS) = ordre[i]
            #nomS, niveauS = roles[i]
            idSkill = nomToIDS[nomS]
            besoin = True
            #on cherche avec mentor
            if niveauMentor[idSkill] >= niveauS :
                listeT = list(aNiveau[idSkill][niveauS-1])
                for idPers in listeT :
                    if occupe[idPers]<t and estPris[idPers] == 0 :
                        besoin = False
                        bonus += 1
                        estPris[idPers] = 1
                        solution.append((idPers,idR))
                        break
            if besoin :
                #on cherche sans mentor, mais qui s'upgrade
                listeT = list(aNiveau[idSkill][niveauS])
                for idPers in listeT :
                    if occupe[idPers]<t and estPris[idPers] == 0 :
                        besoin = False
                        bonus += 1
                        estPris[idPers] = 1
                        solution.append((idPers,idR))
                        break
            if besoin : #on prend qqn qui convient
                for idNiv in range (niveauS+1,niveauMax+1) :
                    listeT = list(aNiveau[idSkill][idNiv])
                    for idPers in listeT :
                        if occupe[idPers]<t and estPris[idPers] == 0 :
                            besoin = False
                            estPris[idPers] = 1
                            solution.append((idPers,idR))
                            break
                    if not besoin :
                        break
            if besoin : return (-1,-1)
            #on met a jour les niveaux de mentor
            idPers = solution[-1][0]
            for i in range(nbSkills) :
                niveauMentor[i] = max(niveauMentor[i],infoContr[idPers][2][i])
        #il faut remettre la solution dans l'ordre
        sol2 = [0]*len(roles)
        for i in range(len(roles)) :
            sol2[solution[i][1]] = solution[i][0]
        return (sol2,bonus)



    #INPUT
    nbPers,nbProjets,infoContr,infoProj,setSkills = lecture()
    records = high_scores()
    #SOLUTION
    #on transforme la liste des skills pour les avoir tous pour chaque contributeur
    listeSkills = list(setSkills)
    nbSkills = len(listeSkills)
    nomToIDS = dict()
    for i,x in enumerate(listeSkills) :
        nomToIDS[x] = i
    for i in range (nbPers) :
        nouvListe = [0]*nbSkills
        for nom, niveau in infoContr[i][2] :
            nouvListe[nomToIDS[nom]] = niveau
        infoContr[i][2] = nouvListe
    #on trouve le temps max
    tMax = 0
    dureeMoy = 0
    scoreMoy = 0
    for i in range (nbProjets) :
        tMaxProj = infoProj[i][3]+infoProj[i][2]-infoProj[i][1]
        infoProj[i].append(tMaxProj)
        dureeMoy += infoProj[i][1]
        scoreMoy += infoProj[i][2]
        tMax = max(tMaxProj,tMax)
    infoProj.sort(key=lambda x:-x[-1])
    dureeMoy /= nbProjets
    scoreMoy /= nbProjets
    niveauMax = 20
    aNiveau = [[set() for _ in range (niveauMax+1)] for _ in range (nbSkills)]
    for idPers in range(nbPers) :
        for idSkill,niveau in enumerate(infoContr[idPers][-1]) :
            aNiveau[idSkill][niveau].add(idPers)
    continuer = False
    #solution
    t = 0
    occupe = [-1]*nbPers
    nbProjPris = 0
    reponse = ""
    decile = 0
    scoreCours = 0
    while t<=tMax :
        if t/tMax > decile+0.01 :
            decile += 0.01
            print(decile,nbProjPris,scoreCours)
        """#on enleve les projets qu'on ne peut plus faire (en vrai peut être rentable de faire des projets gratuitement pour progresser)
        while infoProj != [] and t>infoProj[-1][-1] :
            infoProj.pop()
        """
        if len(infoProj) == 0 :
            return
        nbProj = len(infoProj)
        assignement = []
        bestVal = -1
        dureeBest = 0
        idProjBest = -1
        bestBonus = 0
        indices = list(range(nbProj))
        random.shuffle(indices) #Rq : avec ou sans
        def ordreProj(i) : #Rq : a voir pour modifier
            x= infoProj[i]
            nom, duree,score,dateLim,nbRoles,roles,tMaxProj = x
            return score/(1+max(0,(dateLim-t)/duree))-max(0,t+duree-dateLim)
        indices.sort(key=ordreProj)
        for idProj in indices[-500:] :#for idProj in range (nbProjets) : #Rq: pour accelerer, varier le cutoff
            nom, duree,score,dateLim,nbRoles,roles,tMaxProj = infoProj[idProj]
            if True:#t <= tMaxProj :#and (dateLim-t)<3*dureeMoy: #pour accelerer
                #on trouve un assignement des collaborateurs
                solution,bonus = estPossible(roles,infoContr,occupe,t)#bonus : nb de personnes qui s'upgradent
                if solution != -1 :
                    #on donne un score
                    if t<= tMaxProj :
                        scoreTest = score/(1+max(0,1-(dateLim-t)/duree))-max(0,t+duree-dateLim)+(tMax-t)/dureeMoy*scoreMoy*bonus/100
                    else :
                        scoreTest = 0
                    #scoreTestReel = max(0,score-max(0,t+duree-dateLim))
                    if scoreTest>bestVal or (scoreTest==bestVal and bonus >bestBonus):
                        bestVal = scoreTest
                        assignement = solution
                        dureeBest = duree
                        idProjBest = idProj
                        bestBonus = bonus
        if assignement != [] :#on a des projets a mettre
            nbProjPris += 1
            nom, duree,score,dateLim,nbRoles,roles,tMaxProj  = infoProj[idProjBest]
            reponse += nom+'\n'
            for iL,idPers in enumerate(assignement) :
                #on met dans la reponse
                reponse += infoContr[idPers][0]+' '
                #on occupe
                occupe[idPers] = t+duree-1
                #on fait apprendre
                nomTache = roles[iL][0]
                idSkill = nomToIDS[nomTache]
                niveauAvant = infoContr[idPers][2][idSkill]
                if niveauAvant <= roles[iL][1] :
                    infoContr[idPers][2][idSkill] += 1
                    if niveauAvant<20 :
                        aNiveau[idSkill][niveauAvant].remove(idPers)
                        aNiveau[idSkill][niveauAvant+1].add(idPers)
            reponse+='\n'
            scoreCours += max(0,score-max(0,t+duree-dateLim))
            infoProj.pop(idProjBest)
            #OUTPUT
            best = scoreCours
            if best > records[lettre] :
                records[lettre] = best
                maj_high_scores(records)
                with open("v3_output"+lettre+".txt", "w") as fichier:
                    fichier.write(str(nbProjPris)+'\n')
                    fichier.write(reponse)
        else :
            t = max(min(occupe)+1,t+1)

for lettre in 'abcdef' :
    main(lettre)