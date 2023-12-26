package io.github.waujito.messenger.api.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.config.annotation.web.invoke
import org.springframework.security.web.SecurityFilterChain

@Configuration
@EnableWebSecurity
class DefaultSecurityConfig {
    @Bean
    fun defaultSecurityFilterChain(http: HttpSecurity): SecurityFilterChain {
        http.invoke {
            authorizeRequests {
                authorize("/.~~spring-boot!~/**", permitAll)
                authorize("/", permitAll)
            }
        }

        return http.build()
    }
}