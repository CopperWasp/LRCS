<?php  
 //pagination.php  
 $connect = mysqli_connect("localhost", "visuala1_LARankingUser", "LAP@s$", "visuala1_LaRanking");  
 
 
 $keywords = $_POST['keywords'];

$query_keywords = "";

if(strcmp($keywords,'')==0){
 	$query_keywords="Title IS NOT NULL";
}
else{
	$query_keywords="Title like '%" . $keywords . "%'";
}


 
//$query_text = "Select Title,Rank,`Scopus Sub-Subject Area`,`Citation Count`,`Scholarly Output`,Publisher,year_auto from elsevier Where " . $query_keywords;

$query_text = "select Title,Rank,`Scopus Sub-Subject Area`,`Citation Count`,`Scholarly Output`,Publisher,year_auto from (select Title,Rank,`Scopus Sub-Subject Area`,`Citation Count`,`Scholarly Output`,Publisher,year_auto, match(Title) against ('" .$keywords." ') as score from elsevier where (match(Title) against ('".$keywords."')) > 0 order by score desc) A";
 
 if ($connect) {
 $record_per_page = 20;  
 $page = '';  
 $output = '';  
 if(isset($_POST["page"]))  
 {  
      $page = $_POST["page"];  
 }  
 else  
 {  
      $page = 0;  
 }  
 $start_from = $page;  
 $query = $query_text. " LIMIT ". $start_from.",". $record_per_page;  
 $result = mysqli_query($connect, $query);  
 if(!$result){
 	echo mysqli_error($connect);
 }
 $output .= "  
      <ul class='resultList'>  
 ";  
 while($row = mysqli_fetch_array($result))  
 {  
      $output .= '  
           <li class="resultItem"> 
           		<div style="display:block; float:left; text-align:left;">
           	    <div class="resultTitle" style="font-weight:bold;">'.$row["Title"].'</div>
           	    <div class="resultCiteScore">Citation Count: '.$row["Citation Count"].'</div>
           	    <div class="resultPercent_Cited">Subject Area: '.$row["Scopus Sub-Subject Area"].'</div>
           	    </div>
           	    <div class="resultYear" style="float:right;">'.$row["year_auto"].'</div>
           	    <div style="clear:both"></div>
           	   	
				
           </li>  
      ';  
 }  
 $output .= '</ul>';  
 $page_query = $query_text;
 $page_result = mysqli_query($connect, $page_query);  
 $total_records = mysqli_num_rows($page_result);  
 $total_pages = (ceil($total_records/$record_per_page));  
 
 $output .="<span class='text'>".$page." - ".min(($page+$record_per_page),$total_records)." of ".$total_records."</span>";
 
 if($page==0){
 	 $output .= "<span class='pagination_link_deactivated fa fa-chevron-left' style='cursor:pointer; padding:6px; border:1px solid #ccc;color:red' id='".($page-$record_per_page)."'></span>";  
 }
 else{
 	 $output .= "<span class='pagination_link fa fa-chevron-left' style='cursor:pointer; padding:6px; border:1px solid #ccc;' id='".($page-$record_per_page)."'></span>";  
 }
 
 if(($page+$record_per_page)<$total_records){
 	 	 $output .= "<span class='pagination_link fa fa-chevron-right' style='cursor:pointer; padding:6px; border:1px solid #ccc;' id='".($page+$record_per_page)."'></span>";  			
 }
 else{
 	 	 $output .= "<span class='pagination_link_deactivated fa fa-chevron-right' style='cursor:pointer; padding:6px; border:1px solid #ccc;color:red;' id='".($page+$record_per_page)."'></span>";  
 }
 
$output .= '</div><br /><br />';  
 echo $output;
} else {
  echo 'not conected';
}

   
 ?>