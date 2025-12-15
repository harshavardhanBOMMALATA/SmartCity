window.onload = function () {
    const form = document.getElementById('accountcreation');

    if (!form) {
        return;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const name = document.getElementsByName('name')[0].value.trim();
        const email = document.getElementsByName('email')[0].value.trim();
        const phonenumber = document.getElementsByName('phonenumber')[0].value.trim();
        const password = document.getElementsByName('password')[0].value.trim();
        const address = document.getElementsByName('address')[0].value.trim();

        fetch('/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                phonenumber: phonenumber,
                password: password,
                address: address
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Signup successful');
                window.location.href = '/';
            } else if (data.status === 'exists') {
                document.getElementsByClassName('message1')[0].innerText =
                    'User already exists';
            } else {
                document.getElementsByClassName('message1')[0].innerText =
                    'Signup failed';
            }
        })
        .catch(error => {
            console.error(error);
            document.getElementsByClassName('message1')[0].innerText =
                'Error during signup';
        });
    });
};

