package com.priyankalearning.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PriyankaController {

    @GetMapping("/app1/hello")
    public String sayHello(){
        return "Hi";
    }

    @GetMapping("/app1/bye")
    public String sayBye(){
        return "Bye";
    }

    @GetMapping("/app1/myname")
    public String sayMyName(){
        return "Sarthak";
    }

    @GetMapping("/app1/mydashname")
    public String sayDashName(){
        return "Saro";
    }

    @GetMapping("/app1/mybroname")
    public String sayBroName(){
        return "Gagan";
    }

}
