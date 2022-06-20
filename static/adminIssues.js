function newIssue()
{
    var url = prompt("Enter the url code for this issue: ");
    document.getElementById("newUrl").value = url;
    document.getElementById("newIssue").submit();
}

function submit(url, decision)
{
    if (confirm("Are you sure you want to " + decision + " issue " + url + "?"))
    {
        document.getElementById("url").value = url;
        document.getElementById("decision").value = decision;
        document.getElementById("form").submit();
    }
}