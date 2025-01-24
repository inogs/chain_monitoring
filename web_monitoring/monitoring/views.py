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

    ANALYSIS = Path('C:\\Users\\Lorenzo\\Documents\\chain_logs\\analysis') 

    DATADIR = Path('C:\\Users\\Lorenzo\\Documents\\chain_logs\\forecast\\' + day)

    result = []
    chains = []
    
    names, start_times, end_times, phases, term_chains = get_data(DATADIR, prv, nxt) 

    for i in range(len(names)):

        phases_for_chain = []

        for j in range(len(phases)):
            
            if phases[j][0] == names[i]:
                if(phases[j][2] is False):
                    phases[j][6] = False

                phase = Phase(phases[j][1], phases[j][2],phases[j][6], phases[j][3], phases[j][4], phases[j][5])
                phases_for_chain.append(phase)

        chain = Chain(names[i], term_chains[i], start_times[i], end_times[i], phases_for_chain, 'Forecast')
        chains.append(chain)

    result.append(chains)
    json_text_forecast = [chain.to_dict() for chain in chains]
#-------------------------------------------------------------------------------------

    

    if(ANALYSIS / day).exists():
        chainsAnalysis = []
        ANALYSISDIR = ANALYSIS / day
        names, start_times, end_times, phases, term_chains = get_data(ANALYSISDIR, prv, nxt) 


        for i in range(len(names)):

            phases_for_chain = []

            for j in range(len(phases)):
            
                if phases[j][0] == names[i]:
                    if(phases[j][2] is False):
                        phases[j][6] = False

                    phase = Phase(phases[j][1], phases[j][2],phases[j][6], phases[j][3], phases[j][4], phases[j][5])
                    phases_for_chain.append(phase)

            chain = Chain(names[i], term_chains[i], start_times[i], end_times[i], phases_for_chain, 'Analysis')
            chainsAnalysis.append(chain)
        result.append(chainsAnalysis)
        json_text_forecast = [chain.to_dict() for chain in chains]
        json_text_analysis = [chain.to_dict() for chain in chainsAnalysis]
        return JsonResponse( {
            'analysis': json_text_analysis,
            'forecast': json_text_forecast,
        })
    
    #trasforma in json l'output del metodo 'to_dict' in Catena per ogni oggetto catena, spazi settati a 4
    else:

        return JsonResponse( {

            'forecast': json_text_forecast,
        })
