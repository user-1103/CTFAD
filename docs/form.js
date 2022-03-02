
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

digestMessage(text)
    .then(digestHex => console.log(digestHex));

function notify_send(message) {
    console.log(message)
}

function check_flag() {
    let flag_guess = document.getElementById("flag_guess").value;
    let flag_hash = document.getElementById("flag_hash").innerHTML;
    let username_element = document.getElementById("A1");
    let check_element = document.getElementById("A2");
    let email_element = document.getElementById("B1");
    console.log(flag_hash);
    console.log(flag_guess);
    digestMessage(flag_guess).then(
        (guess_hash) => {
            if (guess_hash == flag_hash){
                notify_send("Nice! Thats a valid flag!");
                username_element.classList.remove("d-none");
                check_element.classList.remove("d-none");
            } else {
                notify_send("Thats not the flag!");
                username_element.classList.add("d-none");
                check_element.classList.add("d-none");
            }
        }
    ).catch(
        (error) => {
            notify_send(`Err hashing flag: ${error}`);
        }
    );
}



