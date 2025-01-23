var check = true;
const today = new Date();


window.onload = function () {
    var date = today.getFullYear();

    if ((today.getMonth() + 1) < 10) {
        date += '0' + (today.getMonth() + 1);
    }
    else {
        date += (today.getMonth() + 1);
    }

    if (today.getDate() < 10) {
        date += '0' + today.getDate();
    }
    else {
        date += today.getDate();
    }
    drawChains(date);
};

function autoRefresh() {
    window.location = window.location.href;
}



function isFinished(phase) {

    if (phase['exists'] == true && phase['terminated'] == true) {
        return 'done';
    }

    else if (phase['exists'] == true && phase['terminated'] == false && phase['errors'] == '') {
        return 'inProgress';
    }

    else if (phase['exists'] == true && phase['terminated'] == false && phase['errors'] != '') {
        check = false;
        return 'failed';
    }

    else {
        return 'notStarted';
    }

}

function findInProgress(phases) {

    for (let i = phases.length - 1; i >= 0; i--) {
        if (phases[i]['exists'] == true && phases[i]['terminated'] == true && i == phases.length - 1) {
            return 'The chain has finished! Last phase complited: ' + phases[phases.length - 1 - i]['name'];
        }

        else if (phases[i]['exists'] == true && phases[i]['terminated'] == false && phases[i]['errors'] == '') {
            let perc = 100 * (phases.length - i) / phases.length;
            return 'The chain is running! Current phase: ' + phases[i]['name'] + ' (' + perc + '%)';
        }

        else {
            let perc = 100 * (phases.length - i) / phases.length;
            return 'The chain has failed! The failed phase: ' + phases[i]['name'] + ' (' + perc + '%)';
        }
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


async function drawChains(date) {

    document.getElementById('date').innerHTML = "Watching today's chain status: " + date;

    //console.log(date);

    let div_content = document.getElementById('contentPage');

    let url = '/data?date=' + date;

    let res = await fetch(url).then((res) => {
        if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    }).catch((error) => console.error("Unable to fetch data from " + url + ":", error));

    const chains = res['chains'];

    for (let i = 0; i < chains.length; i++) {

        let to_center = document.createElement('div');
        to_center.classList.add('toCenter');

        let chain = document.createElement('div');
        chain.classList.add('chain');

        //--------------------- HEADER ---------------------

        let header_chain = document.createElement('div');
        header_chain.classList.add('headerChain');

        let title_chain = document.createElement('h1');
        title_chain.classList.add('titleChain');
        title_chain.innerHTML = 'CHAIN: ' + chains[i]['name'];

        let running_chain = document.createElement('h2');
        running_chain.classList.add('runningChain');
        running_chain.innerHTML = findInProgress(chains[i]['phases']);

        //--------------------------------------------------

        //--------------------- TIME -----------------------

        let time_chain = document.createElement('div');
        time_chain.classList.add('timeChain');
        let time_content = document.createElement('h1');
        time_content.classList.add('titleChain');
        time_content.innerHTML = 'From: ' + chains[i]['start_time'].substring(9, 17) + ' To: ' + chains[i]['end_time'].substring(9, 17);


        //--------------------------------------------------

        //--------------------- PHASES ---------------------


        let content_chain = document.createElement('div');
        content_chain.classList.add('contentChain');

        check = true;

        for (let m = chains[i]['phases'].length - 1; m >= 0; m--) {

            let progress_chain = document.createElement('div');
            progress_chain.classList.add('progressChain');

            let content_phase = document.createElement('h1');
            content_phase.classList.add('phase');
            if (check && i == 0 && chains.length > 1) {
                progress_chain.classList.add('failed');
                running_chain.innerHTML = 'The chain has failed! The failed phase: ' + chains[i]['phases'][m]['name'] + ' (12.5%)';
                check = false;
            }
            else if(check) {
                progress_chain.classList.add(isFinished(chains[i]['phases'][m]), check);
            }
            content_phase.innerHTML = chains[0]['phases'][m]['name'];

            progress_chain.appendChild(content_phase);
            content_chain.appendChild(progress_chain);
            

        }

        //--------------------- FOOTER ---------------------

        let footer_chain = document.createElement('div');
        footer_chain.classList.add('footerChain');

        let footer_content = document.createElement('p');
        footer_content.classList.add('footerChain');
        let text_errors = findErrors(chains[i]['phases']);
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

    // for(let m = chains[0]['phases'].length - 1; m >= 0; m--) {

    //     console.log(chains[0]['phases'][m]['name']);

    // }

    //setInterval('autoRefresh()', 60000);

}

