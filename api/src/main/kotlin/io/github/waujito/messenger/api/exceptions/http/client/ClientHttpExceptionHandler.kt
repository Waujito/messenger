package io.github.waujito.messenger.api.exceptions.http.client

import io.github.waujito.messenger.api.exceptions.BaseExceptionHandler
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class ClientHttpExceptionHandler : BaseExceptionHandler() {
    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(ex: NotFoundException) = baseHandler(ex, HttpStatus.NOT_FOUND)

    @ExceptionHandler(BadRequestException::class)
    fun handleBadRequest(ex: BadRequestException) = baseHandler(ex, HttpStatus.BAD_REQUEST, "Bad Request")

    @ExceptionHandler(ForbiddenException::class)
    fun handleBadRequest(ex: ForbiddenException) = baseHandler(ex, HttpStatus.FORBIDDEN, "Forbidden")
}