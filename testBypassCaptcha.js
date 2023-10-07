var anyCaptchaToken = 'ADD_TOKEN_HERE';
var enc = document.getElementById('enforcementFrame');
var encWin = enc.contentWindow || enc;
var encDoc = enc.contentDocument || encWin.document;
let script = encDoc.createElement('SCRIPT');
script.append('function AnyCaptchaSubmit(token) { parent.postMessage(JSON.stringify({ eventId: "challenge-complete", payload: { sessionToken: token } }), "*") }');
encDoc.documentElement.appendChild(script);
encWin.AnyCaptchaSubmit(anyCaptchaToken);

