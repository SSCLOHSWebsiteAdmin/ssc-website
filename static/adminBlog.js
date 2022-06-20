function submit(number, decision)
{
    if (confirm("Are you sure you want to " + decision + "?"))
    {
        document.getElementById("number").value = number;
        document.getElementById("decision").value = decision;
        document.getElementById("form").submit();
    }
}