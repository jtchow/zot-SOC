function showContents(id) {
    var contents = document.getElementById("big-requirement-contents");
    var id_num = String(id).charAt(7);
    var selected = document.getElementById(id_num);
    contents.innerHTML = selected;
    // var selected = document.getElementById(id);
    // selected.style.display = "block";
    // big_requirement_contents.innerHTML = "<p>hi</p>";
}

// var big_reqs = document.getElementsByClassName('big_requirement');
// var i;

// for (big_req in big_reqs) {
//     // console.log(big_reqs[i]);
//     big_reqs[i].addEventListener("click", showContents(big_req));    
// }

// <script>
//     var big_reqs = document.getElementsByClassName('big_requirement');
//     var i;
//     for (i = 0; i < big_reqs.length; i++) {
//          var id = String(big_reqs[i].id);
//          big_reqs[i].addEventListener("click", showContents(id));   
     

// </script>