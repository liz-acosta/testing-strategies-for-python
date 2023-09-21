var fileDrag = document.getElementById("file-drag");

function updateProgressBar() {
    var progressBar = document.getElementById('progress-bar');
    let progressBarWidth = document.getElementById('progress-bar').style.width.replace("%", "");
    progressBarWidth = +progressBarWidth + 10
    progressBar.style.width= progressBarWidth + "%";
  }

function showProgressBar() {
  var formButton = document.getElementById('form-button');
  var progressBar = document.getElementById('progress-bar-div');
  
  formButton.setAttribute("hidden", "hidden");
  progressBar.removeAttribute("hidden");
  
  setInterval(updateProgressBar, 1000);
}

