package io.github.waujito.messenger.api.config

import io.github.waujito.messenger.api.user.IdUserRepository
import io.github.waujito.messenger.api.user.UserAuthenticationConverter
import io.github.waujito.messenger.api.user.UserAuthenticationEntryPoint
import io.github.waujito.messenger.api.user.UserRepository
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.config.annotation.web.invoke
import org.springframework.security.web.SecurityFilterChain
import org.springframework.web.cors.CorsConfiguration
import org.springframework.web.cors.CorsConfigurationSource
import org.springframework.web.cors.UrlBasedCorsConfigurationSource

@Configuration
@EnableWebSecurity
class DefaultSecurityConfig {
    @Bean
    fun defaultSecurityFilterChain(http: HttpSecurity, userRepository: UserRepository): SecurityFilterChain {
        http.invoke {
            oauth2ResourceServer {
                jwt {
                    jwtAuthenticationConverter = UserAuthenticationConverter(userRepository)
                }

                authenticationEntryPoint = UserAuthenticationEntryPoint()
            }

            authorizeRequests {
                authorize("/.~~spring-boot!~/**", permitAll)
                authorize("/error", permitAll)
                authorize("/", permitAll)
                authorize(anyRequest, authenticated)
            }

            cors {
                configurationSource = corsConfigurationSource()
            }
        }

        return http.build()
    }

    @Bean
    fun corsConfigurationSource(): CorsConfigurationSource {
        val configuration = CorsConfiguration()
        configuration.allowedOriginPatterns = listOf("*")
        configuration.allowedMethods = listOf("HEAD", "GET", "POST", "PUT", "DELETE", "PATCH")
        configuration.allowCredentials = true
        configuration.allowedHeaders =
                listOf(
                        "Accept",
                        "Origin",
                        "Content-Type",
                        "Depth",
                        "User-Agent",
                        "If-Modified-Since,",
                        "Cache-Control",
                        "Authorization",
                        "X-Req",
                        "X-File-Size",
                        "X-Requested-With",
                        "X-File-Name"
                )

        val source = UrlBasedCorsConfigurationSource()
        source.registerCorsConfiguration("/**", configuration)
        return source
    }

    @Bean
    fun userRepository(): UserRepository = IdUserRepository()
}