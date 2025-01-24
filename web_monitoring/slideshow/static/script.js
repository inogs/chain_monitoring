var check = true;
const today = new Date();
var toUse = new Date();
toUse.setDate(today.getDate());

window.onload = function () {
    drawChains();
};

function autoRefresh() {
    window.location = window.location.href;
}

function previousDay() {
    toUse.setDate(toUse.getDate() - 1);
    drawChains();
}

function nextDay() {
    toUse.setDate(toUse.getDate() + 1);
    drawChains();
}

function isFinished(phase) {

    if (phase['exists'] == true && phase['terminated'] == true) {
        return 'done';
    }

    else if (phase['exists'] == true && phase['terminated'] == false && phase['errors'] == '') {
        return 'inProgress';
    }

    else if (phase['exists'] == true && phase['terminated'] == false && phase['errors'] != '') {
        //check = false;
        return 'failed';
    }

    else {
        return 'notStarted';
    }

}

function findInProgress(phases) {

    for (let i = phases.length - 1; i >= 0; i--) {

        if (phases[i]['exists'] == true && phases[i]['terminated'] == false && phases[i]['errors'] == '') {
            return 'The chain is running!';
        }

        else {
            return 'The chain has failed!';
        }
    }

}

function isFirstChain(chain, phase) {

    var x = 0;

    for (let i = 0; i < chain['phases'].length; i++) {
        if ((chain['phases'][i]['exists'] == true && chain['phases'][i]['terminated'] == true) || (chain['phases'][i]['terminated'] == false && chain['phases'][i]['exists'] == true)) {
            x = i;
            break;
        }

    }

    if (phase['exists'] == true && phase['terminated'] == true && phase['name'] == chain['phases'][x]['name']) {
        return 'failed';
    }
    else if (phase['exists'] == true && phase['terminated'] == true) {
        return 'done';
    }

    else if (phase['exists'] == true && phase['terminated'] == false) {
        return 'failed';
    }

    else {
        return 'notStarted';
    }
}

function findErrors(phases) {

    let to_return = "";

    for (let i = 0; i < phases.length; i++) {
        if (phases[i]['errors'] != '') {
            to_return += 'phase ' + phases[i]['name'] + ': ' + phases[i]['errors'] + '\n';
        }
    }

    return to_return;
}



