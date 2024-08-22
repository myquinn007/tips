document.addEventListener('DOMContentLoaded', () => {
  const rows = document.querySelectorAll('.hidden-info');
  
  rows.forEach(row => {
    row.addEventListener('click', () => {
      // Toggle the 'active' class to show/hide action buttons
      row.classList.toggle('active');
    });
  });
});

function playMusic(pid, mic){
    let audio = new Audio('static/'+pid)
    audio.play()
    // audio.pause()
    const url = "/play_music/" + mic;
    console.log(url)
  
    // sleep before update
    fetch(url, {
      method: 'POST'
    }).then (response => {
      if (response.ok) {
        console.log('Play Updated: ' + mic );
        //window.location.reload();
      } else {
        console.error('Failed to Play item pid: ' + mic );
      }
    }).catch(error => {
      console.error('Error during fetching: ' + error);
    })
  }
  
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
