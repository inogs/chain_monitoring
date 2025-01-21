from pathlib import Path

def get_data(folder_path):

    names = get_names(folder_path)
    
    start_times = get_starting_date(folder_path, names)
    end_times = get_endindg_times(folder_path, names)
    phases, terminated, term_chains  = get_phases(folder_path, names)

    #print(terminated)

    chain_num = 0

    for i in range(len(phases)):
        pos = i % 8

        if i != 0 and i % 8 == 0:
            chain_num += 1

        #print(str(chain_num) + ' ' + str(pos))
        phases[i].append(terminated[chain_num][pos])

        

        

    return names, start_times, end_times, phases, term_chains

def get_starting_date(folder_path, names):

    start_time = []
    
    for name in names:
        
        file_name = 'opa.g100.' + name + '.opa_preproc.out'
        file = open(folder_path / file_name, 'r')
        txt = file.readlines()

        #print(file.readline())
        for line in txt:
            if (folder_path.name + '-') in line:
                start_time.append(line[line.find(folder_path.name + '-'):(line.find(folder_path.name + '-') + 17)])
                break
        #start_time.append(file.readline()[6:22])


    return start_time

def get_endindg_times(folder_path, names):

    end_time_chain = []
    phases = ['A1', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']

    for name in names:

        for i in reversed(range(7)):

            checked = False
            file = None
            txt = None

            for j in range(0, len(list(folder_path.glob('*')))):

                if name in list(folder_path.iterdir())[j].name and phases[i] in list(folder_path.iterdir())[j].name:
                    #print(list(folder_path.iterdir())[j].name)
                    file = open(list(folder_path.iterdir())[j], 'r')
                    txt = file.readlines()
                    if len(txt) != 0:
                        checked = True
                        break

            if checked is True:
                for line in reversed(txt):
                    if (folder_path.name + '-') in line:
                        end_time_chain.append(line[line.find(folder_path.name + '-'):(line.find(folder_path.name + '-') + 17)])
                        break
                break

        if checked is False:
            file_name = 'opa.g100.' + name + '.opa_get.out'
            file = open(folder_path / file_name, 'r')
            txt = file.readlines()
            # end_time_chain.append(txt[-4][5:22]) 
            for line in reversed(txt):
                if (folder_path.name + '-') in line:
                    end_time_chain.append(line[line.find(folder_path.name + '-'):(line.find(folder_path.name + '-') + 17)])
                    break
        #print(file.readline())
    return end_time_chain

def get_phases(folder_path, names):

    output_phases = []
    term_phases = []
    term_chains = []
    n_phases = ['get','A1', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']
    phases = ['opa_get','opa_preproc__phase_A1', 'opa_model__phase_B1', 'opa_model__phase_B2', 'opa_postproc__phase_C1', 'opa_postproc__phase_C2', 'opa_postproc__phase_C3', 'opa_postproc__phase_C4']

    for name in names:

        for i in reversed(range(8)):

            phase = []

            exist = False
            
            for j in range(0, len(list(folder_path.glob('*')))):

                #if name in list(folder_path.iterdir())[j].name and phases[i] in list(folder_path.iterdir())[j].name:
                if list(folder_path.iterdir())[j].name == ('opa.g100.' + name + '.' + phases[i] + '.out'):
                    exist = True
                    file = open(list(folder_path.iterdir())[j], 'r')
                    txt = file.readlines()
                    
                    phase.append(name)
                    phase.append(n_phases[i])
                    phase.append(exist)
                    if len(txt) != 0:
                        #phase.append(txt[1][5:22])
                        for line in txt:
                            if (folder_path.name + '-') in line:
                                phase.append(line[line.find(folder_path.name + '-'):(line.find(folder_path.name + '-') + 17)])
                                break
                        for line in reversed(txt):
                            if (folder_path.name + '-') in line:
                                phase.append(line[line.find(folder_path.name + '-'):(line.find(folder_path.name + '-') + 17)])
                                break
                        #phase.append(txt[-1][0:17])
                    else:
                        phase.append('None')
                        phase.append('None')

                    errors = search_for_errors(txt)
                    phase.append(errors)
                    break
            
            if exist is False:
                phase.append(name)
                phase.append(n_phases[i])
                phase.append(exist)
                phase.append('None')
                phase.append('None')
                phase.append('')
                

            output_phases.append(phase)
        terminated = search_for_elimination(folder_path, name)
        term_phases.append(terminated)
        term_chains.append(terminated[6])

    return output_phases, term_phases, term_chains

def search_for_elimination(folder_path, name):


    terminated = []

    #to check get
    file_name = 'opa.g100.' + name + '.opa_get.out'
    if (folder_path / file_name).exists():
        #print(name + ' GET CHECK')
        file = open(folder_path / file_name, 'r')
        txt = file.readlines()
        if 'err'.upper() in txt[-1].upper():
            terminated.append(False)
        else:
            terminated.append(True)
    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        return terminated

    #to check A1
    file_name = 'opa.g100.' + name + '.opa_preproc.out'
    if (folder_path / file_name).exists():
        
        file = open(folder_path / file_name, 'r')
        txt = file.readlines()
        if 'err'.upper() in txt[-1].upper():
            terminated.append(False)
        else:
            
            terminated.append(True)
    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        return terminated
    
    #to check B1, B2, C1
    file_name = 'opa.g100.' + name + '.opa_model.out'
    if (folder_path / file_name).exists():
        #print(name + ' B1/B2/C1 CHECK')
        file = open(folder_path / file_name, 'r')
        txt = file.readlines()
        if 'err'.upper() in txt[-1].upper():
            c_one = 'opa.g100.' + name +'.opa_postproc__phase_C1.out'
            if (folder_path / c_one).exists():
                terminated.append(True)
                terminated.append(True)
                terminated.append(False)
            else:
                b_two = 'opa.g100.' + name +'.opa_model__phase_B".out'
                if (folder_path / b_two).exists():
                    terminated.append(True)
                    terminated.append(False)
                    terminated.append(False)
                else:
                    terminated.append(False)
                    terminated.append(False)
                    terminated.append(False)
        else:
            terminated.append(True)
            terminated.append(True)
            terminated.append(True)
    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        return terminated

    #to check  C2, C3, C4
    file_name = 'opa.g100.' + name + '.opa_postproc.out'
    if (folder_path / file_name).exists():
        #print(name + ' A1 CHECK')
        file = open(folder_path / file_name, 'r')
        txt = file.readlines()
        if 'err'.upper() in txt[-1].upper():
            c_four = 'opa.g100.' + name +'.opa_postproc__phase_C4.out'
            if (folder_path / c_four).exists():
                terminated.append(True)
                terminated.append(True)
                terminated.append(False)
            else:
                c_three = 'opa.g100.' + name +'.opa_postproc__phase_C3.out'
                if (folder_path / c_three).exists():
                    terminated.append(True)
                    terminated.append(False)
                    terminated.append(False)
                else:
                    terminated.append(False)
                    terminated.append(False)
                    terminated.append(False)
        else:
            terminated.append(True)
            terminated.append(True)
            terminated.append(True)
    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)
        return terminated
    
    return terminated
    

def search_for_errors(file):

    errors = ''
    
    for line in file:
        if 'ko'.upper() in line.upper():
            errors += line + '\n'

    return errors

def get_names(folder_path):

    # Open all folders in the current directory
    chain = []
    #print(folder)
    for i in range(1, len(list(folder_path.glob('*')))):

        #print(list(folder.iterdir())[i].name)
        if i < 10:
            key = '00' + str(i)
        elif i < 100:
            key = '0' + str(i)
        else:
            key = str(i)

        check = False

        for j in range(0, len(list(folder_path.glob('*')))):

                

            if key in list(folder_path.iterdir())[j].name:
                check = True
                break;

        if check is True:
            #print(key)
            chain.append(key)
        else:
            break;
        
        
    
    return chain



            