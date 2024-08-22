
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
const select_playlist = document.querySelector(".select_span_playlist");
const options_list_playlist = document.querySelector(".options-list-playlist");
const options_playlist = document.querySelectorAll(".option-playlist");

//show & hide options list
select_playlist.addEventListener("click", () => {
  options_list_playlist.classList.toggle("active");
  select_playlist.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});
options_playlist.forEach((option) => {
  option.addEventListener("click", () => {
    options_playlist.forEach((option) => { option.classList.remove('selected') });
    select_playlist.querySelector(".sort_by").innerHTML = option.innerHTML;
    //options1.classList.add("selected");
    options_list_playlist.classList.toggle("active");
    select_playlist.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
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
