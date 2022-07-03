function setupClouds(number)
{
    var parent = document.getElementById("clouds");
    for (i=0;i<number;i++)
    {
        var cloud = document.createElement("img");
        cloud.setAttribute("src", "static/cloud.svg");
        cloud.setAttribute("class", "cloud");
        var x = (Math.floor(Math.random() * 100)-10).toString() + "vw";
        var y = Math.floor(Math.random() * 100).toString() + "%";
        //alert(x);
        cloud.style.left = x;
        cloud.style.top = y;
        var dur = (110 - parseInt(clouds.children[i].style.left))/5;
        clouds.children[i].style.transitionDuration = dur.toString() + "s";
        parent.appendChild(cloud);
    }
    moveClouds();
    setInterval(function(){moveClouds();}, 5000);
}

function moveClouds()
{
    moveCloudsY();
    moveCloudsX();
}
function moveCloudsY()
{
    var clouds = document.getElementById("clouds");

    if (clouds.classList.contains("up"))
    {
        clouds.classList.remove("up");
        clouds.classList.add("down");
    }
    else
    {
        clouds.classList.remove("down");
        clouds.classList.add("up");
    }
}

function moveCloudsX()
{
    for (i=0;i<clouds.children.length;i++)
    {
        var x = parseInt(clouds.children[i].style.left);
        if (x > 110 && clouds.children[i].style.transitionDuration != "0s")
        {
            clouds.children[i].style.transitionDuration = "0s";
        }
        else if (x>110 && clouds.children[i].style.transitionDuration == "0s")
        {
            x = (Math.floor(Math.random() * -25)-15);
            clouds.children[i].style.left = x.toString() + "vw";
            clouds.children[i].style.top = Math.floor(Math.random() * 80).toString() + "%";
        }
        else if (x<0 && clouds.children[i].style.transitionDuration == "0s")
        {
            var dur = (110 - parseInt(clouds.children[i].style.left))/5;
            clouds.children[i].style.transitionDuration = dur.toString() + "s";
        }
        else if (x<0)
        {
            clouds.children[i].style.left = "110vw";
        }
    }
}