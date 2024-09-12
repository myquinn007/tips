
const select_user = document.querySelector(".select-user");
const options_list_user = document.querySelector(".options-list-user");
const options_user = document.querySelectorAll(".option-user");

document.addEventListener('DOMContentLoaded', () => {
  const rows = document.querySelectorAll('.music-row');
  
  rows.forEach(row => {
    row.addEventListener('click', () => {
      // Toggle the 'active' class to show/hide action buttons
      row.classList.toggle('active');
    });
  });
});

const select1 = document.querySelector(".select1_span");
const options_list1 = document.querySelector(".options-list1");
const options1 = document.querySelectorAll(".option1");

//show & hide options list
select1.addEventListener("click", () => {
  options_list1.classList.toggle("active");
  select1.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});
options1.forEach((option) => {
  option.addEventListener("click", () => {
    options1.forEach((option) => { option.classList.remove('selected') });
    select1.querySelector(".sort_by").innerHTML = option.innerHTML;
    //options1.classList.add("selected");
    options_list1.classList.toggle("active");
    select1.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
  });
});


const select2 = document.querySelector(".select2_span");
console.log('select2: '+ select2)
const options_list2 = document.querySelector(".options-list2");
const options2 = document.querySelectorAll(".option2");

//show & hide options list
select2.addEventListener("click", () => {
  options_list2.classList.toggle("active");
  select2.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});
options2.forEach((option) => {
  option.addEventListener("click", () => {
    options2.forEach((option) => { option.classList.remove('selected') });
    select2.querySelector(".sort_by").innerHTML = option.innerHTML;
    //options1.classList.add("selected");
    options_list2.classList.toggle("active");
    select2.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
  });
});

function selectMenuGroup(type){
  console.log('hey big boy: '+ type)
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


function userAddListMusic(mic){
  const url = "/user_add_list_add_list/" + mic;
  fetch(url, {
    method: 'POST'
  }).then (response => {
    if (response.ok) {
      console.log('Add List Music Updated: ' + mic );
      window.location.reload();
    } else {
      console.error('Failed to Add to List item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function publishMusic(mic){
  const url = "/publish_input/" + mic;
  fetch(url, {
    method: 'POST'
  }).then (response => {
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to Add to List item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function unpublishMusic(mic){
  console.log('checking id= '+mic)
  const url = "/unpublish_input/" + mic;
  fetch(url, {
    method: 'POST'
  }).then (response => {
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to Add to List item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function editMusic(mic) {
  const url = "/music_edit/" + mic;
  fetch(url, {
    method: 'GET'
  }).then (response => {
    if (response.ok) {
     window.location.reload();
    } else {
      console.error('Failed to Edit item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function saveMusic(mic) {
  const url = "/music_edit/" + mic;
  fetch(url, {
    method: 'GET'
  }).then (response => {
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to Edit item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function deleteMusic(mic) {
  const url = "/music_delete/" + mic;
  fetch(url, {
    method: 'POST'
  }).then (response => {
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to Edit item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

function deletePlaylist(mic) {

  const url = "/playlist_delete/" + mic;
  fetch(url, {
    method: 'POST'
  }).then (response => {
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to Edit item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  })
}

let currentAudio = null;  // Track the currently playing audio

function playMusic(pid, mic) {
  // If a track is already playing, pause it
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0; // Reset audio to the beginning
  }

  // Create a new audio element for the selected track
  currentAudio = new Audio('static/' + pid);

  // Play the selected track
  currentAudio.play();
  
  // Change the button to "Pause" while the track is playing
  let playButton = document.getElementById('play');
  playButton.innerHTML = '<i class="ion-ios-pause"></i> Pause';

  // Stop playing after 30 seconds
  setTimeout(() => {
    currentAudio.pause();
    currentAudio.currentTime = 0; // Reset to the beginning
    playButton.innerHTML = '<i class="ion-ios-play"></i> Play'; // Change button back to "Play"
  }, 30000); // 30 seconds in milliseconds

  // Send a request to update play status
  const url = "/play_music/" + mic;
  fetch(url, {
    method: 'POST'
  }).then(response => {
    if (response.ok) {
      console.log('Play Updated: ' + mic );
    } else {
      console.error('Failed to Play item pid: ' + mic );
    }
  }).catch(error => {
    console.error('Error during fetching: ' + error);
  });

  // Add click event to pause the song when button is clicked again
  playButton.onclick = () => {
    if (!currentAudio.paused) {
      currentAudio.pause();
      playButton.innerHTML = '<i class="ion-ios-play"></i> Play';
    } else {
      currentAudio.play();
      playButton.innerHTML = '<i class="ion-ios-pause"></i> Pause';
    }
  };
}
