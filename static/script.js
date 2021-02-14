// var socket = io.connect();

// socket.on('connect', function () {
//     socket.send('I am now connected!');
//     console.log("connected");

//     socket.on('message', function (massage) {
//         console.log(massage);
//         // // $("#refresh").load(window.location.href + " #refresh");
//         // location.reload();

//     })
//     socket.on('redirect', function (data) {
//         // window.location = data.url;
//         $("#refresh").load(window.location.href + " #refresh");
//         $("#refresh2").load(window.location.href + " #refresh2");

//     });
// });


var myInterval = setInterval(refresh, 5000);
function refresh(){
    window.location.reload()
}

function myStopFunction(){
    clearInterval(myInterval);
}



    





