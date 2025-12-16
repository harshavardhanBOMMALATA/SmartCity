document.getElementById("postForm").addEventListener("submit", (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const shortdescription = document.getElementById("shortdescription").value;
    const description = document.getElementById("description").value;
    const location = document.getElementById("location").value;

    fetch("/api/new_post/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            short_description: shortdescription,
            description: description,
            location: location,
            time: new Date().toISOString(),
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Post created successfully!");
            window.location.href = "/home/";
        } else {
            if(data.status==="logout"){
                alert("You are not logged in. Redirecting to login page.");
                window.location.href = "/";
                return;
            }
            alert("Error creating post: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong");
    });
});
