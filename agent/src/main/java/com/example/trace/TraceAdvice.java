package com.example.trace;

import java.lang.reflect.Method;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import net.bytebuddy.asm.Advice;

public class TraceAdvice {

    @Advice.OnMethodEnter
    public static void onEnter(@Advice.Origin Class<?> clazz, @Advice.Origin Method method,
            @Advice.AllArguments Object[] args) {
        String threadId = Long.toString(Thread.currentThread().threadId());
        String dateTime = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        String str = String.format("%s %s TraceAdvice onEnter %s#%s", dateTime, threadId, clazz.getName(), method.getName());
        System.out.println(str);
    }

    @Advice.OnMethodExit
    public static void onExit(@Advice.Origin Class<?> clazz, @Advice.Origin Method method,
            @Advice.AllArguments Object[] args) {
                String threadId = Long.toString(Thread.currentThread().threadId());
                String dateTime = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        String str = String.format("%s %s TraceAdvice onExit %s#%s", dateTime, threadId, clazz.getName(), method.getName());
        System.out.println(str);
    }
}
