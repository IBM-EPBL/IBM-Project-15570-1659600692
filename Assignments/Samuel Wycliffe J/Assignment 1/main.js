
document.addEventListener("DOMContentLoaded", function () {

    // Ease in stuff
    setTimeout(function () {
        var replacers = document.querySelectorAll('[data-replace]');
        for (var i = 0; i < replacers.length; i++) {
            let replaceClasses = JSON.parse(replacers[i].dataset.replace.replace(/'/g, '"'));
            Object.keys(replaceClasses).forEach(function (key) {
                replacers[i].classList.remove(key);
                replacers[i].classList.add(replaceClasses[key]);
            });
        }
    }, 1);


    // cloud stuff
    cloud = document.getElementById("cloud");
    var i = 0;
    for (var tag of cloud.getElementsByTagName("li")) {
        tag.style["grid-area"] = `s${i + 1}`;
        i += 1;
    }

});

