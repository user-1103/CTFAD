
async function digestMessage(message) {
    // Stolen striaght from https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest#converting_a_digest_to_a_hex_string
    const msgUint8 = new TextEncoder().encode(message);
    // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
    // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer));                     
    // convert buffer to byte array
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');     // convert bytes to hex string
    return hashHex;
}

function notify_send(message) {
    let valid_note = document.getElementById("valid_note");
    valid_note.innerHTML = message;
}

function check_flag() {
    let flag_guess = document.getElementById("flag_guess").value;
    let flag_hash = document.getElementById("flag_hash").innerHTML;
    let username_element = document.getElementById("A1");
    let check_element = document.getElementById("A2");
    let sub_element = document.getElementById("sub_but");
    let email_element = document.getElementById("B1");
    let comment_element = document.getElementById("C1");
    let check_element2 = document.getElementById("do_comment");
    console.log(flag_hash);
    console.log(flag_guess);
    digestMessage(flag_guess).then(
        (guess_hash) => {
            if (guess_hash == flag_hash.trim()){
                notify_send("✓");
                username_element.classList.remove("d-none");
                check_element.classList.remove("d-none");
                sub_element.classList.remove("d-none");
                check_element2.classList.remove("d-none");
                console.log(guess_hash);
            } else {
                notify_send("✕");
                username_element.classList.add("d-none");
                check_element.classList.add("d-none");
                sub_element.classList.add("d-none");
                email_element.classList.add("d-none");
                check_element2.classList.add("d-none");
                comment_element.classList.add("d-none");
                console.log(guess_hash);
            }
        }
    ).catch(
        (error) => {
            notify_send('?');
        }
    );
}

function check_comment(){
    let comment_element = document.getElementById("C1");
    let check_element2 = document.getElementById("do_comment");
    if (check_element2.checked){
        comment_element.classList.remove("d-none");
    } else {
        comment_element.classList.add("d-none");
    }
}

function check_reg(){
    let email_element = document.getElementById("B1");
    let check_element = document.getElementById("do_register");
    if (check_element.checked){
        email_element.classList.remove("d-none");
    } else {
        email_element.classList.add("d-none");
    }
}

function send_request(flag, username, comment="", email=null){

