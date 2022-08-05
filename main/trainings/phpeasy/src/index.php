<?php
    error_reporting(0);
    require_once("flag.php");
    if(!isset($_GET["a"])){
        show_source(__FILE__);
    }
    else if($_GET['a']!=$_GET['b'] && md5($_GET['a'])===md5($_GET['b'])){     
        echo $flag;
    }
    else{
        show_source(__FILE__);
    }
?>
