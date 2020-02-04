// To install dependencies, run: npm install
const xmlbuilder = require('xmlbuilder');
// request-promise has a dependency on request
const rp = require('request-promise');
const fs = require('fs');
const readline = require('readline-sync');


// Gets an access token.
function getAccessToken(subscriptionKey) {
    let options = {
        method: 'POST',
        uri: 'https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken',
        headers: {
            'Ocp-Apim-Subscription-Key': subscriptionKey
        }
    }
    return rp(options);
}

// Converts text to speech using the input from readline.
function textToSpeech(accessToken, text) {
    // Create the SSML request.
    let xml_body = xmlbuilder.create('speak')
        .att('version', '1.0')
        .att('xml:lang', 'fr-fr')
        .ele('voice')
        .att('xml:lang', 'fr-fr')
        .att('name', 'fr-FR-Julie-Apollo') // Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        .txt(text)
        .end();
    // Convert the XML into a string to send in the TTS request.
    let body = xml_body.toString();
    console.log(body);

    let options = {
        method: 'POST',
        baseUrl: 'https://francecentral.tts.speech.microsoft.com/',
        url: 'cognitiveservices/v1',
        headers: {
            'Authorization': 'Bearer ' + accessToken,
            'cache-control': 'no-cache',
            'User-Agent': 'YOUR_RESOURCE_NAME',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'Content-Type': 'application/ssml+xml'
        },
        body: body
    }

    let request = rp(options)
        .on('response', (response) => {
            if (response.statusCode === 200) {
                request.pipe(fs.createWriteStream('TTSOutput.wav'));
                console.log('\nYour file is ready.\n')
            }
        });
    return request;

};

// Use async and await to get the token before attempting
// to convert text to speech.
async function main() {
    // Reads subscription key from env variable.
    // You can replace this with a string containing your subscription key. If
    // you prefer not to read from an env variable.
    const subscriptionKey = "0cf90ceec03c44a6942e8ae5066457ee";
    //const subscriptionKey = process.env.SPEECH_SERVICE_KEY;
    if (!subscriptionKey) {
        throw new Error('Environment variable for your subscription key is not set.')
    };
    // Prompts the user to input text.
    const text = readline.question('What would you like to convert to speech? ');

    try {
        const accessToken = await getAccessToken(subscriptionKey);
        await textToSpeech(accessToken, text);
    } catch (err) {
        console.log(`Something went wrong: ${err}`);
    }
}

// Run the application
main()