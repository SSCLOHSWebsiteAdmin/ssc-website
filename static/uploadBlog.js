function up(element)
{
    image = element.parentElement;
    div = image.parentElement;
    image.remove();
    div.appendChild(image);
}

function deleteImage(element)
{
    image = element.parentElement;
    image.remove();
}

function addImage()
{
    var inputList = document.getElementById("files")
    var images = inputList.children;

    for (let i = 0; i < images.length; i++)
    {
        if (images[i].value != "" && images[i].hidden == false)
        {
            images[i].hidden = true;

            var div = document.getElementById("imageList");
            var item = document.createElement("p");
            item.innerHTML = "<span class='button' onclick='up(this)'>^</span>" + images[i].value + "<span class='button' onclick='deleteImage(this)'>delete</span>";
            div.appendChild(item);

            var x = document.createElement("INPUT");
            x.setAttribute("type", "file");
            x.name = "file";
            inputList.appendChild(x);
        }
    }
}

setInterval(addImage,100);