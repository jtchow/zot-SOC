function showContents(id) {
    var id = id.charAt(7);
    var contents = document.getElementById("big-requirement-contents");
    console.log(contents);
    document.getElementById("big-requirement-contents").innerHTML = '<p>hi</p>';
    // var selected = document.getElementById(id);
    // selected.style.display = "block";
    // big_requirement_contents.innerHTML = "<p>hi</p>";
}

var big_reqs = document.getElementsByClassName('big_requirement');
var i;

for (i = 0; i < big_reqs.length; i++) {
    console.log(big_reqs[i]);
    big_reqs[i].addEventListener("click", showContents(this.id));    
}

