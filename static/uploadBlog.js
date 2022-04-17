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