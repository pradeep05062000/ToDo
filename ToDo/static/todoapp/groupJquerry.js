$(document).ready(function(){
  $(".grpSort").click(function () {
    var taskArr = $(".group").map( function() { 
      return $(this).text()
    });
    let temp  ;
    let rows = document.getElementById("myTable").rows;
    for(let j=0; j < taskArr.length; j++) {
      for(let i = 1; i < taskArr.length; i++) {
        if(taskArr[i-1].toLowerCase() > taskArr[i].toLowerCase()) {
          temp = taskArr[i-1];
          taskArr[i-1] = taskArr[i];
          taskArr[i] = temp;
          rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
        }
      }
    }
    
  });
});


$(document).ready(function(){
  $(".created").click(function () {
    var taskArr = $(".admins").map( function() { 
      return $(this).text()
    });
    let temp  ;
    let rows = document.getElementById("myTable").rows;
    for(let j=0; j < taskArr.length; j++) {
      for(let i = 1; i < taskArr.length; i++) {
        if(taskArr[i-1].toLowerCase() > taskArr[i].toLowerCase()) {
          temp = taskArr[i-1];
          taskArr[i-1] = taskArr[i];
          taskArr[i] = temp;
          rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
        }
      }
    }
    
  });
});