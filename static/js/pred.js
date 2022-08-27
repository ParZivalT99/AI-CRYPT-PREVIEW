btn = document.getElementById("btn-consult");
btn.addEventListener("click", btnDisabled)
btn.disabled = true;

(function () {
    if (localStorage.getItem('time') === '0') {
        //pass
        console.log('time cero')
        btnUndisabled()

    }else if (localStorage.getItem('time') === 'NaN' || localStorage.getItem('time') === null ){
        setTime(0);
        btnUndisabled()
    }else {
        setTimeout(countdown, 10);
        /* console.log('else' + localStorage.getItem('time')) */
    }
})();

function setTime(time) {
    localStorage.setItem('time', time);
}



function countdown() {
    btn.disabled = true;
    if (localStorage.getItem('time') === '0') {
        setTime(20);
    }
    var count = parseInt(localStorage.getItem('time'), 10);

    var myTimer = setInterval(function () {
        setTime(count--);
        //count--;
        /* console.log('counteer ::: ' + count) */
        document.getElementById("counter").innerHTML = localStorage.getItem('time') + 's';
        if (localStorage.getItem('time') == 0) {
            setTime(0);
            document.getElementById("counter").innerHTML = '';
            btnUndisabled();
            clearInterval(myTimer);
        }
    }, 1000);
}


function btnDisabled() {
    setTimeout(countdown, 1);
}

function btnUndisabled() {
    btn.disabled = false;
}

