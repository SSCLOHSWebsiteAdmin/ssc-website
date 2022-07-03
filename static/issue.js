function getPoints()
{
    var textSide = document.getElementById("textSide");
    var markers = document.getElementsByClassName("marker");
    var points = [];
    for (let i = 0; i < markers.length; i++)
    {
        console.log("marker: " + String(markers[i].offsetTop) + " textside: " + String(textSide.offsetTop));
        if (window.innerWidth <  600)
        {
            points.push(markers[i].offsetTop - textSide.offsetTop);
        }
        else
        {
            points.push(markers[i].offsetTop);
        }
    }

    return points;
}

function checkTransition()
{

    var points = getPoints();
    var section = 0;
    var textSide = document.getElementById("textSide");
    var windowElem = document.getElementById("window");
    var body = document.getElementsByTagName("BODY")[0];
    if (10 < textSide.scrollTop && textSide.scrollTop < textSide.scrollHeight - textSide.offsetHeight - 10)
    {
        console.log(String(textSide.scrollTop) + " " + String(textSide.scrollTop + (textSide.offsetHeight*(2/3))) + " " + points[section].toString());
        window.scrollTo(0,windowElem.offsetTop-45);
    }

    while (points[section] < textSide.scrollTop + (textSide.offsetHeight*(2/3)))
    {
        section = section + 1;
    }
    var images = document.getElementById("imageSide").children;

    for (let i = 0; i < images.length; i++)
    {

        if (images[i].classList.contains("show"))
        {
            images[i].classList.add("hide");
            images[i].classList.remove("show");
        }
    }

    images[section].classList.add("show");
    images[section].classList.remove("hide");
}

points = getPoints();
setInterval(checkTransition, 100);