<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Louisiana Ranking System for Computer Science</title>
    <meta name="description" content="Ranking, Journals, Conferences">
    <meta name="keywords" content="Ranking, Journals, Conferences	">
    
    <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Open+Sans|Candal|Alegreya+Sans">
    <link rel="stylesheet" type="text/css" href="css/font-awesome.min.css">
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/imagehover.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <script type="text/javascript" src="js/jquery.min.js"></script>
	<script type="text/javascript" src="js/jquery.paginate.js"></script>
	<script type="text/javascript" src="js/jquery.paginate.min.js"></script>
	
	<script type="text/javascript" src="js/jquery.dynatable.js"></script>
	<link rel="stylesheet" type="text/css" href="css/jquery.dynatable.css">

	
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
          <li><a href="#">Conferences</a></li>
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
          <table id="dynatable">
		    <thead>
		    <th>Title</th>
		    <th>CiteScore</th>
		    <th>Percent_Cited</th>
		    <th>Year</th>
		    </thead>
		    <tr>
		    <td>Title</td>
		    <td>CiteScore</td>
		    <td>Percent_Cited</td>
		    <td>Year</td>
		    </tr>
		</table>

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
    
    
    <script src="js/jquery.easing.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/custom.js"></script>
    
    <script>
    $("document").ready(function() {
    	
    	
    	
        $.ajax({
            url: "paginationjsonconf.php",
            method:"POST",  
            success: function(data) {
                console.log(data);
                //alert(JSON.stringify(data));

                var myRecords = JSON.stringify(data);
                
                console.log(myRecords);

                var dynatable = $('#dynatable').dynatable({
                	table:{
                		defaultColumnIdStyle: 'camelCase'
                	},
                    dataset: {
                        records: data
                    }
                });
            }
        });		
	}); 
    </script>
    
  </body>
</html>