async function drawChains() {

    var date = toUse.getFullYear();

    var prv = new Date();
    prv.setDate(toUse.getDate() - 1);
    var prv_date = prv.getFullYear();

    var nxt = new Date();
    nxt.setDate(toUse.getDate() + 1);
    var nxt_date = nxt.getFullYear();


    if (toUse.getDate() == today.getDate()) {
        document.getElementById('nxt').disabled = 'true';
    }
    else {
        document.getElementById('nxt').disabled = '';
    }

    if ((toUse.getMonth() + 1) < 10) {
        date += '0' + (toUse.getMonth() + 1);
    }
    else {
        date += '' + (toUse.getMonth() + 1);
    }

    if (toUse.getDate() < 10) {
        date += '0' + toUse.getDate();
    }
    else {
        date += '' + toUse.getDate();
    }

    //---------------------------------------

    if ((prv.getMonth() + 1) < 10) {
        prv_date += '0' + (prv.getMonth() + 1);
    }
    else {
        prv_date += '' + (prv.getMonth() + 1);
    }

    if (prv.getDate() < 10) {
        prv_date += '0' + prv.getDate();
    }
    else {
        prv_date += '' + prv.getDate();
    }

    //---------------------------------------

    if ((nxt.getMonth() + 1) < 10) {
        nxt_date += '0' + (nxt.getMonth() + 1);
    }
    else {
        nxt_date += '' + (nxt.getMonth() + 1);
    }

    if (nxt.getDate() < 10) {
        nxt_date += '0' + nxt.getDate();
    }
    else {
        nxt_date += '' + nxt.getDate();
    }


    document.getElementById('date').innerHTML = "Watching today's chain status: " + toUse.getDate() + '/' + (toUse.getMonth() + 1) + '/' + toUse.getFullYear();
    document.getElementById('footerOGS').innerHTML = "© OGS - " + toUse.getFullYear();
    document.getElementById('footerOGS').appendChild(document.createElement('br'));
    document.getElementById('footerOGS').innerHTML += "*Note: if in dates appears 'It wasn't possible to get the time', it means that the chain worked before the previous day, or after the next day or both.";
    ;
    let div_content = document.getElementById('contentPage');
    div_content.innerHTML = '';

    let url = '/data?date=' + date + '&prec=' + prv_date + '&next=' + nxt_date;


    let res = await fetch(url).then((res) => {
        if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    }).catch((error) => console.error("Unable to fetch data from " + url + ":", error));

    const chains = res;
    const types = ['analysis', 'forecast']

    for (let k = 0; k < types.length; k++) {
        if (types[k] in chains) {
            for (let i = chains[types[k]].length - 1; i >= 0; i--) {

                let to_center = document.createElement('div');
                to_center.classList.add('toCenter');

                let chain = document.createElement('div');
                chain.classList.add('chain');

                //--------------------- HEADER ---------------------

                let header_chain = document.createElement('div');
                header_chain.classList.add('headerChain');

                let title_chain = document.createElement('h1');
                title_chain.classList.add('titleChain');
                title_chain.innerHTML = 'CHAIN: ' + chains[types[k]][i]['name'] + ' ' + chains[types[k]][i]['type'];

                let running_chain = document.createElement('h2');
                running_chain.classList.add('runningChain');
                if (chains[types[k]][i]['terminated'] == true) {
                    running_chain.innerHTML = 'The chain has finished!';
                }
                else {
                    running_chain.innerHTML = findInProgress(chains[types[k]][i]['phases']);
                }

                //--------------------------------------------------

                //--------------------- TIME -----------------------

                let time_chain = document.createElement('div');
                time_chain.classList.add('timeChain');
                let time_content = document.createElement('h1');
                time_content.classList.add('titleChain');
                var toAdd = "From: ";
                if (chains[types[k]][i]['start_time'].includes("It wasn't")) {
                    toAdd += chains[types[k]][i]['start_time'];
                }
                else {
                    toAdd += chains[types[k]][i]['start_time'].substring(9, 17);
                }
                toAdd += ' To: ';
                if (chains[types[k]][i]['end_time'].includes("It wasn't")) {
                    toAdd += chains[types[k]][i]['end_time'];
                }
                else {
                    toAdd += chains[types[k]][i]['end_time'].substring(9, 17);
                }
                time_content.innerHTML = toAdd;


                //--------------------------------------------------

                //--------------------- PHASES ---------------------


                let content_chain = document.createElement('div');
                content_chain.classList.add('contentChain');

                check = true;

                for (let m = chains[types[k]][i]['phases'].length - 1; m >= 0; m--) {

                    let progress_chain = document.createElement('div');
                    progress_chain.classList.add('progressChain');

                    let content_phase = document.createElement('h1');
                    content_phase.classList.add('phase');
                    if (i != chains[types[k]].length - 1 && chains[types[k]].length > 1 && chains[types[k]][i]['terminated'] == false) {
                        progress_chain.classList.add(isFirstChain(chains[types[k]][i], chains[types[k]][i]['phases'][m]));
                        running_chain.innerHTML = 'The chain has failed!';
                        check = false;
                    }
                    else if (check) {
                        progress_chain.classList.add(isFinished(chains[types[k]][i]['phases'][m]), check);
                    }
                    content_phase.innerHTML = chains[types[k]][i]['phases'][m]['name'];

                    progress_chain.appendChild(content_phase);
                    content_chain.appendChild(progress_chain);


                }

                //--------------------- FOOTER ---------------------

                let footer_chain = document.createElement('div');
                footer_chain.classList.add('footerChain');

                let footer_content = document.createElement('p');
                footer_content.classList.add('footerChain');
                let text_errors = findErrors(chains[types[k]][i]['phases']);
                if (text_errors != '') {
                    footer_content.innerHTML = text_errors;
                }
                else {
                    footer_content.innerHTML = "Currently there aren't any errors";
                }


                //--------------------------------------------------

                //--------------------- APPEND ---------------------

                header_chain.appendChild(title_chain);
                header_chain.appendChild(running_chain);
                chain.appendChild(header_chain);

                time_chain.appendChild(time_content);
                chain.appendChild(time_chain);

                chain.appendChild(content_chain)

                footer_chain.appendChild(footer_content);
                chain.appendChild(footer_chain);

                to_center.appendChild(chain);
                div_content.appendChild(to_center);

            }
        }

    }
    // if(toUse == today) {
    //     setInterval('drawChain()', 60000);
    // }

}

