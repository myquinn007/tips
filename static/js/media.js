document.addEventListener('DOMContentLoaded', () => {
  const rows = document.querySelectorAll('.hidden-info');
  
  rows.forEach(row => {
    row.addEventListener('click', () => {
      // Toggle the 'active' class to show/hide action buttons
      row.classList.toggle('active');
    });
  });
});
  
  function downloadMusic(pid, mic){
    let audio = new Audio('static/'+pid)
    // audio.play()
    // audio.pause()
    const url = "/download_music/" + mic;
    console.log(url)
    
    // sleep before update
    fetch(url, {
      method: 'POST'
    }).then (response => {
      if (response.ok) {
        console.log('Download Updated: ' + mic );
        // window.location.reload();
      } else {
        console.error('Failed to Download item pid: ' + mic );
      }
    }).catch(error => {
      console.error('Error during fetching: ' + error);
    })
  }


  let currentAudio = null;  // Track the currently playing audio
  let currentButton = null; // Track the currently active button
  let timeoutId = null;     // Track the timeout to stop the music after 30 seconds
  
  function playMusic(pid, mic) {
    const playButton = document.getElementById('play-' + mic);
  
    // If the current song is already playing and the same button is clicked, pause it
    if (currentAudio && currentAudio.src.includes(pid)) {
      if (!currentAudio.paused) {
        currentAudio.pause();
        playButton.innerHTML = '<i class="ion-ios-play"></i> Play';
        clearTimeout(timeoutId); // Clear timeout if paused
      } else {
        // Resume if paused
        currentAudio.play();
        playButton.innerHTML = '<i class="ion-ios-pause"></i> Pause';
  
        // Resume the timeout with the remaining time
        timeoutId = setTimeout(() => {
          currentAudio.pause();
          currentAudio.currentTime = 0; // Reset to the beginning
          playButton.innerHTML = '<i class="ion-ios-play"></i> Play';
          currentAudio = null;
        }, 30000 - currentAudio.currentTime * 1000); // Adjust timeout for remaining time
      }
      return; // Exit here as we're just toggling play/pause on the same song
    }
  
    // If a different song is playing, pause the current one and reset the button
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      if (currentButton) {
        currentButton.innerHTML = '<i class="ion-ios-play"></i> Play';
      }
      clearTimeout(timeoutId); // Clear previous timeout
    }
  
    // Create a new audio element for the selected track
    currentAudio = new Audio('static/' + pid);
    currentButton = playButton;
  
    // Play the new song
    currentAudio.play();
    playButton.innerHTML = '<i class="ion-ios-pause"></i> Pause';
  
    // Set a timeout to stop the music after 30 seconds
    timeoutId = setTimeout(() => {
      currentAudio.pause();
      currentAudio.currentTime = 0; // Reset to the beginning
      playButton.innerHTML = '<i class="ion-ios-play"></i> Play';
      currentAudio = null;
    }, 30000); // 30 seconds in milliseconds
  
    // Add event listener to reset button once the song ends naturally
    currentAudio.onended = function() {
      playButton.innerHTML = '<i class="ion-ios-play"></i> Play';
      currentAudio = null;
    };
  
    // Send a request to update play status
    const url = "/play_music/" + mic;
    fetch(url, {
      method: 'POST'
    }).then(response => {
      if (response.ok) {
        console.log('Play Updated: ' + mic);
      } else {
        console.error('Failed to Play item pid: ' + mic);
      }
    }).catch(error => {
      console.error('Error during fetching: ' + error);
    });
  }
  