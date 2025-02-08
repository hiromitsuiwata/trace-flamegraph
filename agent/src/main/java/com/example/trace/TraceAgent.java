package com.example.trace;

import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;

import net.bytebuddy.agent.builder.AgentBuilder;
import net.bytebuddy.asm.Advice;
import net.bytebuddy.description.type.TypeDescription;
import net.bytebuddy.dynamic.DynamicType.Builder;
import net.bytebuddy.matcher.ElementMatchers;
import net.bytebuddy.utility.JavaModule;

public class TraceAgent {
    public static void premain(String arguments, Instrumentation instrumentation) {
        new AgentBuilder.Default()
                .type(ElementMatchers.nameContains("com.example"))
                .transform(new AgentBuilder.Transformer() {
                    @Override
                    public Builder<?> transform(Builder<?> builder, TypeDescription typeDescription,
                            ClassLoader classloader, JavaModule module,
                            ProtectionDomain domain) {
                        System.out.println(String.format("Transforming %s", typeDescription.getName()));
                        return builder.visit(Advice.to(TraceAdvice.class).on(ElementMatchers.isMethod()));
                    }
                }).installOn(instrumentation);
    }
}