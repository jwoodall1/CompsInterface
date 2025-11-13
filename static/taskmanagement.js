let intervalRunning = 0
let websiteWindow = null
let secondsRemaining = 0
function startStopTimer(website) {
    if (intervalRunning === 0) {
        startTimer(website) 
        intervalRunning = 1
    } else {
        stopTimer()
        intervalRunning = 0
    }
}

function startTimer(website, taskId) {
    const timerDisplay = document.getElementById('timer')
    secondsRemaining = 300
    document.getElementById('startbutton').innerHTML = "I'm Finished"
    websiteWindow = window.open(website)
    const timerInterval = setInterval(() => {
        const minutes = Math.floor(secondsRemaining / 60)
        const seconds = secondsRemaining % 60
        timerDisplay.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        document.title = `Time Remaining: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        //redirect back when time is up
        if (secondsRemaining <= 0) {
            clearInterval(timerInterval)
            websiteWindow.close()
            alert('Time is up! You will now be redirected to the questionnaire.')
            window.location.href = '/form_unprompted?previousTask='+taskId
        }
        
        secondsRemaining--
    }, 1000)
}

function stopTimer() {
    websiteWindow.close()
    window.location.href = '/purgatory?timeLeft='+secondsRemaining
}