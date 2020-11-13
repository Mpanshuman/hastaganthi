console.log('hey')
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
      }
    function reload_auto() {
        btn = document.querySelector('#btn-interest')
        btn.innerHTML = "remove";
        console.log('hello')
        
    }
    //   function interest() {

    //     // let btn = document.querySelector('#btn-interest');
    //     // console.log('hey there')
    //     // let btn_name = document.querySelector('#btn-interest').name;
    //     // btn.innerHTML = "Remove";
    //     // btn_value = "remove";
    //     location.reload()
    //     return false;
    // }

    // function notinterest() {
    //     // let btn = document.querySelector('#btn-remove');
    //     // console.log('hey there2')
    //     // let btn_name = document.querySelector('#btn-remove').name;
    //     // btn.innerHTML = "Interested?";
    //     // btn_value = "interest";
    //     location.reload()
    //     return false;
    // }
