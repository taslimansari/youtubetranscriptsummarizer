const urlInput = document.getElementById('url');
const transcript = document.getElementById("transcript");
const summary = document.getElementById("summary");

urlInput.addEventListener('input', function () {
    const btn = document.getElementById("summarise");
        
    if (this.value !== "") {
        btn.disabled = false;
    } else {
        btn.disabled = true;
    }
    transcript.innerHTML = "<span>Transcript here ....</span>";
    summary.innerHTML = "<span>Summary here ...</span>";
});

const btn = document.getElementById("summarise");
btn.addEventListener("click", function () {
    btn.disabled = true;
    btn.innerHTML = "Summarizing...";
    
    var url = document.getElementById('url').value;
    console.log("URL: ", url)
    fetch("http://127.0.0.1:5000/summary?url=" + url).then((response) => {
        return response.json()
    }).then((jsonResponse) =>  {
        console.log("Response: ", jsonResponse);

        if(jsonResponse.summary === ""){
            transcript.innerHTML = "No transcript found";
            summary.innerHTML = jsonResponse.summary;
        }
        else {
            transcript.innerHTML = jsonResponse.transcript;
            summary.innerHTML = jsonResponse.summary;
        }

        btn.disabled = false;
        btn.innerHTML = "Summarize";
    })
});