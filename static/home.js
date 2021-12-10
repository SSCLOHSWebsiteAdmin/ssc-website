function setupClouds(number)
{
    var parent = document.getElementById("clouds");
    for (i=0;i<number;i++)
    {
        var cloud = document.createElement("img");
        cloud.setAttribute("src", "static/cloud.svg");
        cloud.setAttribute("class", "cloud");
        var x = (Math.floor(Math.random() * 100)-10).toString() + "%";
        var y = Math.floor(Math.random() * 100).toString() + "%";
        //alert(x);
        cloud.style.left = x;
        cloud.style.top = y;
        parent.appendChild(cloud);
    }
    setInterval(function(){moveClouds();}, 5000);
}

function moveClouds()
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

    for (i=0;i<clouds.children.length;i++)
    {
        var x = parseInt(clouds.children[i].style.left) + 5;
        if (x > 100)
        {
            x = (Math.floor(Math.random() * -25)-15);
            clouds.children[i].style.transitionDuration = "0s";
            clouds.children[i].style.left = x.toString() + "vw";
            clouds.children[i].style.top = Math.floor(Math.random() * 80).toString() + "%"
        }
        else
        {
            clouds.children[i].style.transitionDuration = "5s";
            clouds.children[i].style.left = x.toString() + "vw";
        }
    }
}