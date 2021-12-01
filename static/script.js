function moveCarousel(button, direction)
{
    // direction: negative is left, positive is right
    var items = button.parentNode.children[1].children;

    for (i=0; i<items.length; i++)
    {
        if (items[i].classList.contains("shown-carousel-item"))
        {
            items[i].classList.add("hidden-carousel-item")
            items[i].classList.remove("shown-carousel-item")
            var index = i;
        }
    }
    index = index + direction;
    if (index >= items.length)
    {
        index = 0;
    }
    else if (index < 0)
    {
        index = items.length - 1;
    }

    items[index].classList.remove("hidden-carousel-item")
    items[index].classList.add("shown-carousel-item")
}
