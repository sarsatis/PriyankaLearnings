package com.priyankalearning.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PriyankaController {

    @GetMapping("/hello")
    public String sayHello(){
        return "Hello";
    }
}
