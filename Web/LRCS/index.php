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
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    
    
        <link rel="stylesheet" type="text/css" href="css/style.css">


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
        <a class="navbar-brand" href="index.php">LRSC <span> </span></a>
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
    <!--Banner-->
    <div class="banner">
      <div class="bg-color">
        <div class="container">
          <div class="row">
            <div class="banner-text text-center">
                <h2 class="text-dec"></h2>
              <div class="intro-para text-center quote">
                <p class="big-text">Louisiana Ranking System for Computer Science</p>
              </div>
              <div class="container">
		        <div class="row main_search">
		          <div class="form-group has-feedback">
				  <form id="searchbox" action="results.php" method="get">
					  <input type="text" name="q" style="width:50%;" placeholder="Enter Journal or Conference Title" id="searchinput"><br>
					  <input class="btn buttom" type="submit" id="searchbutton" value="Search">
					  
					</form>
				</div>
		        </div>
		      </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--/ Banner-->
    <section id ="courses" class="section-padding">
      <div class="container">
        <div class="row">
          <div class="col-md-6 text-center">
            <h2>Top 10 Journals</h2>
            <div id="journalResults"></div>
            <a href="journals.php"><button type="button" class="btn btn-danger">More Information</button></a>
</div>
          <div class="col-md-6 text-center">
            <h2>Top 10 Conferences</h2>
            <div id="confResults"></div>

            <a href="conferences.php"><button type="button" class="btn btn-danger">More Information</button></a>
          </div>          
          </div>
        </div>
      </div>
      
    </section>
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
    	 $.ajax({
            url: "searchresults.php",
            method:"POST", 
            data:{type:'journal'}, 
            success: function(data) {
             $('#journalResults').html(data);  
            }
        });		
        $.ajax({
            url: "searchresults.php",
            method:"POST", 
            data:{type:'conf'}, 
            success: function(data) {
            	$('#confResults').html(data);  
            }
        });		
    });
    </script>
  </body>
</html>