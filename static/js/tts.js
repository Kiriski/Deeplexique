const subscriptionKey = "0cf90ceec03c44a6942e8ae5066457ee";

// Gets an access token -> this need to be on server side
function request_AccessToken_From_Azure(subscriptionKey) {
    return new Promise(function (resolve, reject) {
        let req = new XMLHttpRequest();
        req.open('POST', 'https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken');
        req.setRequestHeader('Ocp-Apim-Subscription-Key', subscriptionKey);
        req.onload = () => {
            if (req.status >= 200 && req.status < 300) {
                resolve(req.responseText);
            } else {
                reject({
                    status: req.status,
                    statusText: req.statusText
                });
            }
        };
        req.onerror = function () {
            reject({
                status: req.status,
                statusText: req.statusText
            });
        };
        req.send();
    });
}

function request_TTS_AudioData_From_azure(phrase, accessToken) {
    return new Promise(function (resolve, reject) {
        let req = new XMLHttpRequest();
        req.open('POST', 'https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1');
        req.setRequestHeader('Content-Type', 'application/ssml+xml');
        req.setRequestHeader('Authorization', 'Bearer ' + accessToken);
        req.setRequestHeader('cache-control', 'no-cache');
        req.setRequestHeader('X-Microsoft-OutputFormat', 'riff-24khz-16bit-mono-pcm');
        req.responseType = "arraybuffer";
        req.onload = () => {
            if (req.status >= 200 && req.status < 300) {
                resolve(req.response);
            } else {
                reject({
                    status: req.status,
                    statusText: req.statusText
                });
            }
        };
        req.onerror = () => {
            reject({
                status: req.status,
                statusText: req.statusText
            });
        };
        req.send(`<?xml version="1.0"?><speak version="1.0" xml:lang="fr-fr"><voice xml:lang="fr-fr" name="fr-FR-Julie-Apollo">${phrase}</voice></speak>`);
    });
}

function play_audio(audio_data) {
    return new Promise(function (resolve, reject) {
        var soundContext = new window.AudioContext();
        var source = soundContext.createBufferSource();
        soundContext.decodeAudioData(audio_data, function (newBuffer) {
            source.buffer = newBuffer;
            source.onended = () => { resolve(); }
            source.connect(soundContext.destination);
            source.start(0);
        });
    });
}

async function text_to_speech(phrase) {
    console.log(`tts => ${phrase}`)
    var accessToken = await request_AccessToken_From_Azure(subscriptionKey);
    var data_wave = await request_TTS_AudioData_From_azure(phrase, accessToken);
    await play_audio(data_wave);
}
