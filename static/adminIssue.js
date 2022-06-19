function newSlide(that)
{
    var div = document.createElement("div");
    div.innerHTML = '<center><input type=file name="file"><br><div class="button" onclick="newText(this)">New Text</div><input type="hidden" name="text" value="Among us"></center><hr>'
    that.parentElement.insertBefore(div, that);

}

function newText(that)
{
    var ta = document.createElement("TEXTAREA");
    ta.name = "text";

    var br = document.createElement("br");
    that.parentElement.insertBefore(ta, that);
    that.parentElement.insertBefore(br, that);
}