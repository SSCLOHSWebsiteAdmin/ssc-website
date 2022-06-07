function newIssue()
{
    var url = prompt("Enter the url code for this issue: ");
    document.getElementById("url").value = url;
    document.getElementById("newIssue").submit();
}