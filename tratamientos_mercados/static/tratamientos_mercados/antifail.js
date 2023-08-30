const next_Button = document.querySelector('.otree-btn-next')
function highlighterAction() {
        const completados = document.querySelectorAll('.table-success')
        const alone = completados.length >= 6
        const checked = !!localStorage.getItem('gameOver')
        if(!checked && alone){
            localStorage.setItem('gameOver', 'true')
            location.reload()
            return;
        }
        if(alone && checked){
            localStorage.clear()
            next_Button.click()
            return;
        } 
        if(checked) localStorage.clear()
}

function highlighter() {
    setTimeout(function() {
        highlighterAction();
    }, 200);
}

if (document.readyState == 'complete') {
    highlighter();
} else {
    document.onreadystatechange = function () {
        if (document.readyState === "complete") {
            highlighter();
        }
    }
}