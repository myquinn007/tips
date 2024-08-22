const select = document.querySelector(".select");
const options_list = document.querySelector(".options-list");
const options = document.querySelectorAll(".option");

//show & hide options list
select.addEventListener("click", () => {
  options_list.classList.toggle("active");
  select.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});

//select option
options.forEach((option) => {
  option.addEventListener("click", () => {
    options.forEach((option) => { option.classList.remove('selected') });
    select.querySelector("span").innerHTML = option.innerHTML;
    option.classList.add("selected");
    options_list.classList.toggle("active");
    select.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
  });
});


const select_user = document.querySelector(".select-user");
const options_list_user = document.querySelector(".options-list-user");
const options_user = document.querySelectorAll(".option-user");

//show & hide options list
select_user.addEventListener("click", () => {
  options_list_user.classList.toggle("active");
  select_user.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});

//select option
options_user.forEach((option) => {
  option.addEventListener("click", () => {
    options_user.forEach((option) => { option.classList.remove('selected') });
    select_user.querySelector("span").innerHTML = option.innerHTML;
    option.classList.add("selected");
    options_list_user.classList.toggle("active");
    select_user.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
  });
});

const email_select = document.querySelector(".email-select");
const email_options_list = document.querySelector(".email-options-list");
const email_options = document.querySelectorAll(".email-option");

//show & hide options list
email_select.addEventListener("click", () => {
  email_options_list.classList.toggle("active");
  email_select.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
});

//select option
email_options.forEach((option) => {
  option.addEventListener("click", () => {
    email_options.forEach((option) => { option.classList.remove('selected') });
    email_select.querySelector("span").innerHTML = option.innerHTML;
    option.classList.add("selected");
    email_options_list.classList.toggle("active");
    email_select.querySelector(".fa-angle-down").classList.toggle("fa-angle-up");
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


