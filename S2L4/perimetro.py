calcolo= ""
while calcolo != "no":
    calcolo= input("Vuoi calcolare un perimetro? ")
    if calcolo== "si":
        perimetro = input("Per quale figura geometrica vuoi calcolare il perimetro? ")
        
        if perimetro== "quadrato" :
            lato = float(input ("Dimmi il lato del tuo quadrato: "))
            perimetro1 = lato * 4
            print(f"Il perimetro del tuo quadrato sarà:", (round (perimetro1, 2)))
        
        elif perimetro== "cerchio" : 
            raggio = float(input ("\nInserisci il raggio della tua circonferenza: "))
            perimetro2 = 2 * 3.14 * raggio
            print(f"Il perimetro della tua circonferenza sarà:", (round (perimetro2, 2)))
               
        elif perimetro == "rettangolo" :
            lator = float(input("\nInserisci il lato del tuo rettangolo: "))
            altezza = float(input("Inserisci l`altezza del tuo rettangolo: "))
            perimetror= (lator * 2) + (altezza * 2)
            print(f"Il perimetro del tuo rettangolo sarà:", (round (perimetror, 2)))
        
        else:
            print("Ti sei dimenticato di dirmi la figura geometrica, inseriscila")
    
    elif calcolo == "no":
        print("Mi sa proprio che oggi non hai voglia di fare gli esercizi che ti hanno assegnato")