
let tracked_chars = [
    'keya', 'keyb', 'keyc', 'keyd', 'keye', 'keyf', 'keyg',
     'keyh', 'keyi', 'keyj', 'keyk', 'keyl', 'keym', 'keyn',
     'keyo', 'keyp', 'keyq', 'keyr', 'keys', 'keyt', 'keyu',
     'keyv', 'keyw', 'keyx', 'keyy', 'keyz',
     'digit0', 'digit1', 'digit2', 'digit3', 'digit4',
     'digit5', 'digit6', 'digit7', 'digit8', 'digit9',
     'backquote', 'minus', 'equal', 'bracketleft',
     'bracketright', 'backslash', 'semicolon', 'quote',
     'comma', 'period', 'slash'
]
let times = [];


function is_tracked_key(code) {
    return tracked_chars.indexOf(code.toLowerCase()) >= 0;
}


function keyDown(event) {
    if (is_tracked_key(event.code)) {
        times.push(Math.round(window.performance.now()));
    }
}


function keyUp(event) {
    if (is_tracked_key(event.code)) {
        times.push(Math.round(window.performance.now()));
    }
}


function checkKeystrokePattern(event) {
    console.log("Sending times:\n\n");
    console.log(times);
    $.ajax({
        url: "/checkTimes",
        type: "POST",
        data: JSON.stringify({
            "times": times,
            "uuid": "demo123demo123demo123demo123demo"
        }),
        contentType: "application/json",
        success: function(data) { console.log("Response from POST: " + data); },
        failure: function(data) { alert("Failure: " + data); }
    });
    times = [];
}


function clearKeystrokeHistory(event) {
    console.log("Clear keystroke history\n");
    $.ajax({
        url: "/clearTimes",
        type: "DELETE",
        data: JSON.stringify({
            "uuid": "demo123demo123demo123demo123demo"
        }),
        success: ()=> { console.log("Successfully cleared history"); },
        failure: ()=> { alert("Failed to clear keystroke history!"); }
    });
}


function setup() {
    let userInput = document.getElementById("userInput")
    userInput.addEventListener("keydown", keyDown);
    userInput.addEventListener("keyup", keyUp);
    document.getElementById("loginButton").addEventListener(
        "click", checkKeystrokePattern);
    document.getElementById("clearButton").addEventListener(
        "click", clearKeystrokeHistory);
}

