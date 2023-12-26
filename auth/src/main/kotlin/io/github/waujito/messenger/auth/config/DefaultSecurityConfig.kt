package io.github.waujito.messenger.auth.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.config.annotation.web.invoke
import org.springframework.security.core.GrantedAuthority
import org.springframework.security.core.authority.mapping.GrantedAuthoritiesMapper
import org.springframework.security.web.SecurityFilterChain
import org.springframework.security.web.context.NullSecurityContextRepository
import org.springframework.web.cors.CorsConfiguration
import org.springframework.web.cors.CorsConfigurationSource
import org.springframework.web.cors.UrlBasedCorsConfigurationSource


@Configuration
@EnableWebSecurity
class DefaultSecurityConfig {
    @Bean
    fun defaultSecurityFilterChain(http: HttpSecurity): SecurityFilterChain {
        http.invoke {
            cors { configurationSource = corsConfigurationSource() }

            authorizeRequests {
                authorize("/.~~spring-boot!~/**", permitAll)
                authorize("/error", permitAll)
                authorize("/.well-known/**", permitAll)
                authorize(anyRequest, authenticated)
            }

            oauth2Login {
                redirectionEndpoint { baseUri = "/oauth2/callback/*" }
            }
        }

        return http.build()
    }

    companion object {
        /**
         *
         * Set up cors settings for the application.
         *
         */
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
    }

    @Bean
    fun corsConfigurationSourceBean(): CorsConfigurationSource = corsConfigurationSource()

    /**
     *
     * Adds client to user authorities
     *
     * TODO: Remove this method when find solution for mapping user authorities on exchange user
     * info step
     */
    private fun userAuthoritiesMapper(): GrantedAuthoritiesMapper =
            GrantedAuthoritiesMapper { authorities: Collection<GrantedAuthority> ->
                val mappedAuthorities = authorities.toMutableList()

                // Adds OAUTH2_CLIENT_GOOGLE to all users logged in through OAuth2
                // Here is only one client, so it is allowed
                mappedAuthorities.add(GrantedAuthority { "OAUTH2_CLIENT_GOOGLEs" })

                mappedAuthorities
            }
}