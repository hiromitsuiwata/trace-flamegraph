package com.example.rest;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@Path("/helloworld")
public class HelloWorldResource {
    @GET
    public String sayHelloWorld() {
        waitFor(100L);
        System.out.println(this.sayHello());
        waitFor(300L);
        return "Hello World";
    }

    public String sayHello() {
        waitFor(200L);
        return "sayHello";
    }

    private void waitFor(long milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
