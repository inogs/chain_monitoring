from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .chain import Chain
from .phase import Phase
from .openFolders import get_data
from pathlib import Path
import json



def main(request):

    day = request.GET['date']
    prv = request.GET['prec']
    nxt = request.GET['next']

    #DATADIR = Path('C:\\Users\\Lorenzo\\Documents\\chain_monitoring\\monitoring\\forecast\\' + today)

    #DATADIR = Path('C:\\Users\\Lorenzo\\Documents\\chain_monitoring\\monitoring\\forecast\\20250108')

    DATADIR = Path('D:\\chain_logs\\forecast\\' + day)
    
    names, start_times, end_times, phases, term_chains = get_data(DATADIR, prv, nxt) 
    
    chains = []

    for i in range(len(names)):

        phases_for_chain = []

        for j in range(len(phases)):
            
            if phases[j][0] == names[i]:
                if(phases[j][2] is False):
                    phases[j][6] = False

                phase = Phase(phases[j][1], phases[j][2],phases[j][6], phases[j][3], phases[j][4], phases[j][5])
                phases_for_chain.append(phase)

        chain = Chain(names[i], term_chains[i], start_times[i], end_times[i], phases_for_chain)
        chains.append(chain)

    
    #trasforma in json l'output del metodo 'to_dict' in Catena per ogni oggetto catena, spazi settati a 4
    json_text = [chain.to_dict() for chain in chains]
    return JsonResponse( {
        'chains': json_text
    })
