<?php
    error_reporting(0);
    require_once("flag.php");
    if($_SERVER['REQUEST_METHOD'] !=='POST'){
        die("Please Change Your Method!");
        exit();
    }
    
    else{
        if(!isset($_POST["AVA"])){
            show_source(__FILE__);
        }
        else if($_POST["AVA"] === "cute"){
                if((isset($_GET["web"])) && (($_GET["web"]) === "like")){
                    setcookie("flag","0");
                    if($_COOKIE['flag'] === '1'){
                        echo $flag ;
                    }
                    else{
                        show_source(__FILE__);
                    }
                }
                else{
                    show_source(__FILE__);
                }
        }
    }


