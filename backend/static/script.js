document.addEventListener("DOMContentLoaded", function() {
    const videoList = document.getElementById("video-list");
  
    fetch("/list")
      .then(response => response.json())
      .then(data => {
        // Clear existing content in case this script runs multiple times
        videoList.innerHTML = "";
  
        data.forEach(video => {
          const videoElement = document.createElement("div");
          videoElement.innerHTML = `<h2><a href="/watch?id=${video.id}">${video.filename}</a></h2> Video Processed: ${video.processed} <br> <a href="/delete?id=${video.id}">Delete</a>`;
          videoList.appendChild(videoElement);
        });
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  });