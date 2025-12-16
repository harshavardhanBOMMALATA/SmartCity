function editField(field){
    document.getElementById(field + "Text").style.display = "none";
    document.getElementById(field + "Input").style.display = "block";
    document.getElementById("submitBtn").style.display = "inline-block";
}

function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


function submitProfile(){
    const name = document.getElementById("nameInput").value;
    const phone = document.getElementById("phoneInput").value;
    const address = document.getElementById("addressInput").value;

    fetch("/home/profile/api/update_profile/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            name: name,
            phonenumber: phone,
            address: address
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById("nameText").innerText = data.profile.name;
            document.getElementById("phoneText").innerText = data.profile.phonenumber;
            document.getElementById("addressText").innerText = data.profile.address;
            document.getElementById("submitBtn").style.display = "none";
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
}


function changePhoto(){
    const input = document.getElementById("photoInput");
    input.click();
    input.onchange = function(){
        const file = input.files[0];
        if(file){
            const reader = new FileReader();
            reader.onload = e => {
                document.getElementById("profileImg").src = e.target.result;
                document.getElementById("submitBtn").style.display = "inline-block";
            };
            reader.readAsDataURL(file);
        }
    };
}

document.addEventListener("DOMContentLoaded", () => {
    fetch("/home/profile/api/profile_data/")
        .then(response => response.json())
        .then(data => {
            if(data.status === "success"){
                document.getElementById("nameText").innerText = data.profile.name;
                document.getElementById("emailText").innerText = data.profile.email;
                document.getElementById("phoneText").innerText = data.profile.phonenumber;
                document.getElementById("addressText").innerText = data.profile.address;
            } else {
                window.location.href = "/";
                alert("Error loading profile: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error fetching profile:", error);
        });
});
