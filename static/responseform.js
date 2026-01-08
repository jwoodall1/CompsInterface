const urlParams = new URL(window.location.href).searchParams;
let previousTask = urlParams.get('previousTask')

function changeResponseButton() {
    const timerDisplay = document.getElementById('timer')
    const timerInterval = setInterval(() => {
        const minutes = Math.floor(secondsRemaining / 60)
        const seconds = secondsRemaining % 60
        timerDisplay.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        document.title = `Time Remaining: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        //redirect back when time is up
        if (secondsRemaining <= 0) {
            clearInterval(timerInterval)
            websiteWindow.close()
            alert('you are now out of purgatory')
            window.location.href = '/form_unprompted'
        }
        
        secondsRemaining--
    }, 1000)
}

setTimeout(changeResponseButton, 100);