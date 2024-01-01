package io.github.waujito.messenger.api.exceptions.crud

import io.github.waujito.messenger.api.exceptions.BaseExceptionHandler
import jakarta.persistence.EntityNotFoundException
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class CrudExceptionHandler : BaseExceptionHandler() {
    @ExceptionHandler(EntityNotFoundException::class)
    fun handleNotFound() = baseHandler(HttpStatus.NOT_FOUND)

}