
//This two function are used to sort the personal task in assinging 

//This function is used to sord according to task name
$(document).ready(function(){
  $(".first").click(function () {
  	var taskArr = $(".task").map( function() { 
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

//This function is used to sort according to date
$(document).ready(function(){
  $(".second").click(clickDateOrTime);
});

$(document).ready(function(){
  $(".third").click(clickDateOrTime);
});



const clickDateOrTime = function () {
    
    let s, hr, temp = 0, dateArr = []  ;
    var arr = $(".date").map( function() { 
      return $(this).text().replace(/\./g , '');
    });
    var timeArr = $(".time").map(function() {
      return $(this).text()
    });

    //converting the time format as required for Date() object
    for(let i = 0; i < timeArr.length; i++) {
      s = timeArr[i];
      s = s.match(/(\d+)\:(\d+) (\w+\.\w+\.)/);
      hr =  /a.m./.test(s[3]) ? s[1] === "12" ? "00" : s[1] : s[1] === "12" ? "12" : (Number(s[1]) + 12).toString();
      dateArr.push(arr[i]+' ' + hr + ':' + s[2]); 
    }
    
    let rows = document.getElementById("myTable").rows;

    for(let j=0; j < dateArr.length; j++) {
      for(let i = 1; i < dateArr.length; i++) {
        if(new Date(dateArr[i-1]) > new Date(dateArr[i])) {
          temp = dateArr[i-1];
          dateArr[i-1] = dateArr[i];
          dateArr[i] = temp;
          rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
        }
      }
    } 
}



$(document).ready(function() {

  $(".assigned-to-title").click(() => sortGroup(".assigned-to"))

});

$(document).ready(function() {

  $(".group-task-title").click(() => sortGroup(".group-task"))

});

$(document).ready(function() {

  $(".assigned-by-title").click(() => sortGroup(".assigned-by"))

});


//Insertion sort logic is used in sortGroup()

const sortGroup = async function(sortChoiceVariable) {
     
    var arr = await $(sortChoiceVariable).map(function () {
      return $(this).text().toLowerCase();
    });
    
    
   
    let rows = await document.getElementById("grp-task").rows;
    

   for(let i=1; i < arr.length; i++) {
      let key = arr[i]
      
    for(var j= i-1;( j !== -1 && arr[j] > key); j--) {
        if(arr[j] > key) {
          
          arr[j+1] = arr[j]
          rows[i].parentNode.insertBefore(rows[j+1], rows[j+2]);
          
        }

    }
    
    if(arr[j+1] > key) {
      
      arr[j+1] = key
     rows[i].parentNode.insertBefore(rows[i+1], rows[j+2]);
    }
    

   }

   
  }



