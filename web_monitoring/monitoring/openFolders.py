from pathlib import Path
import re

def get_data(folder_path):

    names = get_names(folder_path)
    
    data_re = re.compile('(PrEx )?(?P<date>[0-9]{8})-(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})')

    start_times = get_starting_date(folder_path, names, data_re)
    end_times = get_endindg_times(folder_path, names, data_re)
    phases, terminated, term_chains  = get_phases(folder_path, names, data_re)

    #print(terminated)

    chain_num = 0

    for i in range(len(phases)):
        pos = i % 8

        if i != 0 and i % 8 == 0:
            chain_num += 1

        #print(str(chain_num) + ' ' + str(pos))
        
        phases[i].append(terminated[chain_num][pos])
        #print(terminated[chain_num][pos])
        #print(phases[i])
        

    #print(end_times)   

    return names, start_times, end_times, phases, term_chains

def getYearMonthDay(toAdd):

    year = toAdd[0:4]
    month = toAdd[4:6]
    day = toAdd[6:8]

    return str(day) + '/' + str(month) + '/' + str(year)

def get_starting_date(folder_path, names, reg):

    start_time = []
    
    for name in names:
        
        file_name = 'opa.g100.' + name + '.opa_preproc.out'
        if (folder_path / file_name).exists():
            file = open(folder_path / file_name, 'r')
            txt = file.readlines()

        #print(file.readline())
            if len(txt) != 0:
                checkDate = False
                for line in txt:
                    if reg.match(line):
                        start_time.append(getYearMonthDay(reg.match(line).group('date')) + '-' + reg.match(line).group('time'))
                        checkDate = True
                        break
                if checkDate is False:
                       start_time.append("It wasn't possible to find the specified item")
            else:   
                start_time.append('None')
        else:
            start_time.append('None')
        #start_time.append(file.readline()[6:22])


    return start_time

