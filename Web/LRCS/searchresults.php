<?php  
 //pagination.php  
 $connect = mysqli_connect("localhost", "visuala1_LARankingUser", "LAP@s$", "visuala1_LaRanking");  
$type = $_POST['type'];

$query_type = "";
$val = "";

if(strcmp($type,'journal')==0){
 	$query_type="Journal";
  $val = "Journals";
}
else{
	$query_type="Conference Proceedings";
  $val = "Conferences";

}


 
$query_text = "Select Title, `citation count`, year_auto from elsevier Where type='" . $query_type ."'";
$output = '';
 if ($connect) {
 
 $query = $query_text . " order by `citation count` desc limit 10";
 
 
 $result = mysqli_query($connect, $query);  
 if(!$result){
 	echo mysqli_error($connect);
 }
 $output .= "  
      <table class='table table-bordered'>  
           <tr>  
                <th>$val</th>  
                <th>Citation_Count</th>
                <th>Year</th>
           </tr>  
 ";  
 while($row = mysqli_fetch_array($result))  
 {  
      $output .= '  
           <tr>  
                <td>'.$row["Title"].'</td>            
                <td>'.$row["citation count"].'</td> 
                <td>'.$row["year_auto"].'</td> 
           </tr>  
      ';  
 }  
 $output .= '</table>';  
 echo $output;
} else {
  echo 'not conected';
}

   
 ?>