#Definisco la classe delle eccezioni
class ExamException(Exception):
    pass

#Corpo principale del programma
class CSVTimeSeriesFile:

    #Inizializzo la classe su "name"
    def __init__(self, name):
        self.name = name

    #Metodo get_data() che torna una lista di liste, dove il primo elemento delle liste annidate è l’epoch ed il secondo la temperatura
    def get_data(self):

        #Verifico che il file esista e sia leggibile, altrimenti alzo un'eccezione
        try:
            my_file = open(self.name,'r')
        except:
            raise ExamException ('Il file non esiste o non è leggibile')

        data = my_file.read()[1:]

        #Creo una lista e un metodo che inserisce nella lista appena creata delle liste in cui il primo elemento è l'epoch e il secondo è la temperatura
        result = list()
        for line in data.split('\n'):
            split_line = line.split(',')
            try:
                epoch = round(float(split_line[0]))
                #Alzo un'eccezione se c'è un timestamp fuori ordine o un duplicato
                if len(result)>0 and epoch<=result[-1][0]:
                    raise ExamException ('Lista non ordinata')
                temperature = float(split_line[1])
            except ValueError:
                continue
            result.append([epoch, temperature])
        return result

#Funzione indipendente che mi dice il numero di inversioni di trend di temperatura rilevati per ogni ora presente nel dataset
def hourly_trend_changes(time_series):

    result = list()
    temp = list()
    ep = list()
    cont = 0

    #Ciclo che calcola le inversioni di trend per ogni ora del dataset
    for cont in range(len(time_series)):

        prec = int(time_series[cont][0]/3600)
        try:
            succ = int(time_series[cont+1][0]/3600)
        except IndexError:
            succ = 0

        #Salvo in una stessa lista tutti gli epoch che appartengono alla stessa ora e tutti i valori di temperatura associati
        if prec==succ:
            ep.append(prec)
            temp.append(time_series[cont][1])
        else:
            ep.append(prec)
            temp.append(time_series[cont][1])
            #print(ep)
            #print(temp)

            #Calcolo le inversioni di trend in un'ora
            index = 0
            trend = None
            changes = 0
            for el in temp:
                if index!=0:
                    if temp[index-1]>el:
                        if trend == "Increasing":
                            changes+=1
                        trend = "Decreasing"
                    elif temp[index-1]<el:
                        if trend == "Decreasing":
                            changes+=1
                        trend = "Increasing"
                index+=1

            cont+=1
            #print(cont)
            #Salvo il risultato ricavato dalla funzione precedente e svuoto le liste 'temp' ed 'ep'
            result.append(changes)
            temp = list()
            ep = list()
    #print(ep)
    #print(temp)
    return result


#Provo il programma con il file 'data.csv'
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
#print(time_series)
print(hourly_trend_changes(time_series))