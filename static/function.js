const textarea = document.querySelector("textarea"),
speechBtn = document.getElementById("ts");
const resetButton = document.getElementById("reset");
resetButton.addEventListener("click", reset);

    let synth = speechSynthesis,
    isSpeaking = true;

    function textToSpeech(text){
        let utterance = new SpeechSynthesisUtterance(text);
        synth.speak(utterance);
    }

    speechBtn.addEventListener("click", e =>{
        e.preventDefault();
        if(textarea.value !== ""){
            if(!synth.speaking){
                textToSpeech(textarea.value);
            }
            if(textarea.value.length > 80){
                setInterval(()=>{
                    if(!synth.speaking && !isSpeaking){
                        isSpeaking = true;
                        speechBtn.innerText = "Convert To Speech";
                    }else{
                    }
                }, 500);
                if(isSpeaking){
                    synth.resume();
                    isSpeaking = false;
                    speechBtn.innerText = "Pause Speech";
                }else{
                    synth.pause();
                    isSpeaking = true;
                    speechBtn.innerText = "Resume Speech";
                }
            }else{
                speechBtn.innerText = "Convert To Speech";
            }
        }
    });
    function reset() {
        synth.cancel();
    }