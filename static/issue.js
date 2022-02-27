function getPoints()
{
    var markers = document.getElementsByClassName("marker");
    var points = [];
    for (let i = 0; i < markers.length; i++)
    {
        points.push(markers[i].offsetTop);
    }

    return points;
}

function checkTransition()
{

    var points = getPoints();
    var section = 0;
    var textSide = document.getElementById("textSide");

    while (points[section] < textSide.scrollTop + 500)
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