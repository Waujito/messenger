package io.github.waujito.messenger.api.exceptions.validation

import io.github.waujito.messenger.api.exceptions.BaseExceptionHandler
import jakarta.validation.ConstraintViolationException
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class ValidationExceptionHandler : BaseExceptionHandler() {
    @ExceptionHandler(ConstraintViolationException::class)
    fun handleConstraintViolation(ex: ConstraintViolationException) =
            baseHandler(ex, HttpStatus.BAD_REQUEST, "Bad request")
}