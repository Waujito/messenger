package io.github.waujito.messenger.auth

import org.apache.catalina.webresources.TomcatURLStreamHandlerFactory
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.security.core.Authentication
import org.springframework.security.core.GrantedAuthority
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
@RestController
class AuthenticationServiceApplication{

	@GetMapping("/")
	fun root(auth: Authentication): Collection<GrantedAuthority>{
		return auth.authorities
	}
}

fun main(args: Array<String>) {
	// Disables TomcatURLStreamHandlerFactory
	// to bypass the factory is already defined exception
	// when auto reloading the application with spring DevTools remote
	TomcatURLStreamHandlerFactory.disable()

	runApplication<AuthenticationServiceApplication>(*args)
}
