<?php  
 //pagination.php  
 $connect = mysqli_connect("localhost", "visuala1_LARankingUser", "LAP@s$", "visuala1_LaRanking");  
 
 header("Content-Type: application/json");
 $jsonreply=array();
 
 $type = 'conferences';

 $queryType="";

  if(strcmp($type,'journals')==0){
 	$queryType="Journal";
 }
 elseif(strcmp($type,'conferences')==0){
 	$queryType="Conference Proceedings";
 }
 else{
 	echo "Error in Data";
 }
 
 
 if ($connect) {
 $record_per_page = 5;  
 $page = '';  
 $output = '';  
 if(isset($_POST["page"]))  
 {  
      $page = $_POST["page"];  
 }  
 else  
 {  
      $page = 1;  
 }  
 $start_from = ($page - 1)*$record_per_page;  
 $query = "SELECT Title,CiteScore,`Percent Cited`,year_auto  FROM elsevier where type='" . $queryType . "'";  
 $result = mysqli_query($connect, $query);   
 while($row = mysqli_fetch_array($result))  
 {  
      $output .= '  
           <tr>  
                <td>'.$row["Title"].'</td>  
                <td>'.$row["CiteScore"].'</td>
                <td>'.$row["Percent Cited"].'</td>  
                <td>'.$row["year_auto"].'</td>  
           </tr>  
      ';  
	  
	  $jsonreply[] = array("title" => $row["Title"],
	  						"citeScore" => $row["CiteScore"],
	  						"percent_Cited" => $row["Percent Cited"],
	  						"year" => $row["year_auto"]
	  );
 }   
 echo json_encode($jsonreply);
 
} else {
  echo 'not conected';
}

   
 ?>