def get_endindg_times(folder_path, names, reg):

    end_time_chain = []
    phases = ['get', 'A1', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']

    for name in names:

        for i in reversed(range(len(phases))):

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
                check_date = False
                for line in reversed(txt):
                    if reg.match(line):
                        end_time_chain.append(getYearMonthDay(reg.match(line).group('date')) + '-' + reg.match(line).group('time'))
                        check_date = True
                        break
                if check_date is False:
                    end_time_chain.append("It wasn't possible to find the specified item")

                break

            if checked is False and i == 0:
                file_name = 'opa.g100.' + name + '.opa_preproc.out'
                if (folder_path / file_name).exists():

                    file = open(folder_path / file_name, 'r')
                    txt = file.readlines()
            # end_time_chain.append(txt[-4][5:22]) 
                    if len(txt) != 0:
                        check_date_two = False
                        for line in reversed(txt):
                            if reg.match(line):
                                end_time_chain.append(getYearMonthDay(reg.match(line).group('date')) + '-' + reg.match(line).group('time'))
                                check_date_two = True
                                break
                        if check_date_two is False:
                            end_time_chain.append("It wasn't possible to find the specified item")
                                
                        break
                    else:
                        end_time_chain.append('None')
                        break
                else:
                    end_time_chain.append('None')
                    break
        #print(file.readline())
    return end_time_chain

def get_phases(folder_path, names, reg):

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
                    #print(str(n_phases[i])+ ' ' + str(folder_path.name))
                    phase.append(name)
                    phase.append(n_phases[i])
                    phase.append(exist)
                    if len(txt) != 0:
                        #phase.append(txt[1][5:22])
                        #print(str(n_phases[i])+ ' ' + str(folder_path.name) + ' lunghezza passata')
                        check_date = False
                        for line in txt:
                            if reg.match(line):
                                #print(str(n_phases[i])+ ' ' + str(folder_path.name) + ' lunghezza passata' + 'trovato inizio')
                                phase.append(getYearMonthDay(reg.match(line).group('date')) + '-' + reg.match(line).group('time'))
                                check_date = True
                                break

                        if check_date is False:
                            phase.append("It wasn't possible to find the specified item")

                        check_date_two = False
                        for line in reversed(txt):
                            if reg.match(line):
                                #print(str(n_phases[i])+ ' ' + str(folder_path.name) + ' lunghezza passata' + 'trovato inizio')
                                phase.append(getYearMonthDay(reg.match(line).group('date')) + '-' + reg.match(line).group('time'))
                                check_date_two = True
                                break

                        if check_date_two is False:
                            phase.append("It wasn't possible to find the specified item")

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
        term_chains.append(terminated[0])

    return output_phases, term_phases, term_chains

def search_for_elimination(folder_path, name):


    terminated = []

    #to check C4, C3, C2
    file_name = 'opa.g100.' + name + '.opa_postproc.out'
    if (folder_path / file_name).exists():

        
        c_four = 'opa.g100.' + name +'.opa_postproc__phase_C4.out'
        if (folder_path / c_four).exists():
            file_c_four = open(folder_path / c_four, 'r')
            txt_c_four = file_c_four.readlines()
            if len(txt_c_four) != 0:
                if 'err'.upper() in txt_c_four[-1].upper() or 'error'.upper() in txt_c_four[-1].upper() or 'ko'.upper() in txt_c_four[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)

        c_three = 'opa.g100.' + name +'.opa_postproc__phase_C3.out'
        if (folder_path / c_three).exists():
            file_c_three = open(folder_path / c_three, 'r')
            txt_c_three = file_c_three.readlines()
            if len(txt_c_three) != 0:

                if 'err'.upper() in txt_c_three[-1].upper() or 'error'.upper() in txt_c_three[-1].upper() or 'ko'.upper() in txt_c_three[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)

        c_two = 'opa.g100.' + name +'.opa_postproc__phase_C2.out'
        if (folder_path / c_two).exists():
            file_c_two = open(folder_path / c_two, 'r')
            txt_c_two = file_c_two.readlines()
            if len(txt_c_two) != 0:
                if 'err'.upper() in txt_c_two[-1].upper() or 'error'.upper() in txt_c_two[-1].upper() or 'ko'.upper() in txt_c_two[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)

    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)

    #to check C1, B2, B1
    file_name = 'opa.g100.' + name + '.opa_model.out'
    if (folder_path / file_name).exists():

        c_one = 'opa.g100.' + name +'.opa_postproc__phase_C1.out'
        if (folder_path / c_one).exists():
            file_c_one = open(folder_path / c_one, 'r')
            txt_c_one = file_c_one.readlines()
            if len(txt_c_one) != 0:

                if 'err'.upper() in txt_c_one[-1].upper() or 'error'.upper() in txt_c_one[-1].upper() or 'ko'.upper() in txt_c_one[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)

        b_two = 'opa.g100.' + name +'.opa_model__phase_B2.out'
        if (folder_path / b_two).exists():
            file_b_two = open(folder_path / b_two, 'r')
            txt_b_two = file_b_two.readlines()
            if len(txt_b_two) != 0:
                if 'err'.upper() in txt_b_two[-1].upper() or 'error'.upper() in txt_b_two[-1].upper() or 'ko'.upper() in txt_b_two[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)

        b_one = 'opa.g100.' + name +'.opa_model__phase_B1.out'
        if (folder_path / b_one).exists():
            file_b_one = open(folder_path / b_one, 'r')
            txt_b_one = file_b_one.readlines()
            if len(txt_b_one) != 0:

                if 'err'.upper() in txt_b_one[-1].upper() or 'error'.upper() in txt_b_one[-1].upper() or 'ko'.upper() in txt_b_one[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)
    else:
        terminated.append(False)
        terminated.append(False)
        terminated.append(False)

    #to check get, A1
    file_name = 'opa.g100.' + name + '.opa_preproc.out'
    if (folder_path / file_name).exists():

        check_get = True
        a_one = 'opa.g100.' + name +'.opa_preproc__phase_A1.out'
        if (folder_path / a_one).exists():
            file_a_one = open(folder_path / a_one, 'r')
            txt_a_one = file_a_one.readlines()

            if len(txt_a_one) != 0:
                if 'err'.upper() in txt_a_one[-1].upper() or 'error'.upper() in txt_a_one[-1].upper() or 'ko'.upper() in txt_a_one[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
                    terminated.append(True)
                    check_get = False
            else:
                terminated.append(False)
        else:
            terminated.append(False)

        _get = 'opa.g100.' + name + '.opa_get.out'
        if (folder_path / _get).exists() and check_get is True:
            file_get = open(folder_path / _get, 'r')
            txt_get = file_get.readlines()
            if len(txt_get) != 0:
                if 'err'.upper() in txt_get[-1].upper() or 'error'.upper() in txt_get[-1].upper() or 'ko'.upper() in txt_get[-1].upper():
                    terminated.append(False)
                else:
                    terminated.append(True)
            else:
                terminated.append(False)
        else:
            terminated.append(False)
            
    else:
        terminated.append(False)
        terminated.append(False)

    
    return terminated
    

def search_for_errors(file):

    errors = ''
    
    for line in file:
        if 'ko'.upper() in line.upper() or 'err'.upper() in line.upper() or 'error'.upper() in line.upper():
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
                break

        if check is True:
            #print(key)
            chain.append(key)
        else:
            break
        
        
    
    return chain



            