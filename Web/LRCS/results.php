<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>LA Ranking</title>
    <meta name="description" content="Ranking, Journals, Conferences">
    <meta name="keywords" content="Ranking, Journals, Conferences	">
    
    <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Open+Sans|Candal|Alegreya+Sans">
    <link rel="stylesheet" type="text/css" href="css/font-awesome.min.css">
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/imagehover.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

	<script type="text/javascript" src="js/jquery.paginate.js"></script>
	<script type="text/javascript" src="js/jquery.paginate.min.js"></script>
	
    <link rel="stylesheet" type="text/css" href="css/style.css">

    
    <style type="text/css">
a.disabled {
    text-decoration: none;
    color: black;
    cursor: default;
}
</style>

  </head>
  <body>
    <!--Navigation bar-->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="index.php">LRSC<span> </span></a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
        <ul class="nav navbar-nav navbar-right">
           <li><a href="aboutus.php">About Us</a></li>
          <li><a href="#">Methodology</a></li>
          <li><a href="journals.php">Journals</a></li>
          <li><a href="conferences.php">Conferences</a></li>
        </ul>
        </div>
      </div>
    </nav>
    <!--/ Navigation bar-->
    <!--Courses-->
    <section id ="courses" class="section-padding">
      <div class="container">
        <div class="row">
          <div class="header-section text-center" id="Search_Results">
          

          </div>
        </div>
      </div>
      
    </section>
    <!--/ Courses-->
    
    <!--Footer-->
    <footer id="footer" class="footer">
      <div class="container text-center">    
      
        <div class="credits">
            
           <a href="https://louisiana.edu/">© 2017 University of Louisiana at Lafayette. All rights reserved.</a>
        </div>
      </div>
    </footer>
    <!--/ Footer-->
    
    <script src="js/jquery.min.js"></script>
    <script src="js/jquery.easing.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/custom.js"></script>
    <script src="contactform/contactform.js"></script>
    <script>
    $("document").ready(function() {
    	
    	
    	
    	function getAllUrlParams(url) {

  // get query string from url (optional) or window
  var queryString = url ? url.split('?')[1] : window.location.search.slice(1);

  // we'll store the parameters here
  var obj = {};

  // if query string exists
  if (queryString) {

    // stuff after # is not part of query string, so get rid of it
    queryString = queryString.split('#')[0];

    // split our query string into its component parts
    var arr = queryString.split('&');

    for (var i=0; i<arr.length; i++) {
      // separate the keys and the values
      var a = arr[i].split('=');

      // in case params look like: list[]=thing1&list[]=thing2
      var paramNum = undefined;
      var paramName = a[0].replace(/\[\d*\]/, function(v) {
        paramNum = v.slice(1,-1);
        return '';
      });

      // set parameter value (use 'true' if empty)
      var paramValue = typeof(a[1])==='undefined' ? true : a[1];

      // (optional) keep case consistent
      paramName = paramName.toLowerCase();
      paramValue = paramValue.toLowerCase();

      // if parameter name already exists
      if (obj[paramName]) {
        // convert value to array (if still string)
        if (typeof obj[paramName] === 'string') {
          obj[paramName] = [obj[paramName]];
        }
        // if no array index number specified...
        if (typeof paramNum === 'undefined') {
          // put the value on the end of the array
          obj[paramName].push(paramValue);
        }
        // if array index number specified...
        else {
          // put the value at that index number
          obj[paramName][paramNum] = paramValue;
        }
      }
      // if param name doesn't exist yet, set it
      else {
        obj[paramName] = paramValue;
      }
    }
  }

  return obj;
}
		var q = getAllUrlParams().q;
		var qer = q.replace('+',' ');
		load_data();
		function load_data(page){
			$.ajax({  
		url:"pagination.php",  
		method:"POST",  
		data:{
			page:page,
			keywords:qer},
		success:function(data){  
			 $("#Search_Results").html(data);
			}
		});
		}
		$(document).on('click', '.pagination_link', function(){  
        var page = $(this).attr("id");  
        load_data(page);  
         });
		
	}); 
    </script>
    
  </body>
</html>