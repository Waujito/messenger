package io.github.waujito.messenger.api

import org.apache.catalina.webresources.TomcatURLStreamHandlerFactory
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
@RestController
class ApiApplication{
	@GetMapping("/")
	fun hello(): String = "hello, world!"
}

fun main(args: Array<String>) {
	// Disables TomcatURLStreamHandlerFactory
	// to bypass the factory is already defined exception
	// when auto reloading the application with spring DevTools remote
	TomcatURLStreamHandlerFactory.disable()

	runApplication<ApiApplication>(*args)
}
