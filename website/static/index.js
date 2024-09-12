function viewUser(userId) {

    console.log("Hi");
    // we want to pass the user id from the selected user to our home page endpoint
    fetch('/view-users', {
        method: 'POST',
        body: JSON.stringify({userId: userId})
    }).then((_res) => {
        window.location.href = "/home";
        console.log("User id successfully sent")
    })
}



