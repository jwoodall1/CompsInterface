function startTimer() {
    const timerDisplay = document.getElementById('timer')
    let secondsRemaining = 300
    document.getElementById('startbutton').disabled = true
    document.getElementById('startbutton').innerHTML = 'Test in Progress...'
    canvaWindow = window.open('https://canva.com')
    const timerInterval = setInterval(() => {
        const minutes = Math.floor(secondsRemaining / 60)
        const seconds = secondsRemaining % 60
        timerDisplay.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        document.title = `Time Remaining: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        
        if (secondsRemaining <= 0) {
            clearInterval(timerInterval)
            canvaWindow.close()
            alert('Time is up! You will now be redirected to the questionnaire.')
            // Optionally, you can redirect the user or disable inputs here
        }
        
        secondsRemaining--
    }, 1000)
}
